


import requests
import telebot

# أدخل التوكن الخاص بالبوت هنا
TOKEN = '7310124122:AAFymXsZVrn1Up10_gS7O-pNMn7Mtjl4F7k'
bot = telebot.TeleBot(TOKEN)

# دالة لبدء المحادثة
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أدخل رقم الهاتف :")

# دالة لاستقبال رقم الهاتف من المستخدم
@bot.message_handler(func=lambda message: True)
def get_number(message):
    num = message.text
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3',
    }

    data = {
        'client_id': 'ibiza-app',
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }

    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)
    
    if 'ROOGY' in response.text:
        bot.reply_to(message, 'تم إرسال الكود، أدخل الكود :')
        bot.register_next_step_handler(message, get_otp, num)  # انتظار الكود
    else:
        bot.reply_to(message, 'فشل في إرسال الكود، حاول مرة أخرى.')

# دالة لاستقبال الكود OTP من المستخدم
def get_otp(message, num):
    otp = message.text
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp',
    }

    data = {
        'client_id': 'ibiza-app',
        'otp': otp,
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }

    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)
    
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        bot.reply_to(message, 'تم التحقق بنجاح!')
        send_internet_requests(message, access_token)
    else:
        bot.reply_to(message, 'فشل في التحقق من الكود.')

# دالة لإرسال طلب الانترنت
def send_internet_requests(message, access_token):
    url = 'https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/mgm/info/apply'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'language': 'AR',
        'request-id': 'ef69f4c6-2ead-4b93-95df-106ef37feefd',
        'flavour-type': 'gms',
        'Content-Type': 'application/json'
    }

    payload = {
        "mgmValue": "ABC"
    }

    while True:
        response = requests.post(url, headers=headers, json=payload)
        if 'EU1002' in response.text:
            bot.reply_to(message, 'تم إرسال انترنت')
        else:
            bot.reply_to(message, 'لديك انترنت كافٍ، عندما تنتهي يمكنك المحاولة مرة أخرى.')
        break

# تشغيل البوت
bot.polling()
