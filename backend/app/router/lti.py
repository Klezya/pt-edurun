from fastapi import APIRouter

router = APIRouter()

@router.get("/health/")
async def get_canvas_data():
    return {"status": "ok"}

@router.get("/check_user/{user_id_lms}")
async def is_user_registered(user_id_lms: str):
    from functions.lti import is_user_registered
    return is_user_registered(user_id_lms)