from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from stablediffusion import stablediffusion_response
from claude import claude_response
from llama import llama_response
from enum import Enum
from constants import IMAGES_DIR

bedrock_models_router = APIRouter()

class BedrockModels(str, Enum):
    STABLE_DIFFUSION = "stable-diffusion"
    CLAUDE = "claude"
    LLAMA = "llama"


@bedrock_models_router.post("/generate-response")
async def get_bedrock_model_response(
    prompt: str = Query(..., description="The text prompt for bedrock models"),
    model: BedrockModels = Query(..., description="The model to use for bedrock models"),
    model_id: str = Query(..., description="The model id to use for bedrock models")
):
    try:
        if model == BedrockModels.STABLE_DIFFUSION:
            # Generate image
            image_bytes = stablediffusion_response(
                prompt=prompt,
                model_id=model_id
            )

            # Create the images directory if it doesn't exist
            IMAGES_DIR.mkdir(parents=True, exist_ok=True)

            # Save image with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_{timestamp}.jpg"
            save_path = IMAGES_DIR / filename
            save_path.write_bytes(image_bytes)

            # Generate URLs
            view_url = f"{IMAGES_DIR.resolve()}\{filename}"

            return JSONResponse({
                "message": "Image generated successfully",
                "prompt": prompt,
                "view_url": view_url,
            })
        elif model == BedrockModels.CLAUDE:
            response = claude_response(prompt=prompt, model_id=model_id)
            return JSONResponse({
                "message": "Claude response generated successfully",
                "prompt": prompt,
                "response": response,
            })
        elif model == BedrockModels.LLAMA:
            response = llama_response(prompt=prompt, model_id=model_id)
            return JSONResponse({
                "message": "Llama response generated successfully",
                "prompt": prompt,
                "response": response,
            })
    except Exception as e:
        return JSONResponse({
            "message": "Error generating response",
            "error": str(e)
        }, status_code=500)
