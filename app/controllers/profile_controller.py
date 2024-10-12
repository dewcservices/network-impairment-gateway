from fastapi import APIRouter

router = APIRouter(prefix="/api/profiles")

@router.post("/")
def set_profile(profile_type: str):
    return {"output": output, "error": error}