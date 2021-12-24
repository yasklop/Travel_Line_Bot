from Azure_service import *
from money import *

import json
# import flask related
from flask import Flask, request, abort
# import linebot related
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, AudioMessage,
    LocationSendMessage, ImageSendMessage, StickerSendMessage, ImageMessage, FlexSendMessage,FollowEvent,
    TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, ConfirmTemplate, PostbackEvent, messages
)

# create flask server
app = Flask(__name__)
line_bot_api = LineBotApi('GGrsvJkl66cRYrq9wPSzPdPyYBQmmO0m7JeqV5htxFz7tXpXtdq7RZMZ3Fb5jSsQUzmkaiWA8JBbHIQBEWi8mw4qsqqDbXvlUyYOxyt2EV5ofS1glEgE9SO60WnpkYI5q2DM7W/Sj06gYGjy2WXTLwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('996c48464bb00a1eaaba7743241484d0')

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    FlexMessage_index = json.load(open('index.json','r',encoding='utf-8'))
    line_bot_api.reply_message(event.reply_token, FlexSendMessage('index',FlexMessage_index))

    
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):

    name_img = 'test_img.jpg'
   
    message_content = line_bot_api.get_message_content(event.message.id)
    
    with open(name_img, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    

  
    text = text_img(name_img)
    
    print('Text in image:', text)
    messages=[]
    messages.append(TextSendMessage(text = text))
    messages.append(TextSendMessage(text = language_detection_example(client, text)))
    confirm_template_message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://www.50languages.com/template/img/58755931.jpg',
                    title='即時翻譯',
                    text='請選擇語言',
                    actions=[
                        PostbackAction(
                            label='繁體中文',
                            display_text='繁體中文',
                            data = f'{text}|zh-Hant'
                        ),
                        PostbackAction(
                            label='英文',
                            display_text='英文',
                            data = f'{text}|en'
                        ),
                        PostbackAction(
                            label='日文',
                            display_text='日文',
                            data = f'{text}|ja'
                        ),
                        MessageAction(
                            label='返回',
                            text='返回',
                        )
                    ]
                )
            )
    messages.append(confirm_template_message)
    line_bot_api.reply_message(event.reply_token, messages)

      


@handler.add(PostbackEvent)
def handle_postback(event):
    messages = []
    translate_text = event.postback.data
    translate_list = translate_text.split('|')
    #if str(translate_text) != "nothing":
    messages.append(TextSendMessage(text= translate_to(translate_list[0], translate_list[1])))
   # messages.append(buttons_template_message)
    line_bot_api.reply_message(event.reply_token, messages)
        



@handler.add(MessageEvent, message=TextMessage)
def handle_something(event):
    
    recrive_text=event.message.text

    FlexMessage_index = json.load(open('index.json','r',encoding='utf-8'))

    buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://img.technews.tw/wp-content/uploads/2020/12/08132944/female-tourists-travel-map-624x378.jpg',
                title='旅遊助手',
                text='請選擇您需要的服務',
                actions=[
                    MessageAction(
                        label='文字辨識與翻譯',
                        text='文字辨識與翻譯'
                    ),
                ]
            )
        )

    if '開始文字偵測' in recrive_text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = '請上傳照片，並耐心等候'))
    elif '開始匯率查詢' in recrive_text:
        FlexMessage = json.load(open('currency.json','r',encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('currency',FlexMessage))
    elif '返回' in recrive_text:
        messages = []
        messages.append(TextSendMessage(text = '感謝您使用此服務!'))
        #messages.append(StickerSendMessage(package_id='11538', sticker_id='51626533'))
        messages.append(FlexSendMessage('index',FlexMessage_index))
        line_bot_api.reply_message(event.reply_token, messages)
    elif '您選擇' in recrive_text:
        messages = []
        FlexMessage = json.load(open('calculate.json','r',encoding='utf-8'))
        l = recrive_text.split(" ")
        messages.append(TextSendMessage(text = f'目前 1 {l[1]} 等於 {currency_rate(l[1])} NTD'))
        messages.append(FlexSendMessage('calculate',FlexMessage))
        line_bot_api.reply_message(event.reply_token, messages)
    elif '=?' in recrive_text:
        l = recrive_text.split("=")
        l[1] = l[1][1:].upper()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = calculate(l[0], l[1], currency_rate(l[1]))))
        

    else:
        #line_bot_api.reply_message(event.reply_token, buttons_template_message)
        #FlexMessage_index = json.load(open('index.json','r',encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('index',FlexMessage_index))



# run app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5566)