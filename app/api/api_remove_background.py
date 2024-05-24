from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Response, status
from PIL import Image
from rembg import remove
import io
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer
from utils import VerifyToken

app = FastAPI()
token_auth_scheme = HTTPBearer()

@app.put("/remove_background")
async def remove_background( file: UploadFile = File(...)):
    result = VerifyToken(token).verify()
    if not result.get("status"):
       return Response(status_code=status.HTTP_400_BAD_REQUEST)
    try:
        contents = await file.read()
        input_image = Image.open(io.BytesIO(contents))
        output_image = remove(input_image)
        output_bytes = io.BytesIO()
        output_image.save(output_bytes, format="PNG")
        output_bytes.seek(0)
        return StreamingResponse(output_bytes, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
