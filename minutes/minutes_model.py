import os
import io

from PySide2 import QtCore
from PySide2.QtCore import Qt, QModelIndex, Signal, Slot
from PySide2.QtGui import QBrush
from PySide2.QtWidgets import QMessageBox

from problems import PROBLEMS
from annotation import Minute

class MinutesModel(QtCore.QAbstractTableModel): 

    def __init__(self, annotation, parent=None, *args): 
        super(MinutesModel, self).__init__()
        self.annotation = annotation
        self.annotation.modified_changed.connect(self.update)
        self.setHeaderData(0, QtCore.Qt.Horizontal, "Minute")
        self.annotation.visible_minutes_changed.connect(self.update)

    @Slot()
    def update(self):
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.annotation.minutes_count() 

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 4

    def headerData(self, index, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if index == 0:
                    return 'Minute'
                if index == 1:
                    return 'Adequacy'
                if index == 2:
                    return 'Grammaticality'
                if index == 3:
                    return 'Fluency'
        return super().headerData(index, orientation, role=role)

    def setData(self, index, data, role=Qt.EditRole):
        if index.isValid():
            i = index.row()
            j = index.column()
            if role == Qt.EditRole:
                if j == 0:
                    self.annotation.get_minute(i).text = data
                else:
                    if data < 1:
                        data = 1
                    if data > 5:
                        data = 5
                    if j == 1:
                        self.annotation.get_minute(i).adequacy = data
                    if j == 2:
                        self.annotation.get_minute(i).grammaticality = data
                    if j == 3:
                        self.annotation.get_minute(i).fluency = data
                return True
        return False
        
    def insertRow(self, position, row, parent=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position)
        self.annotation.insert_minute(position, row)

        self.endInsertRows()
        return True

    def removeRows(self, pos, count, parent=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), pos, pos + count - 1)

        self.annotation.remove_minutes(pos, count)

        self.endRemoveRows()
        return True

    def data(self, index, role=QtCore.Qt.DisplayRole):
        i = index.row()
        j = index.column()
        m = self.annotation.get_minute(i)
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if j == 0:
                return m.text
            if any([d.minute == m for d in self.annotation._das]):
                if j == 1:
                    return m.adequacy
                if j == 2:
                    return m.grammaticality
                if j == 3:
                    return m.fluency
        elif role == Qt.BackgroundRole:
            if self.annotation.is_minute_visible(m):
                return self.annotation.get_minute_color(m)
        elif role == Qt.ForegroundRole:
            if self.annotation.is_minute_visible(m):                
                return self.annotation.get_minute_text_color(m)
        else:
            return None

    def flags(self, index):
        i = index.row()
        j = index.column()
        m = self.annotation.get_minute(i)
        if self.annotation.is_minute_visible(m):
            return  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | super().flags(index)
        elif j > 0:
            return  (super().flags(index)) & ~QtCore.Qt.ItemIsEditable
