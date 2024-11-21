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
            "settings": settings  # Also pass settings directly to the template
        }
    )

@app.post("/analyze")
async def analyze_face(request: Request, file: UploadFile = File(...)):
    """Analyze uploaded face image and return results."""
    try:
        # Read the image file
        image_bytes = await file.read()

        # Get analysis from Claude Vision API
        analysis_result = await claude_service.analyze_image(image_bytes)

        # Return the analysis results partial
        return templates.TemplateResponse(
            "partials/results.html",
            {
                "request": request,
                "settings": settings,
                "face_shape": analysis_result["face_shape"],
                "confidence": analysis_result["confidence"],
                "characteristics": analysis_result["characteristics"],
                "recommendations": analysis_result["recommendations"]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
