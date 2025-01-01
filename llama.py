import boto3
import json
from constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def llama_response(
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.5,
        top_p: float = 0.9,
        model_id: str = "us.meta.llama3-1-8b-instruct-v1:0",
        access_key_id: str = AWS_ACCESS_KEY_ID,
        secret_access_key: str = AWS_SECRET_ACCESS_KEY,
    ):
    bedrock_client=boto3.client(
        service_name='bedrock-runtime',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )
    payload={
        "prompt":prompt,
        "max_gen_len":max_tokens,
        "temperature":temperature,
        "top_p":top_p
    }
    body=json.dumps(payload)
    response=bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    response_body=json.loads(response.get("body").read())
    return response_body['generation']
