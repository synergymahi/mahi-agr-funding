import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY or not SUPABASE_SERVICE_KEY:
    raise ValueError("Supabase URL, Key, and Service Key must be set in .env file")

# Client for general, anonymous, or user-specific access
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# A separate client for admin operations requiring elevated privileges
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def get_supabase_client() -> Client:
    return supabase

def get_supabase_admin_client() -> Client:
    return supabase_admin