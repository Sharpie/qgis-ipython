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

import code
import sys
import traceback
import IPython.Shell

from ui_console import Ui_IPython


class IPythonConsole(QWidget, Ui_IPython):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.console = PythonEdit()
        self.verticalLayout.addWidget(self.console)


#------------------------------------------------------------------------------
# Console Implementation
#   (Borrowed from QGIS console.py)
#------------------------------------------------------------------------------
_init_commands = ["from qgis.core import *", "import qgis.utils"]

class PythonEdit(QTextEdit, code.InteractiveInterpreter):

  def __init__(self,parent=None):
    QTextEdit.__init__(self, parent)
    self.shell = IPython.Shell.start()

    self.setTextInteractionFlags(Qt.TextEditorInteraction)
    self.setAcceptDrops(False)
    self.setMinimumSize(30, 30)
    self.setUndoRedoEnabled(False)
    self.setAcceptRichText(False)
    monofont = QFont("Monospace")
    monofont.setStyleHint(QFont.TypeWriter)
    self.setFont(monofont)

    self.buffer = []

    self.insertInitText()

    for line in _init_commands:
      self.shell.IP.runsource(line)

    self.displayPrompt(False)

    self.history = QStringList()
    self.historyIndex = 0

    self.high = ConsoleHighlighter(self)

  def insertInitText(self):
    self.insertTaggedText(QCoreApplication.translate("PythonConsole", "To access Quantum GIS environment from this console\n"
                          "use qgis.utils.iface object (instance of QgisInterface class).\n\n"),
                          ConsoleHighlighter.INIT)


  def clearConsole(self):
    self.clear()
    self.insertInitText()

  def displayPrompt(self, more=False):
    self.currentPrompt = "... " if more else ">>> "
    self.currentPromptLength = len(self.currentPrompt)
    self.insertTaggedLine(self.currentPrompt, ConsoleHighlighter.EDIT_LINE)
    self.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)

  def isCursorInEditionZone(self):
    cursor = self.textCursor()
    pos = cursor.position()
    block = self.document().lastBlock()
    last = block.position() + self.currentPromptLength
    return pos >= last

  def currentCommand(self):
    block = self.cursor.block()
    text = block.text()
    return text.right(text.length()-self.currentPromptLength)

  def showPrevious(self):
        if self.historyIndex < len(self.history) and not self.history.isEmpty():
            self.cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.MoveAnchor)
            self.cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
            self.cursor.removeSelectedText()
            self.cursor.insertText(self.currentPrompt)
            self.historyIndex += 1
            if self.historyIndex == len(self.history):
                self.insertPlainText("")
            else:
                self.insertPlainText(self.history[self.historyIndex])

  def showNext(self):
        if  self.historyIndex > 0 and not self.history.isEmpty():
            self.cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.MoveAnchor)
            self.cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
            self.cursor.removeSelectedText()
            self.cursor.insertText(self.currentPrompt)
            self.historyIndex -= 1
            if self.historyIndex == len(self.history):
                self.insertPlainText("")
            else:
                self.insertPlainText(self.history[self.historyIndex])

  def updateHistory(self, command):
        if isinstance(command, QStringList):
            for line in command:
                self.history.append(line)
        elif not command == "":
            if len(self.history) <= 0 or \
            not command == self.history[-1]:
                self.history.append(command)
        self.historyIndex = len(self.history)

  def keyPressEvent(self, e):
        self.cursor = self.textCursor()
        # if the cursor isn't in the edition zone, don't do anything except Ctrl+C
        if not self.isCursorInEditionZone():
            if e.modifiers() & Qt.ControlModifier or e.modifiers() & Qt.MetaModifier:
                if e.key() == Qt.Key_C or e.key() == Qt.Key_A:
                    QTextEdit.keyPressEvent(self, e)
            else:
                # all other keystrokes get sent to the input line
                self.cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
        else:
            # if Return is pressed, then perform the commands
            if e.key() == Qt.Key_Return:
                self.entered()
            # if Up or Down is pressed
            elif e.key() == Qt.Key_Down:
                self.showPrevious()
            elif e.key() == Qt.Key_Up:
                self.showNext()
            # if backspace is pressed, delete until we get to the prompt
            elif e.key() == Qt.Key_Backspace:
                if not self.cursor.hasSelection() and self.cursor.columnNumber() == self.currentPromptLength:
                    return
                QTextEdit.keyPressEvent(self, e)
            # if the left key is pressed, move left until we get to the prompt
            elif e.key() == Qt.Key_Left and self.cursor.position() > self.document().lastBlock().position() + self.currentPromptLength:
                anchor = QTextCursor.KeepAnchor if e.modifiers() & Qt.ShiftModifier else QTextCursor.MoveAnchor
                move = QTextCursor.WordLeft if e.modifiers() & Qt.ControlModifier or e.modifiers() & Qt.MetaModifier else QTextCursor.Left
                self.cursor.movePosition(move, anchor)
            # use normal operation for right key
            elif e.key() == Qt.Key_Right:
                anchor = QTextCursor.KeepAnchor if e.modifiers() & Qt.ShiftModifier else QTextCursor.MoveAnchor
                move = QTextCursor.WordRight if e.modifiers() & Qt.ControlModifier or e.modifiers() & Qt.MetaModifier else QTextCursor.Right
                self.cursor.movePosition(move, anchor)
            # if home is pressed, move cursor to right of prompt
            elif e.key() == Qt.Key_Home:
                anchor = QTextCursor.KeepAnchor if e.modifiers() & Qt.ShiftModifier else QTextCursor.MoveAnchor
                self.cursor.movePosition(QTextCursor.StartOfBlock, anchor, 1)
                self.cursor.movePosition(QTextCursor.Right, anchor, self.currentPromptLength)
            # use normal operation for end key
            elif e.key() == Qt.Key_End:
                anchor = QTextCursor.KeepAnchor if e.modifiers() & Qt.ShiftModifier else QTextCursor.MoveAnchor
                self.cursor.movePosition(QTextCursor.EndOfBlock, anchor, 1)
            # use normal operation for all remaining keys
            else:
                QTextEdit.keyPressEvent(self, e)
        self.setTextCursor(self.cursor)
        self.ensureCursorVisible()

  def insertFromMimeData(self, source):
        self.cursor = self.textCursor()
        self.cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor, 1)
        self.setTextCursor(self.cursor)
        if source.hasText():
            pasteList = QStringList()
            pasteList = source.text().split("\n")
            for line in pasteList:
		self.insertPlainText(line)
		self.runCommand(unicode(line))

  def entered(self):
    self.cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
    self.setTextCursor(self.cursor)
    self.runCommand( unicode(self.currentCommand()) )

  def insertTaggedText(self, txt, tag):

    if len(txt) > 0 and txt[-1] == '\n': # remove trailing newline to avoid one more empty line
      txt = txt[0:-1]

    c = self.textCursor()
    for line in txt.split('\n'):
      b = c.block()
      b.setUserState(tag)
      c.insertText(line)
      c.insertBlock()

  def insertTaggedLine(self, txt, tag):
    c = self.textCursor()
    b = c.block()
    b.setUserState(tag)
    c.insertText(txt)

  def runCommand(self, cmd):

    self.updateHistory(cmd)

    self.insertPlainText("\n")

    self.buffer.append(cmd)
    src = "\n".join(self.buffer)
    more = self.shell.IP.runsource(src, "<input>")
    if not more:
      self.buffer = []

    output = sys.stdout.get_and_clean_data()
    if output:
      self.insertTaggedText(output, ConsoleHighlighter.OUTPUT)
    self.displayPrompt(more)

  def write(self, txt):
    """ reimplementation from code.InteractiveInterpreter """
    self.insertTaggedText(txt, ConsoleHighlighter.ERROR)


class ConsoleHighlighter(QSyntaxHighlighter):
  EDIT_LINE, ERROR, OUTPUT, INIT = range(4)
  def __init__(self, doc):
    QSyntaxHighlighter.__init__(self,doc)
    formats = { self.OUTPUT    : Qt.black,
		self.ERROR     : Qt.red,
		self.EDIT_LINE : Qt.darkGreen,
		self.INIT      : Qt.gray }
    self.f = {}
    for tag, color in formats.iteritems():
      self.f[tag] = QTextCharFormat()
      self.f[tag].setForeground(color)

  def highlightBlock(self, txt):
    size = txt.length()
    state = self.currentBlockState()
    if state == self.OUTPUT or state == self.ERROR or state == self.INIT:
      self.setFormat(0,size, self.f[state])
    # highlight prompt only
    if state == self.EDIT_LINE:
      self.setFormat(0,3, self.f[self.EDIT_LINE])
