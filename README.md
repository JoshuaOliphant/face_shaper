# Face Shape Analyzer

Face Shape Analyzer is a web application that uses AI to analyze facial features and recommend hairstyles based on face shape. The application leverages Anthropic's Claude Vision API for accurate face shape detection and provides personalized hairstyle recommendations for both men and women.

## Features

- 📸 Upload and analyze face photos
- 🔍 AI-powered gender and face shape detection
- 💇‍♂️ Gender-specific face shape analysis
- 💇‍♀️ Personalized hairstyle recommendations
- 📊 Confidence scoring for analysis
- 🎯 Detailed facial characteristics breakdown
- ⚡ Real-time analysis with HTMX
- 📱 Responsive design with Tailwind CSS

## Face Shape Analysis

The application analyzes face shapes based on established criteria from professional sources:

### Men's Face Shapes
Our male face shape analysis criteria are based on the professional guidelines from [Goodman's Barber Lounge](https://goodmansbarberlounge.com/blog/mens-hairstyles-by-face-shape/), which identifies seven primary face shapes:

1. Oval Face Shape
2. Square Face Shape
3. Heart Face Shape
4. Round Face Shape
5. Triangle Face Shape
6. Oblong/Rectangle Face Shape
7. Diamond Face Shape

### Women's Face Shapes
Our female face shape analysis criteria are based on the comprehensive guide from [Headcurve](https://headcurve.com/hair/face-shapes/), which identifies nine distinct face shapes:

1. Round Face Shape
2. Oval Face Shape
3. Inverted Triangle Face Shape
4. Diamond Face Shape
5. Triangle Face Shape
6. Rectangle Face Shape
7. Square Face Shape
8. Heart Face Shape
9. Oblong Face Shape

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**:
  - HTMX for dynamic interactions
  - Tailwind CSS for styling
  - Minimal JavaScript
- **AI/ML**: Anthropic Claude Vision API
- **Templates**: Jinja2

## Prerequisites

- Python 3.10+
- Anthropic API key
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/face-shape-analyzer.git
cd face-shape-analyzer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

5. Create required directories:
```bash
mkdir -p app/static/css
mkdir -p app/static/js
mkdir -p app/templates/partials
```

## Project Structure

```
face_shape_analyzer/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── services/
│   │   ├── __init__.py
│   │   └── claude_service.py    # Claude Vision API integration
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css       # Custom styles
│   │   └── js/
│   ├── templates/
│   │   ├── base.html            # Base template
│   │   ├── index.html           # Main upload page
│   │   └── partials/
│   │       └── results.html     # Analysis results partial
├── requirements.txt
└── README.md
```

## Running the Application

1. Make sure your virtual environment is activated:
```bash
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Start the development server:
```bash
uvicorn app.main:app --reload
```

3. Open your browser and navigate to:
```
http://127.0.0.1:8000
```

## Usage

1. Visit the home page
2. Click the upload button or drag and drop a photo
3. Wait for the AI analysis to complete
4. View your:
   - Detected gender
   - Face shape analysis
   - Confidence score
   - Key characteristics
   - Personalized hairstyle recommendations

## API Endpoints

- `GET /`: Home page with upload interface
- `POST /analyze`: Face analysis endpoint
  - Accepts multipart/form-data with an image file
  - Returns analysis results in HTML partial

## Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Security Considerations

- File upload validation implemented
- Image size limits enforced (10MB max)
- API key protection through environment variables
- Input sanitization
- CORS policies implemented

## Limitations

- Requires clear, front-facing photos
- Good lighting recommended
- Face should not be obscured by accessories
- Maximum file size: 10MB
- Supported formats: JPG, PNG, GIF

## Acknowledgments

- [Goodman's Barber Lounge](https://goodmansbarberlounge.com/) for male face shape analysis criteria
- [Headcurve](https://headcurve.com/) for female face shape analysis criteria
- Anthropic for the Claude Vision API
- FastAPI team for the excellent framework
- HTMX team for simplified frontend interactions
- Tailwind CSS team for the styling framework

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
