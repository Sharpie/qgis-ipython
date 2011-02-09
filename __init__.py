"""
/***************************************************************************
 ipython
                                 A QGIS plugin
 An enhanced QGIS console powered by IPython
                             -------------------
        begin                : 2011-02-06
        copyright            : (C) 2011 by Charlie Sharpsteen
        email                : source@sharpsteen.net
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
def name():
    return "IPython Console"
def description():
    return "An enhanced QGIS console powered by IPython"
def version():
    return "Version 0.1.1"
def icon():
    return "python_logo.png"
def qgisMinimumVersion():
    return "1.6"
def classFactory(iface):
    # load ipython class from file ipython
    from ipython import QGIS_IPython
    return QGIS_IPython(iface)
