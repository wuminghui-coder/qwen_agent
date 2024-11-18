from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi import APIRouter

web_router = APIRouter()

async def generate_html_response(file_path:str):
    with open(file_path, 'r', encoding='utf-8') as file:
        return HTMLResponse(content=file.read(), status_code=200)
    
@web_router.get("/v1/index", response_class=HTMLResponse)
async def read_items():
    return await generate_html_response('templates/v1_index.html')

@web_router.get("/v2/index", response_class=HTMLResponse)
async def read_items():
    return await generate_html_response('templates/v2_index.html')