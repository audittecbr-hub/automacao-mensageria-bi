import pyodbc

try:
    conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.2.34;DATABASE=STUDIO_FISCAL;UID=sa;PWD=Studio@2021;TrustServerCertificate=yes;"
    conn = pyodbc.connect(conn_str, timeout=5)
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM dbo.vw_powerbi_regionais_hono_encontrados")
    cols = [col[0] for col in cursor.description]
    print("Columns in dbo.vw_powerbi_regionais_hono_encontrados:")
    for c in cols:
        print(f"  - {c}")
except Exception as e:
    print(f"Error: {e}")
