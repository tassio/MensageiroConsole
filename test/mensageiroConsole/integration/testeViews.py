#-*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/mensageiroConsole/src")

from PyQt4.QtGui import QApplication, QStandardItem, QStandardItemModel, QListView, QTableView, QTreeView
from PyQt4.QtCore import QModelIndex

from engineConsole.painelConsole import PainelConsole
from engineConsole.views import TreeViewTela, TableViewTela, ListViewTela
from engineConsole.base.baseApplication import CApplication


cApp = CApplication(QApplication([]))

"""
from PyQt4.QtSql import *

db = QSqlDatabase.addDatabase("QPSQL")
db.setHostName("localhost")
db.setPort(5432)
db.setDatabaseName("postgres")
db.setUserName("postgres")
db.setPassword("123456")
db.open()

model = QSqlTableModel()
model.setTable("tb_teste")
model.select()"""

"""model = QStandardItemModel()
parent = model.invisibleRootItem()
for i in range(5):
    item = QStandardItem(str(i))
    parent.appendRow(item)
    parent.appendRow(QStandardItem(str(i+1)))
    parent = item"""

"""model = QStandardItemModel(10, 4)
for i in range(10):
    for j in range(4):
        item = QStandardItem("({0}, {1})".format(i, j))
        model.setItem(i, j, item)
        if i == 1:
            item.appendRow([QStandardItem("..({0}, {1})".format(i*3, k)) for k in range(4)])
"""

model = QStandardItemModel(2,1)
model.setHorizontalHeaderItem(0,QStandardItem("Menu"))
cadastro = QStandardItem("Cadastro")
model.setItem(0,0,cadastro)
pesquisa = QStandardItem("Pesquisa")
model.setItem(1,0,pesquisa)

for i in ["Usuarios", "Empresas"]:
    cadastro.appendRow(QStandardItem(i))
    pesquisa.appendRow(QStandardItem(i))

parent = QModelIndex()

"""model = QDirModel()
model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
parent = model.index(QDir.currentPath())"""

"""model = QFileSystemModel()"""

    
p = PainelConsole()
l = TreeViewTela(6)
l.setModel(model)
l.setRootIndex(parent)

tv = TableViewTela(6)
tv.setModel(model)
tv.setRootIndex(parent)

lv = ListViewTela(4)
lv.setModel(model)
lv.setRootIndex(parent)

p.addTela(l)
p.addTela(tv)
p.addTela(lv)
p.show()

li = QListView()
li.setWindowTitle("ListView")
li.setModel(model)
li.setRootIndex(parent)
li.show()

t = QTableView()
t.setModel(model)
t.setWindowTitle("TableView")
t.setRootIndex(parent)
t.show()


tr = QTreeView()
tr.setModel(model)
tr.setWindowTitle("TreeView")
tr.setRootIndex(parent)
tr.show()

cApp.exec_()
