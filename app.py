from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models.messages import (
    TextMessage,
    ImageMessage,
    VideoMessage,
    AudioMessage,
    LocationMessage,
    StickerMessage,
    FileMessage
)

from linebot.models import (
    MessageEvent, JoinEvent,
    LeaveEvent, TextMessage,
    TextSendMessage,ImageSendMessage,
    VideoSendMessage,StickerSendMessage,
    TemplateSendMessage,ButtonsTemplate,
    PostbackAction,URIAction,MessageAction
)

import numpy as np

app = Flask(__name__)
# 負責 與 Line 本身的API做溝通
line_bot_api = LineBotApi('zSLBHGz6m7JeIjOo3hiDupS0GtGxb0Nxa1mUVy0rolTQSM7IsN2Z2sBrrTboPt7Jofe9WXeYQ2DYBJYTkhRNAdaaMFRAHh2w/wUJtuJCIbrcKPDHdEOE1ic5Kp9Aw4NkznFH3iUr9YqgCOOTEaPeqAdB04t89/1O/w1cDnyilFU=')
# 負責 處理送過來的資料
handler = WebhookHandler('b02bf42ce4101e111c08c5bb08212f8b')

import requests
from bs4 import BeautifulSoup
def fetch(url):
    response = requests.get(url)
    response = requests.get(url, cookies={'over18': '1'})  # 一直向 server 回答滿 18 歲了 !
    return response

def getphoto():
    url = 'https://www.ptt.cc/bbs/Beauty/index.html'
    addr = []
    for round in range(2):
        res = fetch(url)#抓取網站中的原始碼
        soup = BeautifulSoup(res.text,'html.parser')
        articles = soup.select('div.title a')#從<div>中抓取標題的連結
        paging = soup.select('div.btn-group-paging a')#找到上一頁(next_url)在哪
        next_url = 'https://www.ptt.cc' + paging[1]['href']#真正的上一頁的網址
        url = next_url
        print("round ",round)
        for article in articles:
            if '[正妹]' in article.text:#只抓特定標籤
                addr.append('https://www.ptt.cc'+article['href'])
                #print(article['href'],article.text)
    print('已抓取文章網址')

    addr_img = []#抓取圖片網址
    for i in addr:
       url = i
       res = fetch(url)
       soup = BeautifulSoup(res.text,"lxml")
       for img in soup.select('div a'):
           if 'jpg' in img['href']:#抓取含有jpg的字串
               addr_img.append(img['href'])
               #print(img['href'])
    x = np.random.randint(0,5)
    return addr_img[x]

@app.route("/")
def home():
    return 'home OK'

# 監聽所有來自 /callback 的 Post Request
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


# 處理訊息
@handler.add(JoinEvent)
def handle_join(event):
    newcoming_text = "已經沒事了，因為我─來─了！"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )
    print("JoinEvent =", JoinEvent)

@handler.add(LeaveEvent)
def handle_leave(event):
    print("leave Event =", event)
    print("我被踢掉了QQ 相關資訊", event.source)
    
@handler.add(MessageEvent,message=TextMessage)
def handle_text(event):
    
    user_input = event.message.text
    if user_input == "你好":
        reply = ["我很好","你好啊！","你也好嗎？","好還要更好"]
        line_bot_api.reply_message(event.reply_token,TextSendMessage(np.random.choice(reply)))#隨機從reply回一句話
    elif user_input == "正妹":           
        img_url = getphoto()
        image_message = ImageSendMessage(original_content_url= img_url, #真實圖片
                                         preview_image_url= img_url) #預覽圖
        line_bot_api.reply_message(event.reply_token,image_message)    
        
    elif user_input == "你是誰":
        reply = ["我是:\n","皇甫承佑！","那個永不放棄的男人。"]
        line_bot_api.reply_message(event.reply_token,TextSendMessage(np.random.choice(reply)))#隨機從reply回一句話

    elif user_input == "璇璇" :
        reply = ["貼心的朋友","音樂才女","資管達人","寶可夢大師"]
        line_bot_api.reply_message(event.reply_token,TextSendMessage(np.random.choice(reply,p=[0.249, 0.249, 0.249, 0.249, 0.004])))#隨機從reply回一句話

    elif user_input in ["照片","相片","圖片"]:
        img_url = 'https://i.imgur.com/QjJcnXr.jpg'
        image_message = ImageSendMessage(original_content_url= img_url, #真實圖片
                                         preview_image_url= img_url) #預覽圖
        line_bot_api.reply_message(event.reply_token,image_message)

    elif user_input in ["錡哥"]:
        img_url = "https://scontent-tpe1-1.xx.fbcdn.net/v/t1.0-9/1045129_10200360679116763_110292631_n.jpg?_nc_cat=101&_nc_oc=AQn_CDD_3OAMAWTLdaTwopmuGPqf2Rl-xOmeu6hXbYrGvSJMkePW9VbBbnlh4Fz-fXg&_nc_ht=scontent-tpe1-1.xx&oh=092a83f5de88b7b3a1e1c0ba2d609981&oe=5E1DF4AD"
        image_message = ImageSendMessage(original_content_url= img_url, #真實圖片
                                         preview_image_url= img_url) #預覽圖
        line_bot_api.reply_message(event.reply_token,image_message)

    elif user_input == "影片":
        img_url = "https://upload.wikimedia.org/wikipedia/zh/thumb/6/6b/NCTU_emblem.svg/1200px-NCTU_emblem.svg.png"
        #video_message = VideoSendMessage(original_content_url= "D:\Google 雲端硬碟\影片\片頭新的.mp4",preview_image_url= img_url)
        line_bot_api.reply_message(event.reply_token,TextSendMessage("https://www.youtube.com/watch?v=zTJhb-IqKlc"))

    elif user_input in ["掰掰","88","bye","掰","ㄅㄅ"]:
        sticker_message = StickerSendMessage(
                package_id='11538',
                sticker_id='51626533')
        line_bot_api.reply_message(event.reply_token,sticker_message)

    elif user_input == "晚安" :
        reply = ["晚ㄤㄤ"]
        line_bot_api.reply_message(event.reply_token,TextSendMessage(np.random.choice(reply)))#隨機從reply回一句話

    elif user_input == '按鈕':
        buttons_template = ButtonsTemplate(
            title='功能列表', text='請點選你要的服務', actions=[
                URIAction(label='最偉大的大學', uri='https://www.nctu.edu.tw'),
                PostbackAction(label='成語接龍', data='ping', text='成語接龍'),
                PostbackAction(label='生氣的人', data='ping', text='吵架'),
                MessageAction(label='自我介紹', text='你是誰')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif user_input == "吵架":
        line_bot_api.reply_message(event.reply_token,TextSendMessage("(#‵)3′)▂▂▂▃▄▅～～～嗡嗡嗡嗡嗡"))

    elif "好餓" in user_input:
        reply = ["走！去吃麥當勞","今天很冷，吃個火鍋暖暖身體吧！","我泡好兩杯熱可可了，你要的話，兩杯都給你。","三層山今天的口味很特別哦！"]
        line_bot_api.reply_message(event.reply_token,TextSendMessage(np.random.choice(reply)))#隨機從reply回一句話

    elif user_input == "說笑話" :
        reply = ["笑話","你就是個笑話","中山國中在中國山中","垃圾場有4個垃圾，而你去就4個垃圾","我沒梗了"]
        line_bot_api.reply_message(event.reply_token,TextSendMessage(np.random.choice(reply,p=[0.249, 0.249, 0.249, 0.249, 0.004])))#隨機從reply回一句話

    elif user_input in ["合照"]:
        img_url = "https://scontent-tpe1-1.xx.fbcdn.net/v/t1.0-9/70062123_2261071120682191_8503349855198904320_o.jpg?_nc_cat=102&_nc_eui2=AeFKKVAV1mNxx0zh3w02YVNIry8l_74c220JGLJ7heCY-LPh3ofB96evMnAO0ofNRWZmCzIM3rWzCNUU9DE00B4kpmagV4swaECYqgPumE3FKQ&_nc_oc=AQlp3Ivq_AakrUB1PoO9SnhHUDbGlNOk50WXVAbky5ASAHe80sF2nyVAVVFMkU17EKk&_nc_ht=scontent-tpe1-1.xx&oh=64c982d5be13eb9889df50b0533c88a3&oe=5E1ED952"
        image_message = ImageSendMessage(original_content_url= img_url, #真實圖片
                                         preview_image_url= img_url) #預覽圖
        line_bot_api.reply_message(event.reply_token,image_message)
  
    elif user_input == '約會推薦':
        buttons_template = ButtonsTemplate(
            title='妳要去哪兒?', text='只能選一個哦!', actions=[
                URIAction(label='交通大學', uri='https://www.nctu.edu.tw'),
                URIAction(label='兒童新樂園', uri='https://www.tcap.taipei/Content_List.aspx?n=CD0DAF4E7055A7E8'),
                PostbackAction(label='夜景咖啡廳', data='ping', text='看夜景'),
                MessageAction(label='宅在家', text='今天不想出門')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif user_input in ["哭哭","QQ",'qq',"嗚嗚",'QAQ']  :
        line_bot_api.reply_message(event.reply_token,TextSendMessage("拍拍，別難過，我一直都在:D")) 

    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage("你是說"+user_input+"嗎？\n我不知道啦 哈哈"))
    

# 處理訊息
@handler.add(MessageEvent,message=StickerMessage)
def handle_sticker(event):
#    id	        String	MessageID
#    type	    String	sticker
#    packageId	String	PackageID
#    stickerId	String	StickerID
    if event.message.sticker_id == "52002742" :
        sticker_message = StickerSendMessage(
                package_id='11537',
                sticker_id='52002743')
        line_bot_api.reply_message(event.reply_token,sticker_message)
    elif event.message.sticker_id == "52002743" :
        sticker_message = StickerSendMessage(
                package_id='11537',
                sticker_id='52002742')
        line_bot_api.reply_message(event.reply_token,sticker_message)
    else:
        ID = np.random.choice(list(range(51626494,51626534)))
        sticker_message = StickerSendMessage(
                package_id='11538',
                sticker_id=str(ID))
        line_bot_api.reply_message(event.reply_token,sticker_message)
        #line_bot_api.reply_message(event.reply_token,TextSendMessage("你的貼圖真好看，哪裡買的？"))

@handler.add(MessageEvent,message=ImageMessage)
def handle_image(event):
#id	String	
#type	String	
#contentProvider.originalContentUrl	照片的原址網址
#contentProvider.previewImageUrl	照片預覽的網址
    if event.message.type == "image" :
        line_bot_api.reply_message(event.reply_token,TextSendMessage("這張圖真有趣。"))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage("我不明白你的意思QAQ"))
        
if __name__ == "__main__":
    app.run()
    
