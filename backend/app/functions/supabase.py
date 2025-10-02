import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabaseClient: Client = create_client("https://znduweqofbxljoivufcr.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpuZHV3ZXFvZmJ4bGpvaXZ1ZmNyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjM5NDg0MCwiZXhwIjoyMDcxOTcwODQwfQ.0nI7uj-ToMF1wI_eF44R0aQisE8CnS7cGsrBHKFh4aM")
