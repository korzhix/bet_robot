# Импорт модулей
import vk
from time import sleep
import main_functions as info

u_id = '370609037'#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def auth():
	#Cоздание сессии

	login = ''
	password = ''
	vk_id = ''
	token = ''

	session = vk.Session(access_token=token)
	vkapi = vk.API(session,v=5.75)

	return vkapi
vkapi = auth() #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def prettify(message):
	
	decored_message = """Mатч\n {team_one}({team_one_sum}) : {team_two}({team_two_sum})\nНачало матча:{data_start}
		\n\n""".format(team_one=message['team_one'], team_one_sum=message['team_one_sum'],
		team_two=message['team_two'], team_two_sum=message['team_two_sum'], data_start=message['data-start'])
	return decored_message

def give_upcoming():
	upcoming_list = info.final_list
	lenght = len(upcoming_list)
	str_len=ascii(lenght)
	i=0
	final_message = "Матчи на сегодня ( " + str_len + " штук ) " + "\n" + "Время ближайшего: " + upcoming_list[0]['data-start']+"\n '\n"

	while i < lenght :
		message = upcoming_list[i]
		d_mes = prettify(message)
		final_message =final_message + d_mes
		i+=1
	vkapi.messages.send(user_id=u_id,message=final_message)

def give_next():
	next_match = info.final_list[0]
	final_message = "Следующий матч \n"
	final_message+=prettify(next_match)
	vkapi.messages.send(user_id=u_id,message=final_message)

def send_message(mes):
	vkapi.messages.send(user_id=u_id,message=mes)

send_message("Worked!")


