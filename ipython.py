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
from PyQt4.QtGui import QAction, QIcon

# Initialize Qt resources from file resources.py
import resources

# Import the code for the dialog
from console import IPythonConsole


class QGIS_IPython(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Create action that will start plugin configuration
        self.show_console = QAction(QIcon(":/plugins/ipython_console/python_logo.png"),
            "IPython Console", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.show_console, SIGNAL("triggered()"),
                self.load_console)

        self.ipython_console = IPythonConsole(parent = self.iface.mainWindow())
        self.iface.mainWindow().addDockWidget(Qt.BottomDockWidgetArea,
                self.ipython_console)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.show_console)
        self.iface.pluginMenu().addAction(self.show_console)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.pluginMenu().removeAction(self.show_console)
        self.iface.removeToolBarIcon(self.show_console)

    def load_console(self):
        self.ipython_console.show()
        self.ipython_console.activateWindow()

