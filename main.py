from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Company Private OTA Server")

# 1. Static File Mounting
# 2. Check if the directory exists; if not, create it dynamically
STATIC_DIR = "static"
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# 3. Mount the directory safely now that we know it exists
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 2. In-Memory Source of Truth
# When you have a new update, you will manually increment these numbers here.
LATEST_RELEASE = {
    "versionCode": 2,                           # Increment this for new updates
    "versionName": "1.1.0",
    "apkUrl": "http://127.0.0.1:8000/static/app-release.apk"  # Swap with your server's IP
}

# 3. Request Data Structure Validation
class UpdateCheckRequest(BaseModel):
    current_version_code: int

# 4. The Handshake Endpoint
@app.post("/api/check-update")
def check_update(request: UpdateCheckRequest):
    """
    Compares the mobile application's current version code with the 
    hardcoded server version code. Returns update instructions if necessary.
    """
    if LATEST_RELEASE["versionCode"] > request.current_version_code:
        return {
            "updateAvailable": True,
            "versionCode": LATEST_RELEASE["versionCode"],
            "versionName": LATEST_RELEASE["versionName"],
            "apkUrl": LATEST_RELEASE["apkUrl"]
        }
    
    return {
        "updateAvailable": False,
        "message": "Application is up to date."
    }