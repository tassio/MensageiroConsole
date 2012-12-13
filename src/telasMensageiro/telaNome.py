# -*- coding: utf-8 -*-

from engineConsole.telas import LabelEditConsole


class TelaNome(LabelEditConsole):
    def __init__(self, servico, parent=None):
        super().__init__(textoLabel='Nome',parent=parent)

        self._servico = servico
        self.setTexto(self._servico.getNome())

        self.enterPressed.connect(self._alterarNome)
        
    def _alterarNome(self):
        self._servico.setNome(self.getTexto())
