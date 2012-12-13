#-*- coding: utf-8 -*-

import sys
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/mensageiroConsole/src")

from engineConsole.base.engine import EngineConsole

EngineConsole.setTitle("Titulo")
print("Isso não deveria aparecer")
EngineConsole.clear()

print("Height:", EngineConsole.height(), "- Width:", EngineConsole.width())

print("Erro!")
assert EngineConsole.x() == 0
assert EngineConsole.y() == 2
EngineConsole.printxy(0, 1, "Certo!")
assert EngineConsole.x() == 0
assert EngineConsole.y() == 2

EngineConsole.ungetch("t")
t = EngineConsole.readkey()
assert t.key == "t" and t.code == 116 

print("OK")
EngineConsole.readkey()
