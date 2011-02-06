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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# Initialize Qt resources from file resources.py
import resources

# Import the code for the dialog
from console import IPythonConsole


class ipython:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Create action that will start plugin configuration
        self.show_console = QAction(QIcon(":/plugins/ipython/python_logo.png"),
            "IPython Console", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.show_console, SIGNAL("triggered()"),
                self.doConsole)

        self.ipython_console = IPythonConsole()

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.show_console)
        self.iface.pluginMenu().addAction(self.show_console)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.pluginMenu().removeAction(self.show_console)
        self.iface.removeToolBarIcon(self.show_console)

    # run method that performs all the real work
    def doConsole(self):
        self.ipython_console.show()
        self.ipython_console.activateWindow()
