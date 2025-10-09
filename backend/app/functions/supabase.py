from settings import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client

supabaseClient: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
