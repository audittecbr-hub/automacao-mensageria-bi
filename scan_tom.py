import clr
import System

clr.AddReference("Microsoft.AnalysisServices.Tabular")
from Microsoft.AnalysisServices.Tabular import Server

server = Server()
server.Connect("localhost:62970")
db = server.Databases[0]
model = db.Model

print(f"Connected to model: {model.Name}")
print(f"Tables: {model.Tables.Count}")

for t in model.Tables:
    for m in t.Measures:
        expr = m.Expression
        if 'SYNTAXERROR' in expr:
            print(f"[SYNTAXERROR FOUND] {t.Name}[{m.Name}]:\n{expr}")
        if '\\' in expr:
            print(f"[BACKSLASH FOUND] {t.Name}[{m.Name}]")

print("Finished scan of all measures via TOM!")
