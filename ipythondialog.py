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

from PyQt4 import QtCore, QtGui
from ui_ipython import Ui_ipython
# create the dialog for zoom to point
class ipythonDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_ipython()
        self.ui.setupUi(self)
