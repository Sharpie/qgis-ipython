"""
/***************************************************************************
 ipythonDialog
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
import commands

# IPython needs sys.argv to be defined
if not hasattr(sys, 'argv'):
    sys.argv = []

from IPython.frontend.qt.console.ipython_widget import IPythonWidget
from IPython.frontend.qt.kernelmanager import QtKernelManager
from IPython.utils.localinterfaces import LOCALHOST

from ui_console import Ui_IPythonConsole


class IPythonConsole(QDialog, Ui_IPythonConsole):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # This is here because QGIS defines sys.executable to be the QGIS app
        # and not a python interpreter---but only OS X.
        #
        # FIXME: put some guards around this statement so it only gets executed
        #        when absolutely needed.
        sys.executable = commands.getoutput('which python')

        self.kernel_manager = QtKernelManager()

        self.kernel_manager.start_kernel()
        self.kernel_manager.start_channels()

        self.console = IPythonWidget(local_kernel=LOCALHOST)
        self.console.kernel_manager = self.kernel_manager

        self.verticalLayout.addWidget(self.console)

