########################################################################
#  _   _                   _      _   _              ____        _     #
# | \ | |                 | |    | | | |            |  _ \      | |    #
# |  \| | _____      _____| | ___| |_| |_ ___ _ __  | |_) | ___ | |_   # 
# | . ` |/ _ \ \ /\ / / __| |/ _ \ __| __/ _ \ '__| |  _ < / _ \| __|  #
# | |\  |  __/\ V  V /\__ \ |  __/ |_| ||  __/ |    | |_) | (_) | |_   #
# |_| \_|\___| \_/\_/ |___/_|\___|\__|\__\___|_|    |____/ \___/ \__|  #
#                                                                      #
########################################################################                                                                      #


# Feito por Gabriel Dantas
# https://github.com/gdma2004

# Bot para enviar notícias da newsletter pelo telegram



import easyimap as e
import telebot, schedule, time

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    
    nome = ('{} {}'.format(message.chat.first_name, message.chat.last_name))
    id = message.chat.id

    if message.chat.id != 1469532071:
        bot.send_message(1469532071, 'Usuário: {}\nID: {}'.format(nome,id))
    else:
        pass

    bot.send_message(message.chat.id, 'Bot iniciado. A partir de agora você receberá às 13:00 as novas notícias da Newsletter.')
    password = 'sigilo'
    user = 'sigilo'
    server = e.connect('imap.gmail.com' , user , password)

    email = server.mail(server.listids()[0])
    sender = email.from_addr
    
    def enviar():
        if sender == 'Filipe Deschamps Newsletter<newsletter@filipedeschamps.com.br>':
            corpo_cru = email.body
            corpo = corpo_cru.replace('Rua Antônio da Veiga, 495, Blumenau, SC, 89012-500' , '')
            bot.send_message(message.chat.id, '🔴 Novas notícias chegando!')
            if len(corpo) > 4096:
                for x in range(0, len(corpo), 4096):
                    bot.send_message(message.chat.id, corpo[x:x+4096], disable_web_page_preview=True)
            else:
                bot.send_message(message.chat.id, corpo)
        else:
            pass

    schedule.every().day.at("13:00").do(enviar)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


bot.polling()
