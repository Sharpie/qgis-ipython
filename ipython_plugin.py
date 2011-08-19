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
import sys

from PyQt4.QtCore import Qt, QObject, SIGNAL
from PyQt4.QtGui import QAction, QIcon, QMenu

from qgis.core import QgsApplication

# Most IPython modules require `sys.argv` to be defined.
if not hasattr(sys, 'argv'):
    sys.argv = QgsApplication.instance().argv()

import resources # Initialize Qt resources from file resources.py
from .ipython.internal_ipkernel import InternalIPKernel


class QGIS_IPython(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.kernel = None

    def initGui(self):
        # Create action that will start plugin configuration
        self.launch_external_console = QAction(
            QIcon(":/plugins/ipython_console/logos/launch_external_python.png"),
            "External IPython Console", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.launch_external_console, SIGNAL("triggered()"),
                self.launch_console)


        # Add toolbar menu item
        self.iface.pluginMenu().addAction(self.launch_external_console)
        self.iface.addToolBarIcon(self.launch_external_console)

    def init_kernel(self):
        kernel = InternalIPKernel()
        kernel.app = QgsApplication.instance()

        kernel.init_ipkernel('qt')
        # Start the threads that make up the IPython kernel and integrate them
        # with the Qt event loop.
        kernel.ipkernel.start()

        self.kernel = kernel

    def unload(self):
        # Remove the plugin menu item and icon.
        self.iface.pluginMenu().removeAction(self.launch_external_console)
        self.iface.removeToolBarIcon(self.launch_external_console)

        if self.kernel is not None:
            # Tear down any running consoles and then stop the kernel.
            self.kernel.cleanup_consoles()

    def launch_console(self):
        if self.kernel is None:
            self.init_kernel()

        self.kernel.new_qt_console()

