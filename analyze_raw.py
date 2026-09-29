with open('dump_encontrados_fixed.html', 'r', encoding='utf-8') as f:
    html = f.read()

raw_start = html.find("<div id='raw-data' style='display:none;'>") + len("<div id='raw-data' style='display:none;'>")
raw_end = html.find("</div>", raw_start)
raw = html[raw_start:raw_end]
items = raw.split('~')

print("Total items:", len(items))

# Let's see what happens if items are filtered by some condition
# Look at the rows in Image 1:
# Row 1: Sandro (86730-FTX) - 14.511,22
# Row 2: Sandro (86730-FTX) - 26.824,47
# Row 3: Bari (87233-RPQ) - 57.440,99
# Row 4: SPM Resende (86146-T) - 48.354,32

# Let's check all 201 rows if there is a common filter!
# In step 2942 we found:
# Index 5, 15, 17, 63, 67, 68, 69, 81, 82, 121, 122...
# Notice: In dump_encontrados_fixed.html:
# Index 0 is Sul (S)
# Index 1 is Sudeste 2 (SD)
# Index 2 is NNCO (N)
# Index 3 is SP (SP)
# Index 4 is Sudeste 2 (SD)
# Index 5 is SP (SP) -> Sandro!
