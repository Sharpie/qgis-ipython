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
for the development version of IPython v0.12:

  https://github.com/ipython/ipython/blob/4e1a76c/docs/examples/lib/internal_ipkernel.py

The code has been modified slightly to achieve compatiblity with IPython v0.11.
"""
#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import subprocess
import sys

from IPython.zmq.ipkernel import IPKernelApp

#-----------------------------------------------------------------------------
# Functions and classes
#-----------------------------------------------------------------------------
def get_open_port():
    """Return a random open port
    This function is needed to make the internal kernel work with IPython v0.11.

    Starting with v0.12, a random port is chosen for the heartbeat socket when
    IPKernelApp is created.
    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

def pylab_kernel(gui):
    """Launch and return an IPython kernel with pylab support for the desired gui
    """
    kernel = IPKernelApp(hb_port = get_open_port())
    kernel.initialize(['python', '--pylab=%s' % gui ])
    return kernel


def qtconsole_cmd(kernel):
    """Compute the command to connect a qt console to an already running kernel
    """
    ports = ['--%s=%d' % (name, port) for name, port in kernel.ports.items()]
    return ['ipython', 'qtconsole', '--existing'] + ports


class InternalIPKernel(object):

    def init_ipkernel(self, backend):
        # Start IPython kernel with GUI event loop and pylab support
        self.ipkernel = pylab_kernel(backend)
        # To create and track active qt consoles
        self._qtconsole_cmd = qtconsole_cmd(self.ipkernel)
        self.consoles = []

        # This application will also act on the shell user namespace
        self.namespace = self.ipkernel.shell.user_ns
        # Keys present at startup so we don't print the entire pylab/numpy
        # namespace when the user clicks the 'namespace' button
        self._init_keys = set(self.namespace.keys())

        # Example: a variable that will be seen by the user in the shell, and
        # that the GUI modifies (the 'Counter++' button increments it):
        self.namespace['app_counter'] = 0
        #self.namespace['ipkernel'] = self.ipkernel  # dbg

    def print_namespace(self, evt=None):
        print "\n***Variables in User namespace***"
        for k, v in self.namespace.iteritems():
            if k not in self._init_keys and not k.startswith('_'):
                print '%s -> %r' % (k, v)
        sys.stdout.flush()

    def new_qt_console(self, evt=None):
        self.consoles.append(subprocess.Popen(self._qtconsole_cmd))

    def count(self, evt=None):
        self.namespace['app_counter'] += 1

    def cleanup_consoles(self, evt=None):
        for c in self.consoles:
            c.kill()
