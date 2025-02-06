import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from http import HTTPStatus

# Access the environment variable
gemini_api_key = os.getenv("GEMINIAI_API_KEY")

# Configure Google Generative AI with your API key
import google.generativeai as genai
genai.configure(api_key=gemini_api_key)

# FastAPI app instance
app = FastAPI()

# Set up the secret code for validation
SECRET_CODE = "98765123450"

# Define the input model for the user request
class UserRequest(BaseModel):
    code: str
    user_input: str

# Set up the model configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="user is new to crypto. welcoming language. response is in json format of the message for the user and the relevant data gathered.",
)

@app.post("/process_request/")
async def process_request(request: UserRequest):
    # Validate the code
    if request.code != SECRET_CODE:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid secret code")
    
    # Start chat with the AI model
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [request.user_input],
            }
        ]
    )

    # Get the AI response
    response = chat_session.send_message(request.user_input)
    return {"message": response.text}

# Set the port from the environment variable, defaulting to 80
port = int(os.getenv('PORT', 80))

# Run the app using uvicorn (for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

