import clr
import System
import sys

dll_path = r"C:\Program Files\WindowsApps\Microsoft.MicrosoftPowerBIDesktop_2.157.879.0_x64__8wekyb3d8bbwe\bin\Microsoft.AnalysisServices.Tabular.dll"
clr.AddReference(dll_path)

from Microsoft.AnalysisServices.Tabular import Server

server = Server()
server.Connect("localhost:62970")
db = server.Databases[0]
model = db.Model

print(f"Connected to model: {model.Name}")
print(f"Total tables: {model.Tables.Count}")

broken = []
for t in model.Tables:
    for m in t.Measures:
        expr = m.Expression
        if 'SYNTAXERROR' in expr:
            print(f"\n[SYNTAXERROR] {t.Name}[{m.Name}]:\n{expr[:300]}")
            broken.append((t.Name, m.Name, "SYNTAXERROR"))
        if '\\' in expr:
            print(f"\n[BACKSLASH] {t.Name}[{m.Name}]")
            broken.append((t.Name, m.Name, "BACKSLASH"))

print(f"\nTotal broken measures found: {len(broken)}")
