import pandas as pd
import io

step_output_path = r"C:/Users/cristhofer.maciel.GRUPOSTUDIO/.gemini/antigravity-ide/brain/53a8a01a-da38-486b-92ec-ae80b30b913e/.system_generated/steps/593/output.txt"
with open(step_output_path, 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('{"success":true}'):
    text = text.split('\n', 1)[1]

df = pd.read_csv(io.StringIO(text))
print("Columns:", list(df.columns))
print("Shape:", df.shape)
print("Sample head:")
print(df.head(2))

# Also check raw_tax_corporate.csv if present
import os
if os.path.exists("raw_tax_corporate.csv"):
    df_raw = pd.read_csv("raw_tax_corporate.csv")
    print("\nraw_tax_corporate.csv columns:", list(df_raw.columns))
    print("Shape:", df_raw.shape)
