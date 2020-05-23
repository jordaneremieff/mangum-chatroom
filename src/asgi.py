import os
import uuid

from mangum import Mangum

from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint


BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
WEBSOCKET_DSN = os.environ["WEBSOCKET_DSN"]
# WEBSOCKET_URL = "ws://localhost:3001"
# API_GATEWAY_ENDPOINT_URL = "http://localhost:3001"
WEBSOCKET_URL = os.environ["WEBSOCKET_URL"]
API_GATEWAY_ENDPOINT_URL = None


static = StaticFiles(directory=STATIC_DIR)
templates = Jinja2Templates(directory=TEMPLATE_DIR)


class Chatroom(HTTPEndpoint):
    async def get(self, request):
        context = {"request": request}

        if "channel_name" not in request.path_params:
            template = "home.html"
        else:
            template = "channel.html"
            context["websocket_url"] = WEBSOCKET_URL
            context["channel_name"] = request.path_params["channel_name"]
            context["user_id"] = str(uuid.uuid4())[:8]

        return templates.TemplateResponse(template, context)


class ChatroomWebSocket(WebSocketEndpoint):

    encoding = "json"

    async def on_receive(self, websocket, message) -> None:
        message_type = message["type"].replace(".", "_")
        message_handler = getattr(self, message_type, None)
        await message_handler(websocket, message)

    async def on_subscribe(self, websocket, message) -> None:
        channel = message["channel"]
        await websocket._send(
            {"type": "websocket.broadcast.subscribe", "channel": channel}
        )

    async def on_publish(self, websocket, message) -> dict:
        channel = message["channel"]
        body = message["body"]
        await websocket._send(
            {"type": "websocket.broadcast.publish", "channel": channel, "body": body}
        )


app = Starlette(
    debug=True,
    routes=[
        Route("/chat", Chatroom, name="chat_home"),
        Route("/chat/{channel_name}", Chatroom, name="chat_channel"),
        WebSocketRoute("/", ChatroomWebSocket, name="chat_ws"),
    ],
)

handler = Mangum(
    app,
    log_level="debug",
    lifespan="off",
    api_gateway_endpoint_url=API_GATEWAY_ENDPOINT_URL,
    dsn=WEBSOCKET_DSN,
)
