from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QFont, QKeyEvent, QTextCursor
from PyQt6.QtCore import Qt

class CodeEditor(QTextEdit):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()
        
    def setup_editor(self):
        font = QFont("Courier New", 12)
        font.setFixedPitch(True)
        self.setFont(font)

        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        
        self.setPlaceholderText("Введите текст для анализа...")
        
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Tab:
            self.insertPlainText("    ")
        else:
            super().keyPressEvent(event)
            
    def get_current_line(self):
        cursor = self.textCursor()
        return cursor.blockNumber() + 1
        
    def get_current_column(self):
        cursor = self.textCursor()
        return cursor.columnNumber() + 1
        
    def get_text_length(self):
        return len(self.toPlainText())
        
    def insert_text_at_cursor(self, text):
        self.insertPlainText(text)
        
    def get_selected_text(self):
        cursor = self.textCursor()
        return cursor.selectedText() if cursor.hasSelection() else ""
        
    def set_error_position(self, line, column):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        
        for _ in range(line - 1):
            cursor.movePosition(QTextCursor.MoveOperation.Down)
            
        for _ in range(column - 1):
            cursor.movePosition(QTextCursor.MoveOperation.Right)
            
        self.setTextCursor(cursor)

        self.ensureCursorVisible()


class SyntaxHighlighter:
    
    def __init__(self, parent=None):
        self.parent = parent
        self.highlighting_rules = []
        
    def highlight_block(self, text):

        pass
        
    def add_rule(self, pattern, format):

        self.highlighting_rules.append((pattern, format))