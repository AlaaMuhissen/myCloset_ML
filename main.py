import sys
import os
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.api.recognize_clothe_and_color import process_and_annotate_image  


app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/recognize-clothes-and-colors/")
async def recognize_clothes_and_colors(file: UploadFile = File(...)):
    try:
        input_image_bytes = await file.read()
        result = process_and_annotate_image(input_image_bytes)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))