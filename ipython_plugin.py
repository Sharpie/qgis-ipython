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

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QAction, QIcon, QMessageBox

from qgis.core import QgsApplication

# Most IPython modules require `sys.argv` to be defined.
if not hasattr(sys, 'argv'):
    sys.argv = QgsApplication.instance().argv()

import resources # Initialize Qt resources from file resources.py

try:
    from distutils.version import LooseVersion as V
    REQUIRED_IPYTHON_VERSION = V('0.12')

    import IPython, matplotlib, pygments

    if REQUIRED_IPYTHON_VERSION > V(IPython.__version__):
        raise ImportError

    from .ipython.internal_ipkernel import InternalIPKernel
    IPYTHON_LOADED = True
except:
    IPYTHON_LOADED = False


class QGIS_IPython(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.kernel = None

    def initGui(self):
        self.launch_external_console = QAction(
            QIcon(":/plugins/ipython_console/logos/launch_external_python.png"),
            "External IPython Console", self.iface.mainWindow())
        self.launch_external_console.setToolTip(
            "IPython console running in an external process")
        self.launch_external_console.connect(
            self.launch_external_console,
            SIGNAL("triggered()"),
            self.launch_console)


        # Add toolbar menu item
        self.iface.pluginMenu().addAction(self.launch_external_console)
        self.iface.addToolBarIcon(self.launch_external_console)

    def init_kernel(self):
        self.kernel = InternalIPKernel()

    def unload(self):
        if not IPYTHON_LOADED:
            return

        # Remove the plugin menu item and icon.
        self.iface.pluginMenu().removeAction(self.launch_external_console)
        self.iface.removeToolBarIcon(self.launch_external_console)

        if self.kernel is not None:
            # Tear down any running consoles and then stop the kernel.
            self.kernel.cleanup_consoles()

    def launch_console(self):
        # If IPython failed to load, bail out.
        if not IPYTHON_LOADED:
            QMessageBox.warning(
                self.iface.mainWindow(),
                'Error',
                'Could not load IPython components. Please make sure IPython version 0.12 or newer is installed along with the Pygments and Matplotlib modules.'
                )
            return

        if self.kernel is None:
            self.init_kernel()

        self.kernel.new_qt_console()

