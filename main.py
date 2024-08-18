import logging
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from app.api.recognize_clothe_and_color import process_and_annotate_image
from app.api.generate_outfits import final_outfits
import json
from fastapi import Request
from typing import Dict


app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Pydantic model for the request body
class ImageRequest(BaseModel):
    image_url: str

@app.post("/recognize-clothes-and-colors/")
async def recognize_clothes_and_colors(request: ImageRequest):
    try:
        # Extract image_url from the request body
        image_url = request.image_url
        # Here you call your image processing function
        result = process_and_annotate_image(image_url)
        return JSONResponse(content=result)
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    
@app.post("/generate-outfit/")
async def generate_outfits(data: Dict = Body(...)):
    try:
        
        result = final_outfits(data)
        return JSONResponse(content=result)

    except Exception as e:
        logging.error(f"Error in final_outfits_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def say_hello():
    logging.info("Hello world")
    return {"message": "Hello world"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
