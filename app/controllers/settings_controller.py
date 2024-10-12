from fastapi import APIRouter

router = APIRouter(prefix="/api/settings")

@router.post("/change/")
def set_bandwidth(change_type: str, payload):
    return {"output": output, "error": error}