from gtts import gTTS
import telebot
import qrcode
from khayyam import JalaliDatetime
from random import randint



bot = telebot.TeleBot("secret")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, " خوش اومدی به بات " + message.from_user.first_name+ "   عزیز اگه میخوای قابلیت های این بات رو بدونی از /help کمک بگیر.")
@bot.message_handler(commands=['qrcode'])
def send_Qrcode(message):
    Text=bot.send_message(message.chat.id,"متن رو تایپ کن")
    bot.register_next_step_handler(Text,make_qrcode)
def make_qrcode(message):
    qc=qrcode.make(message.text)
    qc.save("qc_bot.png")
    pec=open("qc_bot.png","rb")
    bot.send_photo(message.chat.id,pec)

@bot.message_handler(commands=['argmax'])

def maximum_index(message):

    array = bot.send_message(message.chat.id , " آرایه رو وارد کن مثل 1,45,68,74 ")

    bot.register_next_step_handler(array , index_searching)

def index_searching(array):

    temp = list(map(int, array.text.split(',')))
    
    ind = temp.index(max(temp))

    bot.send_message(array.chat.id , (ind+1))
@bot.message_handler(commands=['voice'])
def con_text2voi(message):
    text=bot.send_message(message.chat.id,' لطفا متن رو به صورت انگلیسی وارد کن  ')
    bot.register_next_step_handler(text,text2voice)   
def text2voice(message):
    voice=gTTS(text=message.text,lang="en",slow=False)
    voice.save("voice.ogg")
    voice_sent=open("voice.ogg",'rb')
    bot.send_voice(message.chat.id,voice_sent)
@bot.message_handler(commands=['age'])
def age_command(message):
    msg = bot.reply_to(message, "تاریخ تولدت رو وارد کن مثل 1370/9/14")
    bot.register_next_step_handler(msg, convert_date)


def convert_date(message):
    chat_id = message.chat.id
    try:
        text = message.text

        year, month, day = text.split('/')
        age = JalaliDatetime.now().year - JalaliDatetime(year, month, day).year
        bot.send_message(chat_id, str(age))
    except Exception as e:
        bot.send_message(chat_id, 'خطا دوباره تلاش کن!')
@bot.message_handler(commands=['max'])
def Max_handler(message):
    text_user=bot.send_message(message.chat.id,"   آرایه رو تایپ کن مثل 45,12,24,16   ")
    bot.register_next_step_handler(text_user,Max)
def Max(message):
    try:
        array=list(map(int,message.text.split(",")))
        bot.reply_to(message=message,text="بیشترین مقدار برابر است با: "+str(max(array)))
    except:
        bot.reply_to(message=message,text="  خطا دوباره تلاش کن!")
@bot.message_handler(commands=['game'])
def game(message):

    global rand

    rand  = randint(0,20)

    inp = bot.send_message(message.chat.id , 'خوش اومدی یک عدد بین 0و20 حدس بزن')

    bot.register_next_step_handler(inp , game_guess)


def game_guess(inp):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)

    btn_new = telebot.types.KeyboardButton('بازی جدید')
    markup.add(btn_new)
    
    if inp.text == 'بازی جدید':
        inp = bot.send_message(inp.chat.id, ' یک عدد بگو دوباره:',reply_markup=markup)
        global rand

        rand = randint(0,20)

        bot.register_next_step_handler(inp, game_guess)
  
        
    else:
        if int(inp.text) > rand:
            inp = bot.send_message(inp.chat.id , 'برو پایین تر! ' ,reply_markup=markup)

            bot.register_next_step_handler(inp , game_guess)
        elif int(inp.text) < rand:
            inp = bot.send_message(inp.chat.id , 'برو بالاتر! ' ,reply_markup=markup)

            bot.register_next_step_handler(inp , game_guess)
        else:
            markup = telebot.types.ReplyKeyboardRemove(selective=True)
            bot.send_message(inp.chat.id , 'احسنت!' ,reply_markup=markup)
@bot.message_handler(commands=['help'])

def help(message):

    text = bot.send_message(message.chat.id, """
    /start:سلام و خوش آمد گویی به کاربر
    /qrcode:یک رشته از کاربر می گیرد و کیو آر کد آن را تولید می کند
    /argmax:اندیس بزرگترین مقدار آرایه را چاپ می کند
    /voice:یک جمله از کاربر دریافت می کند و صدای آن را تولید می کند   
    /age:تاریخ تولد را به صورت هجری شمسی دریافت میکند و سن کاربر را می گوید
    /max:یک آرایه از کاربر می گیرد و بزرگترین مقدار را چاپ می نماید
    /game:بازی حدس عدد را اجرا می کند
    /help:توضیحات بالا""")

            
            



bot.infinity_polling()