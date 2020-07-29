from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, QuickReplyButton, MessageAction, QuickReply,
    TextSendMessage, LocationMessage, TemplateSendMessage, CarouselTemplate,
    CarouselColumn, URITemplateAction)
import os
from news import News
from weather import Weather
import random



app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # QuickMenu options
    optionList = ['ニュース']
    infoItems = [QuickReplyButton(action=MessageAction(
        label=f"{option}", text=f"{option}")) for option in optionList]
    
    # News columns
    if "ニュース" in event.message.text:
        # ニュースの送付
        js = News("jp", "general")
        newsColumns = [
            CarouselColumn(
                thumbnail_image_url=articles["urlToImage"],
                title=articles["title"][:40],  # titleが40文字までの規制されているので
                text=articles["source"]["name"],
                actions=[
                    URITemplateAction(
                        label="Check",
                        uri=articles["url"]
                    )
                ]
            )
            for articles in js["articles"]
        ]
        news_reply = TemplateSendMessage(
                        alt_text='ニュース送ったの',
                        template=CarouselTemplate(columns=newsColumns)
                     )
        
        # 送付後のリアクション
        random_news_reply = ["どうぞだぬ", "だぬ", "ぬてん", "ちょっと考えるの", "ぬう〜ん", "絶対読むの”"
                             "しっかり読むの", "えらいの", "すてきだぬ", "わくわく", "難しいだぬ"]
        first_reply = TextSendMessage(text=random.choice(random_news_reply))

        line_bot_api.reply_message(event.reply_token,
                                   messages=[news_reply, first_reply])
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text+"だぬ"))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
