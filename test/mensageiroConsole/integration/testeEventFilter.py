#-*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/mensageiroConsole/src")

from engineConsole.base.baseApplication import CApplication
from engineConsole.base.eventoTeclado import EventoTecladoConsole
from engineConsole.base.telaConsole import TelaConsole
from engineConsole.telas import PainelConsole


class Tela(TelaConsole):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._texto = ''

    def eventFilter(self, obj, evento):
        if isinstance(evento, EventoTecladoConsole):
            self.setTexto("FILTER"+evento.tecla())
            return False

        return True

    def setTexto(self, texto):
        self._texto = texto
        self.update()
        
    def onKey(self, key):
        self.setTexto('KEY: '+key+'\n')
        
    def onEscape(self):
        self.setTexto('KEY: ESC\n')

    def onDirecional(self, direc):
        self.setTexto("DIRECIONAL: "+direc+'\n')

    def onFuncional(self, func):
        self.setTexto("FUNCIONAL: "+func+'\n')

    def onEnter(self):
        self.setTexto("KEY: ENTER")

    def acceptFocus(self):
        return True

    def desenhoTela(self, tam):
        return '>' + self._texto + str(self.hasFocus())


cApp = CApplication()
p = PainelConsole()
t = Tela()
t2 = Tela()
t.installEventFilter(t2)
p.addTela(t)
p.addTela(t2)
p.show()

cApp.exec_()
