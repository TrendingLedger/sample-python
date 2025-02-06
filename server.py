import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from http import HTTPStatus

# Create FastAPI app instance
app = FastAPI()

# Define the GET endpoint
@app.get("/", response_class=HTMLResponse)
def read_root():
    msg = f'Hello WORLD CHANGES! you requested {str(app)}'  # Similar to your original message
    return HTMLResponse(content=msg, status_code=HTTPStatus.OK)

# Set the port from the environment variable, defaulting to 80
port = int(os.getenv('PORT', 80))

# Run the app using uvicorn (for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

