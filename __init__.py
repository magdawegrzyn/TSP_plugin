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
import sys, os
plugin_dir = os.path.dirname(__file__)
site_packages_dir = os.path.join(plugin_dir, 'site-packages')


# Checking the presence of ortools library
try:
    from ortools.constraint_solver import pywrapcp
    from ortools.constraint_solver import routing_enums_pb2
except:
    if site_packages_dir not in sys.path:
        sys.path.append(site_packages_dir)

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Komiwojazer class from file Komiwojazer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .komiwojazer_qgis import Komiwojazer
    return Komiwojazer(iface)
