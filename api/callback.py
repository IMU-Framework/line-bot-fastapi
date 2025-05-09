from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = FastAPI()

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "your-token"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET", "your-secret"))

@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()

    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        print("簽名驗證失敗")
        return JSONResponse(content={"status": "invalid signature"}, status_code=400)
    except Exception as e:
        print("Webhook 執行錯誤：", str(e))

    return JSONResponse(content={"status": "ok"}, status_code=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    print("使用者傳來訊息：", text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"你說了：{text}")
    )
