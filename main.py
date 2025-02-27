from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")

app = FastAPI()

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return api_key

class TextInput(BaseModel):
    text: str

@app.get("/", dependencies=[Depends(verify_api_key)])
def read_root():
    return {"Hello": "World"}

@app.post("/count-words", dependencies=[Depends(verify_api_key)])
def count_characters(input_data: TextInput):
    return {"character_count": len(input_data.text)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
