# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Komiwojazer
                                 A QGIS plugin
 Wyznaczanie optymalnej trasy
                              -------------------
        begin                : 2018-01-02
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Magdalena Węgrzyn
        email                : magdalenawegrzyn9@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QMessageBox
from qgis.gui import QgsMapLayerProxyModel, QgsMessageBar
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from komiwojazer_qgis_dialog import KomiwojazerDialog
import os.path, utils
import tsp_script, tcp_api, tcp_api_google
from qgis.core import *

class Komiwojazer:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Komiwojazer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Travelling Salesman Problem')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Travelling Salesman Problem')
        self.toolbar.setObjectName(u'Travelling Salesman Problem')


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Komiwojazer', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = KomiwojazerDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/TSP/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'TSP'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.dlg.routingModeComboBox.addItems(['fastest route', 'shortest route'])
        self.dlg.travelModeComboBox.addItems(['car', 'bicycle', 'pedestrian'])
        self.dlg.mapLayerComboBox.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.dlg.fieldComboBox.setLayer(self.dlg.mapLayerComboBox.currentLayer())
        self.dlg.mapLayerComboBox.layerChanged.connect(self.mapLayerComboBox_layerChanged) #aktualizacja listy pol
        self.dlg.orsRadioButton.setChecked(True)

    def mapLayerComboBox_layerChanged(self):
        self.dlg.fieldComboBox.setLayer(self.dlg.mapLayerComboBox.currentLayer())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Travelling Salesman Problem'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:

            #warstwa wejsciowa punktowa
            inLayer = self.dlg.mapLayerComboBox.currentLayer()
            outLayer = "" #wyjsciowa warstwa liniowa
            self.srcCrs = inLayer.crs()
            self.destCrs = QgsCoordinateReferenceSystem(4326)  # WGS 84 / UTM zone 33N
            self.xform = QgsCoordinateTransform(self.srcCrs, self.destCrs)
            #liczba punktow w warstwie wejsciowej
            inLayerFeatureCount = inLayer.featureCount()
            tmode = self.dlg.travelModeComboBox.currentText()
            rmode = self.dlg.routingModeComboBox.currentText()
            #messagebox
            mbx = QMessageBox(self.dlg)
            mbx.setIcon(QMessageBox.Warning)

            mbx.setStandardButtons(QMessageBox.Ok)

            #checking internet connection
            if not utils.isInternetConnected():
                mbx.setText(
                    "Check your internet connection first")
                mbx.show()
                return False

            locAndIds = self.pointLayerToLocationStringAndIdList(inLayer)
            startLocationString = locAndIds[0]
            startIdList = locAndIds[1]
            startNamesList = locAndIds[2]
            idNamesDict = dict(zip(startIdList,startNamesList))

            #google API limits
            if self.dlg.googleRadioButton.isChecked():#google
                if inLayerFeatureCount > 10:
                    mbx.setText(
                        "You can't solve TSP with this method, google maps API DistanceMatrix query limit is 10x10 points. Try with OpenRouteService.")
                    mbx.show()
                    return False
                else:
                    pass
            # ORS limits
            if self.dlg.orsRadioButton.isChecked():#OpenRouteService
                if inLayerFeatureCount > 5 and tmode != 'car':
                    mbx.setText(
                        "You can't solve TSP for travel mode = '%s', while number of points exceeds 5. Try 'car' mode" % tmode)
                    mbx.show()
                    return False
                elif inLayerFeatureCount > 50:
                    mbx.setText(
                        "You can't solve TSP with OpenRouteService for this layer, because number of points exceeds 50.")
                    mbx.show()
                    return False
                else:
                    pass

                # kolejnosc optymalna
                optimalIdList = self.resolveTSP(startLocationString, startIdList, "ORS")
                optimalLocationString = self.optimalLocationStringFromLayer(inLayer, optimalIdList)

                # wizualizacja optymalnej tasy
                outLayer = self.getTCPRoute(optimalLocationString, "ORS",rmode, tmode)

            elif self.dlg.googleRadioButton.isChecked():#Google API

                # kolejnosc optymalna
                optimalIdList = self.resolveTSP(startLocationString, startIdList, "google")
                if optimalIdList == False:
                    return False



                optimalLocationString = self.optimalLocationStringFromLayer(inLayer, optimalIdList)

                # wizualizacja optymalnej tasy
                outLayer = self.getTCPRoute(optimalLocationString,"google",rmode, tmode)
                if outLayer == False:
                    return False


            strRoute = self.convertRouteToString(optimalIdList, idNamesDict)  # wydruk wyniku
            self.addRouteStringToAttributes(outLayer, strRoute)
            QgsMapLayerRegistry.instance().addMapLayer(outLayer) #add layer to qgis
            self.printSolution(strRoute)


    def addRouteStringToAttributes(self,routeLayer,routeString):
        pr = routeLayer.dataProvider()
        routeIdx = routeLayer.fieldNameIndex('optimalRoute')
        attrMap = {1: {routeIdx: routeString}}
        pr.changeAttributeValues(attrMap)

    def convertRouteToString(self,idList,idToNameDict):
        route = ""
        for idEl in idList:
            point = idToNameDict[idEl]
            if type(point) != type("fff") and type(point) != type(u"fff"):
                point = str(point)
            else:
                pass
            route += point + " -> "
        return route[:-4]


    def printSolution(self,route):
        self.iface.messageBar().pushMessage("Travelling route:", route, level=QgsMessageBar.INFO, duration=35)


    def pointLayerToLocationStringAndIdList(self, layer):
        locationString = ''
        idList = []
        namesList =[]

        fieldName = self.dlg.fieldComboBox.currentField()

        for feat in layer.getFeatures():
            idList.append(feat.id())
            if fieldName == '' or fieldName is None:
                namesList.append(feat.id())
            else:
                namesList.append(feat[fieldName])

            geom = feat.geometry()

            if self.srcCrs != self.destCrs:
                geom.transform(self.xform)
            p = geom.asPoint()
            locationString += str(p.x())+','+str(p.y())+"|"
        return [locationString[:-1],idList,namesList]

    def optimalLocationStringFromLayer(self,layer,idList):
        locationString = ""
        for featid in idList:
            layer.setSelectedFeatures([int(featid)])
            for f in layer.selectedFeatures():
                geom = f.geometry()
                if self.srcCrs != self.destCrs:
                    geom.transform(self.xform)
                p = geom.asPoint()
                locationString += str(p.x()) + ',' + str(p.y()) + "|"
        layer.setSelectedFeatures([])
        return locationString[:-1]

    def resolveTSP(self,locationString,idList, provider):
        rmode = self.dlg.routingModeComboBox.currentText()
        tmode = self.dlg.travelModeComboBox.currentText()
        apiKey = self.dlg.apiTextEdit.text()
        if provider == "ORS":
            try:
                self.tcpapi = tcp_api.tcp_api(rmode, tmode,apiKey)
                matrix = self.tcpapi.DistMatrix(locationString)
            except:
                self.tcpapi = tcp_api.tcp_api(rmode, tmode)
                matrix = self.tcpapi.DistMatrix(locationString)
        elif provider == "google":
            if apiKey.strip() != "":
                try:
                    self.tcpapi = tcp_api_google.tcp_api(rmode, tmode,apiKey)
                except:
                    self.tcpapi = tcp_api_google.tcp_api(rmode, tmode)
                matrix = self.tcpapi.DistMatrix(locationString)
            else:
                self.tcpapi = tcp_api_google.tcp_api(rmode, tmode)
                matrix = self.tcpapi.DistMatrix(locationString)
        else:
            pass

        if type(matrix) != type(list()):
            self.iface.messageBar().pushMessage("Failed from Google API:", str(matrix), level=QgsMessageBar.CRITICAL, duration = 500)
            return False
        return tsp_script.runTSP(matrix=matrix, idList=idList)

    def getTCPRoute(self, locationString, provider, routeType, routeMode):
        directionsJson = self.tcpapi.GetDirections(locationString)

        # create memory layer
        v = QgsVectorLayer("LineString?crs=EPSG:4326", "TSP Route - " + routeType + " - " + routeMode, "memory")
        pr = v.dataProvider()
        qgsPoints = []
        linestring_feature = QgsFeature()

        dist = ""
        dur = ""

        if provider == "ORS":
            # iterate points and add to layer
            for point in directionsJson['features'][0]['geometry']['coordinates']:
                qgsPoints.append(QgsPoint(float(point[0]), float(point[1])))
            dist = directionsJson['features'][0]['properties']['summary'][0]["distance"]
            dur = directionsJson['features'][0]['properties']['summary'][0]["duration"]

        elif provider == "google":
            dist = 0
            dur = 0
            if directionsJson['status'] == "OK":
                qgsPoints = self.tcpapi.decodePolyline(directionsJson['routes'][0]['overview_polyline']['points'])
                for ob in directionsJson['routes'][0]['legs']:
                    dist += int(ob["distance"]["value"])
                    dur += int(ob["duration"]["value"])
            else:
                self.iface.messageBar().pushMessage("Failed from Google API:", directionsJson['status'] + " - " + directionsJson['error_message'], level=QgsMessageBar.CRITICAL, duration=500)
                return False
            dist = str(dist)
            dur = str(dur)

        else:
            pass



        linestring = QgsGeometry.fromPolyline(qgsPoints);
        linestring_feature.setGeometry(linestring)

        pr.addFeatures([linestring_feature])

        # update layer's extent when new features have been added
        v.updateExtents()

        # add attributes
        distField = QgsField('distance', QVariant.String, len = 30)
        durField = QgsField('duration', QVariant.String, len=30)
        routeField = QgsField('optimalRoute', QVariant.String, len=100)
        pr.addAttributes([distField,durField,routeField])
        v.updateFields()
        distIdx = v.fieldNameIndex('distance')
        durIdx = v.fieldNameIndex('duration')
        attrMap = {1: {distIdx: dist, durIdx: dur}}
        pr.changeAttributeValues(attrMap)

        return v
