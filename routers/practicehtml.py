from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/test-html")
async def test_html(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})
