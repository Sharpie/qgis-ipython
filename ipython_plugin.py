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
"""
from PyQt4.QtCore import Qt, QObject, SIGNAL
from PyQt4.QtGui import QAction, QIcon, QMenu

# Initialize Qt resources from file resources.py
import resources


class QGIS_IPython(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Create action that will start plugin configuration
        self.show_console = QAction(
            QIcon(":/plugins/ipython_console/logos/IPy_logo.png"),
            "IPython", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.show_console, SIGNAL("triggered()"),
                self.load_console)


        # Add toolbar menu item
        self.iface.pluginMenu().addAction(self.show_console)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.pluginMenu().removeAction(self.show_console)

    def load_console(self):
        return

