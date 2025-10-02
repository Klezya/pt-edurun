from functions.supabase import supabaseClient

def is_user_registered(user_id_lms: str):
    response = ( supabaseClient.table("usuario")
    .select("id_lms")
    .eq("id_lms", user_id_lms)
    .execute()
    )
    if response.data is None or len(response.data) == 0:
        return False
    return True