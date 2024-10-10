from fastapi import HTTPException, APIRouter, Depends

router = APIRouter(prefix="/api/settings")

@router.post("/change/")
def set_bandwidth(change_type: str, payload):
    return {"output": output, "error": error}