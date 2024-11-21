from anthropic import Anthropic
import base64
import json

class ClaudeVisionService:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.face_shapes_prompt = """
        You are a professional hairstylist and face shape analyzer. Analyze the face shape in this image and determine if the person appears to be male or female. Then analyze their face shape based on these characteristics:

        MALE FACE SHAPES:
        1. Oval Face Shape:
        - Longer than wide across cheekbones and forehead
        - Forehead slightly wider than jawline
        - Generally rounded jawline

        2. Square Face Shape:
        - Similar measurements in height and width
        - Sharp, angular curves rather than soft edges

        3. Heart Face Shape:
        - Forehead dramatically wider than jawline
        - Jawline may be pointy, angular, or round

        4. Round Face Shape:
        - Width of cheekbones equals face length
        - Soft, curved chin and hairline

        5. Triangle Face Shape:
        - Wider jawline than cheekbones
        - Narrowest at forehead

        6. Oblong/Rectangle Face Shape:
        - Longer than wide
        - Similar width at forehead, cheekbones, and jawline

        7. Diamond Face Shape:
        - Long face with angular features
        - Cheekbones are widest part
        - Narrow forehead and jawline

        FEMALE FACE SHAPES:
        1. Round Face Shape:
        - Widest at cheeks
        - Rounded jawline
        - Similar face width and length

        2. Oval Face Shape:
        - Longer than wide
        - Forehead slightly wider than jaw
        - Gently rounded jawline

        3. Inverted Triangle:
        - Wider upper face
        - Narrower jaw and chin
        - Flat top of head

        4. Diamond Face Shape:
        - Widest at cheekbones
        - Narrow forehead and jawline
        - Angular features

        5. Triangle Face Shape:
        - Wide jawline
        - Narrow forehead
        - Gets progressively wider toward bottom

        6. Rectangle Face Shape:
        - Long face with similar width
        - Square jawline
        - High forehead

        7. Square Face Shape:
        - Similar width and height
        - Strong, angular jawline
        - Minimal curves

        8. Heart Face Shape:
        - Wide forehead and cheekbones
        - Narrow, pointed chin
        - Often has widow's peak

        9. Oblong Face Shape:
        - Long and narrow
        - Similar width throughout
        - Tall forehead

        Analyze the face in the image and provide a JSON response in the following format:
        {
            "gender": "male or female",
            "face_shape": "name of face shape",
            "confidence": "float between 0 and 1",
            "characteristics": ["list of identified characteristics that led to this conclusion"],
            "recommendations": ["list of 3-4 recommended hairstyles for this face shape"]
        }

        Important rules:
        1. Only return valid JSON - no other text
        2. Be specific about the characteristics you observe
        3. Match hairstyle recommendations to those appropriate for the face shape and gender
        4. If you cannot clearly see the face or determine the shape, return a confidence of 0.1 and mention this in characteristics
        5. Base recommendations on traditional hairstyles for that face shape while considering modern trends
        """

    async def analyze_image(self, image_bytes: bytes) -> dict:
        """
        Analyze an image using Claude Vision API and return face shape analysis.

        Args:
            image_bytes (bytes): The uploaded image in bytes

        Returns:
            dict: Analysis results including gender, face shape, confidence, characteristics, and recommendations
        """
        try:
            base64_image = base64.b64encode(image_bytes).decode('utf-8')

            response = self.client.messages.create(  # Not async
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.face_shapes_prompt
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image
                            }
                        }
                    ]
                }]
            )

            # Extract the JSON response from Claude
            try:
                result = json.loads(response.content[0].text)
                return result
            except (json.JSONDecodeError, AttributeError, IndexError):
                # Fallback response if Claude doesn't return valid JSON
                return {
                    "gender": "unknown",
                    "face_shape": "unknown",
                    "confidence": 0.1,
                    "characteristics": ["Unable to analyze face shape from the provided image"],
                    "recommendations": [
                        "Please provide a clear, front-facing photo",
                        "Ensure good lighting",
                        "Remove any accessories blocking face shape"
                    ]
                }

        except Exception as e:
            # Handle any API or processing errors
            return {
                "gender": "error",
                "face_shape": "error",
                "confidence": 0.0,
                "characteristics": [f"Error analyzing image: {str(e)}"],
                "recommendations": [
                    "Please try uploading a different photo",
                    "Ensure the image is in a supported format (JPG, PNG)",
                    "Check that the file size is not too large"
                ]
            }
