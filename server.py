from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import google.generativeai as genai
from http import HTTPStatus
from pydantic import BaseModel

# Create FastAPI app instance
app = FastAPI()

# Set up CORS middleware
origins = [
    "*",  # Allow only this domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers, including Content-Type
)

# Set up the API with Gemini API and your secret code validation
SECRET_CODE = "98765123450"
gemini_api_key = os.getenv("GEMINIAI_API_KEY")
genai.configure(api_key=gemini_api_key)

class UserRequest(BaseModel):
    code: str
    user_input: str

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

@app.options("/process_request/")
async def options():
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"message": "CORS preflight request successful"}
    )

@app.post("/process_request/")
async def process_request(request: UserRequest):
    # Validate the code
    """ if request.code != SECRET_CODE:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid secret code") """
    
    # Start chat with the AI model
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [request.user_input],
            }
        ]
    )

    response = chat_session.send_message(request.user_input)
    return {"message": response.text}

# Set port and run app
port = int(os.getenv('PORT', 80))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)


