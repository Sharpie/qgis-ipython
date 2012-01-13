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

This code is a modified vesion of an IPython example created by Fernando Perez
for IPython v0.12:

  https://github.com/ipython/ipython/blob/rel-0.12/docs/examples/lib/internal_ipkernel.py
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import subprocess
import os

from IPython.zmq.ipkernel import IPKernelApp

#-----------------------------------------------------------------------------
# Functions and classes
#-----------------------------------------------------------------------------
def loop_qgis(kernel):
    """QGIS event loop for IPython kernels.

    Based on loop_qt in IPython.zmq.eventloops, but uses the special QGIS main
    application instance and avoids trying to launch a new instance. Using
    loop_qt will cause starting the kernel to hang QGIS with IPython 0.12 or
    later.
    """
    from qgis.core import QgsApplication
    from PyQt4 import QtCore

    kernel.app = QgsApplication.instance()
    kernel.timer = QtCore.QTimer()
    kernel.timer.timeout.connect(kernel.do_one_iteration)
    # Units for the timer are in milliseconds
    kernel.timer.start(1000*kernel._poll_interval)


class InternalIPKernel(object):
    """Class for managing an IPython kernel inside of QGIS.

    IPython normally runs kernels in seperate processes, but this setup is
    limiting in the case of QGIS because external kernels cannot access the
    data and variables that QGIS is working with. This class manages an
    in-process kernel and is capable of launching external consoles that can
    attach to the kernel.

    IPython Consoles are run as external processes because they rely on
    Version 2 of the PyQt api and QGIS is using Version 1 which is
    incompatible.
    """
    def __init__(self):
        # Start IPython kernel with QGIS event loop integration and pylab
        # support
        self.ipkernel = IPKernelApp()
        self.ipkernel.initialize(['python', '--pylab=qt',
            # Ensure the Kernel pre-loads the same modules as the QGIS python
            # console.
            "--c='from qgis.core import *;import qgis.utils;'"])
        # Ensure we use an event loop that is QGIS-friendly.
        self.ipkernel.kernel.eventloop = loop_qgis
        self.ipkernel.start()

        # To create and track active qt consoles
        self._qtconsole_cmd = ['ipython', 'qtconsole', '--existing'] + \
                [os.path.basename(self.ipkernel.connection_file)]
        self.consoles = []

    def new_qt_console(self, evt=None):
        self.consoles.append(subprocess.Popen(self._qtconsole_cmd))

    def cleanup_consoles(self, evt=None):
        for c in self.consoles:
            c.kill()
