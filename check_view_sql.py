import pyodbc

conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=192.168.2.34;Database=STUDIO_FISCAL;Trusted_Connection=yes;"
try:
    conn = pyodbc.connect(conn_str, timeout=10)
    cursor = conn.cursor()
    cursor.execute("SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.vw_powerbi_job_repasse'))")
    row = cursor.fetchone()
    if row and row[0]:
        print("VIEW DEFINITION FOUND (length: {})".format(len(row[0])))
        with open('current_view_def.sql', 'w', encoding='utf-8') as f:
            f.write(row[0])
        print("First 300 chars:")
        print(row[0][:300])
        print("--- Contains CROSS APPLY? ---", "CROSS APPLY" in row[0])
        print("--- Contains OUTER APPLY? ---", "OUTER APPLY" in row[0])
    else:
        print("No definition returned.")
    conn.close()
except Exception as e:
    print("Error:", e)
