# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Komiwojazer
                                 A QGIS plugin
 Wyznaczanie optymalnej trasy
                             -------------------
        begin                : 2018-01-02
        copyright            : (C) 2018 by Magdalena Węgrzyn
        email                : magdalenawegrzyn9@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Komiwojazer class from file Komiwojazer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .komiwojazer_qgis import Komiwojazer
    return Komiwojazer(iface)
