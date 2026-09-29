import os
import shutil

src = r'c:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\repasse (3).SemanticModel\definition\tables\medidas_html.tmdl'
dst_onedrive = r'c:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl'
dst_downloads = r'c:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\repasse.SemanticModel\definition\tables\medidas_html.tmdl'

# Copy clean file to OneDrive and Downloads
shutil.copy2(src, dst_onedrive)
if os.path.exists(dst_downloads):
    shutil.copy2(src, dst_downloads)

print('Clean TMDL copied successfully to OneDrive and Downloads!')
