try:
    import pyodbc
    print("pyodbc is available")
    drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]
    print("SQL Server Drivers:", drivers)
except Exception as e:
    print("pyodbc not available:", e)
