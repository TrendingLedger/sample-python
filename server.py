import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from http import HTTPStatus

app = FastAPI()

SECRET_CODE = "98765123450"  # Secret code to validate

@app.get("/{path_param}", response_class=HTMLResponse)
def read_item(path_param: str, code: str = None):
    # Check if the provided code is valid
    if code == SECRET_CODE:
        msg = f'Hello WORLD CHANGES! You requested the path: {path_param}'
        return HTMLResponse(content=msg, status_code=HTTPStatus.OK)
    else:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="nothing much")


# Set the port from the environment variable, defaulting to 80
port = int(os.getenv('PORT', 80))

# Run the app using uvicorn (for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

