from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.services.claude_service import ClaudeVisionService
from app.config import get_settings
import json

app = FastAPI()

# Setup static files and templates
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Initialize services
settings = get_settings()
claude_service = ClaudeVisionService(settings.anthropic_api_key)

# Add settings to template context
templates.env.globals["settings"] = settings

@app.get("/")
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "settings": settings
        }
    )

@app.post("/analyze")
async def analyze_face(request: Request, file: UploadFile = File(...)):
    """Analyze uploaded face image and return results."""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read the image file
        image_bytes = await file.read()

        if len(image_bytes) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File size too large. Maximum size is 10MB")

        # Get analysis from Claude Vision API
        analysis_result = await claude_service.analyze_image(image_bytes)

        if analysis_result.get("face_shape") == "error":
            raise HTTPException(
                status_code=400,
                detail=analysis_result["characteristics"][0] if analysis_result["characteristics"] else "Unknown error occurred"
            )

        # Return the analysis results partial
        return templates.TemplateResponse(
            "partials/results.html",
            {
                "request": request,
                "settings": settings,
                "gender": analysis_result["gender"],
                "face_shape": analysis_result["face_shape"],
                "confidence": analysis_result["confidence"],
                "characteristics": analysis_result["characteristics"],
                "recommendations": analysis_result["recommendations"]
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
