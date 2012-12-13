#-*- coding: utf-8 -*-
from PyQt4.QtCore import QTimer, QTime

from engineConsole.base.telaConsole import TelaConsole

class HelloWorld(TelaConsole):
    def desenhoTela(self, tam):
        return "Hello World"

class RelogioConsole(TelaConsole):
    def __init__(self, mostrarSegundos=False, parent=None):
        super().__init__(parent)
        self._mostrarSegundos = mostrarSegundos

        self._timer = QTimer()
        self._timer.timeout.connect(self.update)
        self._timer.start(1000)

    def desenhoTela(self, tam):
        return QTime.currentTime().toString('hh:mm:ss')

        
if __name__ == '__main__':
    from engineConsole.base.baseApplication import CApplication
    cApp = CApplication()
    h = HelloWorld()
    h.show()
    """painel = PainelConsole()
    v = VLayoutTela()
    r = RelogioConsole()
    v.addTela(40,r)
    p = PainelConsole()
    d = LabelEditConsole("TESTE")
    p.addTela(d)
    e = LabelEditConsole("NOVO")
    p.addTela(e)
    v.addTela(20,p)
    painel.addTela(v)
    painel.show()

    q = LabelEditConsole("NADA")
    p = PopupConsole(q)
    from PyQt4.QtCore import QTimer
    QTimer.singleShot(2000, lambda: p.show())
    QTimer.singleShot(5000, lambda: p.close())"""
    
    cApp.exec_()
