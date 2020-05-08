import os

from mangum import Mangum
from starlette.templating import Jinja2Templates
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.routing import Route, WebSocketRoute


DATABASE_URL = os.environ["DATABASE_URL"]
WEBSOCKET_URL = os.environ["WEBSOCKET_URL"]


templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
)


class Homepage(HTTPEndpoint):
    async def get(self, request):
        template = "index.html"
        context = {"request": request, "WEBSOCKET_URL": WEBSOCKET_URL}
        return templates.TemplateResponse(template, context)


class Echo(WebSocketEndpoint):
    encoding = "text"

    async def on_receive(self, websocket, data):
        await websocket.send_text(f"Message text was: {data}")


routes = [Route("/", Homepage), WebSocketRoute("/", Echo)]

app = Starlette(routes=routes)


handler = Mangum(app, log_level="debug", dsn=DATABASE_URL)
