import config
import telebot 
from telebot import types

bot = telebot.TeleBot(config.token)

user_num1 = ''
user_num2 = ''
user_prom = ''
result = None

#если /start, /help
@bot.message_handler(commands=['start', 'help']) 
def start(message):
	markup = types.ReplyKeyboardRemove(selective=False)            #убрать клавиатуру Телеграм, которая выводилась до этого
	msg = bot.send_message(message.chat.id,'Привет!' + message.from_user.first_name + ',я бот-калькулятор\nВведите число', reply_markup=markup)
	bot.register_next_step_handler(msg, num1_step)


def num1_step(message, result = None):
	try:
		global user_num1
		if result == None:    #записываем число если только начали start
			user_num1 = int(message.text)
		else: 
			user_num1 = str(result)	#если был передан результат записываем его в первое число
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
		btn1 = types.KeyboardButton('+')
		btn2 = types.KeyboardButton('-')
		btn3 = types.KeyboardButton('*')
		btn4 = types.KeyboardButton('/')
		markup.add(btn1, btn2, btn3, btn4)

		msg = bot.send_message(message.chat.id, 'Выберите операцию', reply_markup=markup)
		bot.register_next_step_handler(msg, process_step)
	except Exception as e:
		bot.reply_to(message, 'Это не число')

def process_step(message):
	try:
		global user_prom
		user_prom = message.text   #запоминаем операцию
		markup = types.ReplyKeyboardRemove(selective=False)
		msg = bot.send_message(message.chat.id,'Введите еще число', reply_markup=markup)
		bot.register_next_step_handler(msg, num2_step)
	except Exception as e:
		bot.reply_to(message, 'Это не число')

def num2_step(message):
	try:
		global user_num2
		user_num2 = int(message.text)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		btn1 = types.KeyboardButton('Результат')
		btn2 = types.KeyboardButton('Продолжить вычисление')
		markup.add(btn1, btn2)
		msg = bot.send_message(message.chat.id,'Показать результат или продолжить вычисления?', reply_markup=markup)
		bot.register_next_step_handler(msg, alternative_step)
	except Exception as e:
		bot.reply_to(message, 'Это не число')

def alternative_step(message):
	try:
		calc() #сделать вычисления
		markup = types.ReplyKeyboardRemove(selective=False)
		if message.text.lower() == 'результат':
			bot.send_message(message.chat.id, calcResPrint(), reply_markup=markup)
		elif message.text.lower() == 'продолжить вычисление':
			num1_step(message, result)	
	except Exception as e:
		bot.reply_to(message, 'Что-то пошло не так')
		
def calcResPrint():  #Вывод результата пользователю
	global user_num1, user_num2, user_prom, result
	return 'Результат:' + str(user_num1) + ' ' + user_prom + ' '+ str(user_num2) + '=' + str(result) 		


def calc():           #Вычисление
	global user_num1, user_num2, user_prom, result
	result = eval(str(user_num1) + user_prom + str(user_num2))
	return result


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()


bot.polling(none_stop=True)

# if__name__=='__calc__':
# 	bot.polling(none_stop=True)







