#-*- coding: utf-8 -*-
from PyQt4.QtGui import QStandardItemModel, QStandardItem 

from engineConsole.views import TreeViewTela


class ItemFuncao(object):
    def __init__(self, item, funcao):
        self.item = item
        self.funcao = funcao


class Menu(TreeViewTela):
    def __init__(self, altura, parent=None):
        super().__init__(altura, parent)

        self._model = QStandardItemModel(0, 1)
        self._model.setHorizontalHeaderItem(0, QStandardItem("Menu"))

        self._itemsFuncoes = []

    def setMenu(self, menu):
        self._adicionarSubMenu(menu, self._model.invisibleRootItem())
        self.setSelecionado(self._model.index(0,0))

    def getMenuSelecionado(self):
        sel = self.getSelecionado()
        s = ''
        while sel.isValid():
            s = '/' + sel.data() + s
            sel = sel.parent()
        return s

    def getFuncaoItem(self, item):
        for i in self._itemsFuncoes:
            if i.item == item.data():
                return i.funcao

    def getFuncaoItemSelecionado(self):
        return self.getFuncaoItem(self.getSelecionado())
        
    def _adicionarSubMenu(self, subMenu, pai):
        if isinstance(subMenu, ItemFuncao):
            item = QStandardItem(subMenu.item)
            self._itemsFuncoes.append(subMenu)
            pai.appendRow(item)
        elif isinstance(subMenu, str):
            pai.appendRow(QStandardItem(subMenu))
        elif isinstance(subMenu, (tuple, list)):
            for i in subMenu:
                self._adicionarSubMenu(i, pai)
        else:
            for key, value in subMenu.items():
                p = QStandardItem(key)
                pai.appendRow(p)
                self._adicionarSubMenu(value, p)


if __name__ == '__main__':
    def inicial():
        print("INICIAL")

    def final():
        print("FINAL")

    def executarFuncao():
        f = m.getFuncaoItemSelecionado()
        if f:
            f()
            
    from engineConsole.base.baseApplication import CApplication
    
    cApp = CApplication()
    m = Menu(10)
    m.setMenu({"Cadastro":
                 ("Usuario",
                  {"Empresa":
                    (ItemFuncao("Inicial",inicial), ItemFuncao("Final",final))
                  }
                 )
               ,
               "Relatorio":
                 "Mensal"}
              )
    m.enterPressed.connect(executarFuncao)
    m.show()
    cApp.exec_()
                
