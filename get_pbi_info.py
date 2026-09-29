import os
import sys

try:
    import clr
except ImportError:
    os.system(f'"{sys.executable}" -m pip install pythonnet')
    import clr

dll_path = r"C:\Program Files\Microsoft Power BI Desktop\bin\Microsoft.AnalysisServices.Tabular.dll"
if not os.path.exists(dll_path):
    print(f"Could not find AMO DLL at {dll_path}")
    sys.exit(1)

clr.AddReference(dll_path)
import Microsoft.AnalysisServices.Tabular as TOM

server = TOM.Server()
try:
    server.Connect("Data Source=localhost:55036")
    db = server.Databases[0]
    print(f"Connected to database: {db.Name}")
    
    # List tables
    print("\nTables:")
    for t in db.Model.Tables:
        print(f" - {t.Name}")
except Exception as e:
    print(f"Error connecting: {e}")
