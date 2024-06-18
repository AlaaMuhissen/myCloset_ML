import logging
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
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
async def recognize_clothes_and_colors(image_url: str = Form(...)):
    try:
        # Here you call your image processing function
        result = process_and_annotate_image(image_url)
        return JSONResponse(content=result)
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    

@app.get("/")
def sayHello():
    print("hello world")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
