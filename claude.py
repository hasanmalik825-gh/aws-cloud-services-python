import boto3
import json
from constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def claude_response(
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.5,
        top_p: float = 0.9,
        model_id: str = "anthropic.claude-3-haiku-20240307-v1:0",
        access_key_id: str = AWS_ACCESS_KEY_ID,
        secret_access_key: str = AWS_SECRET_ACCESS_KEY,
    ) -> str:
    # Initialize Bedrock client
    bedrock_client = boto3.client(
        service_name='bedrock-runtime',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )
    
    # Format the message in the required structure
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]
    
    # Construct the request body
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "messages": messages
    }
    
    # Convert request body to JSON string
    body = json.dumps(request_body)
    
    # Make the API call
    response = bedrock_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    # Parse and return the response
    response_body = json.loads(response.get("body").read())
    response_text = response_body['content'][0]['text']
    return response_text