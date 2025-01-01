import boto3
import json
import base64
from constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

def stablediffusion_response(
        prompt: str,
        cfg_scale: int = 10,
        seed: int = 0,
        steps: int = 50,
        width: int = 512,
        height: int = 512,
        model_id: str = "stability.stable-diffusion-xl-v1",
        access_key_id: str = AWS_ACCESS_KEY_ID,
        secret_access_key: str = AWS_SECRET_ACCESS_KEY,
    ):

    prompt_template=[{"text":prompt,"weight":1}]
    bedrock = boto3.client(
        service_name="bedrock-runtime",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )
    payload = {
        "text_prompts":prompt_template,
        "cfg_scale": cfg_scale,
        "seed": seed,
        "steps":steps,
        "width":width,
        "height":height

    }

    body = json.dumps(payload)
    model_id = "stability.stable-diffusion-xl-v0"
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    print(response_body)
    artifact = response_body.get("artifacts")[0]
    image_encoded = artifact.get("base64").encode("utf-8")
    image_bytes = base64.b64decode(image_encoded)
    return image_bytes