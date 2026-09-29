from src.core.services.supabase_service import SupabaseService

svc = SupabaseService()
templates = svc._get("automation_templates", {"select": "*"})
print(f"Total templates: {len(templates)}")
for t in templates:
    print(f"Template: {t.get('name')} (Type: {t.get('type')})")
    print(t.get("content"))
    print("-" * 50)
