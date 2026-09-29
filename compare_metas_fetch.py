import os
from dotenv import load_dotenv
load_dotenv()
from src.core.services.powerbi_data import PowerBIDataFetcher

print("=== 1. FETCHING FROM Ranking_Metas (5f1e9f0f...) ===")
os.environ["POWERBI_METAS_DATASET_ID"] = "5f1e9f0f-8388-438d-a0be-6a5e13bb3ce4"
f1 = PowerBIDataFetcher()
f1.client.dataset_id = "5f1e9f0f-8388-438d-a0be-6a5e13bb3ce4"
total1, deps1, rec1 = f1.fetch_all_data()

print("\n=== 2. FETCHING FROM Ranking_Metas_V2 (72edf515...) ===")
os.environ["POWERBI_METAS_DATASET_ID"] = "72edf515-6d51-4fb9-ad43-be8b77c85604"
f2 = PowerBIDataFetcher()
f2.client.dataset_id = "72edf515-6d51-4fb9-ad43-be8b77c85604"
total2, deps2, rec2 = f2.fetch_all_data()

print("\n=== COMPARISON RESULTS ===")
print("TOTAL_GS MATCH:", total1 == total2)
print("RECEITAS MATCH:", rec1 == rec2)
print("DEPARTAMENTOS MATCH:", deps1 == deps2)

if total1 != total2:
    print("Total1:", total1)
    print("Total2:", total2)

if rec1 != rec2:
    print("Rec1:", rec1)
    print("Rec2:", rec2)

if deps1 != deps2:
    print("Deps1:", deps1)
    print("Deps2:", deps2)
