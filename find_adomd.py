import os
import glob

paths = glob.glob("C:/Program Files*/**/Microsoft.AnalysisServices.AdomdClient.dll", recursive=True)
for p in paths:
    print(p)
