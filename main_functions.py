from bs4 import BeautifulSoup
import requests
from datetime import datetime,date,time
#import positive_bot_vk_functions as vk_f

url_csgopositive = 'https://csgopositive.com/'
url_hltv = 'https://www.hltv.org/matches'

def get_html(url):
    r = requests.get(url)                                                       #Получаем html из запроса get по url
    return r.text
###############################################################################################################
###############################################################################################################
###############################################################################################################
#РАБОTА С CSGOPOSITIVE
##############################################################################################################
def get_upcoming_matches_list(html):    #Получаем блок html со следующими матчами
    #Переменные с html_ хранят в себе html текст
    soup = BeautifulSoup(html,'html.parser')

    #filter_ = soup.find(name="div", class_="app_filter").find(name="a", class_="active").string
    
    upcoming_content = soup.find(name='div', id='upcoming')  #Берем нужный блок
    html_matches = list()   #Cписок html блоков матчей
    lenght = len(html_matches)
    i = 0
    while lenght <= 10: #Набираем не менее 10 матчей в список
        page = upcoming_content.find_all(name='div', class_='page')[i].find_all(name='div',class_='csgo_event')   #Берем iю страницу матчей
        for j in page:
            html_matches.append(j) # Добавляем блок отдельнго матча
        i+=1
        lenght = len(html_matches)
    return html_matches #Возвращаем список с блоками матчей

def match_info(matches_list, counter):  #Берем всю информацию о матче
    #if counter is None:
    #    counter = 0
    next_match = matches_list[counter]                                          #Блок с информацией о след. матче

    match_info = dict()                                                         #Создаем словарь с информацией о матче
    match_info['data-app_id'] = next_match['data-app_id']
    match_info['data-id'] = next_match['data-id']

    team_one = next_match.find_all(name='span', class_='team_name')[0]                                                         #first name
    team_two = next_match.find_all(name='span', class_='team_name')[1]                                                         #second name
    #Ищем процент победы команды
    team_one_sum = next_match.find_all(name='span',class_='percent_sum')[0]
    team_two_sum = next_match.find_all(name='span',class_='percent_sum')[1]
    #ЗАПОЛНЯЕМ СЛОВАРЬ
    match_info['team_one_sum'] = team_one_sum.contents[0]
    match_info['team_two_sum'] = team_two_sum.contents[0]
    match_info['team_one'] = team_one.string
    match_info['team_two'] = team_two.string
    match_info['data-start'] = next_match.find(name='span', class_='timer')['data-start']
    match_info['event_type'] = next_match.find(name='span', class_='event_type').string

    return match_info                                                           #Возвращаем список

#ФУНКЦИЯ ГЕНЕРИРУЮЩАЯ УПОРЯДОЧЕННЫЙ СПИСОК ГРЯДУЩИХ BO3 МАТЧЕЙ
def get_matches_today(html_matches_blocks_list):  #Принимаем блок матчей из get_upcoming_matches_list
    i = 0
    matches = list()
    lenght = len(html_matches_blocks_list)    #Длина списка с html блоками матчей
    while i < lenght:
        match = match_info(html_matches_blocks_list,i)
        matches.append(match)
        i+=1;
    lenght=len(matches)
    i=0
    while i<lenght:
        match_type = str(matches[i]['event_type'])
        #print(match_type,' ', type(match_type), matches[i]['team_one'])
        if match_type == 'BO1':
            #print('true,deleting!')
            del matches[i]
            i-=1
        i+=1
        lenght=len(matches)
    return matches
################################################################################################################
################################################################################################################
################################################################################################################
#НАЧИНАЕМ РАБОТАТЬ С HLTV.ORG, ОСНОВНАЯ ЦЕЛЬ - ВЕРНУТЬ ССЫЛКУ НА МАТЧ ГДЕ СТАВКА
################################################################################################################

def get_hltv_match_page(html,team_name):    #Функция возвращает ссылку на матч, куда была сделана ставка или сообшение что матчей нет

    #html - html текст url_hltv
    #team_name -название команды, на которую ставили
    #message - собщение для возврата
    soup = BeautifulSoup(html,'html.parser')
    
    try:
        standard_line = soup.find(name='h2',class_='standard-headline',string='Live matches').string   #Строка Live matches
    except AttributeError as e:
        message = "Live матчей сейчас нет:<"
        return message
    html_live_matches = soup.find(class_="live-matches")   #Начиная отсюда все что есть html тект имеет html_ в начале
    for i in html_live_matches: # i - html блок live матча 
        try:
            teams = i.find_all(class_="teams")  #Список имен команд
            for j in teams:
                if j.span.string == team_name:  #Если нашли нужную команду(из аргумента)
                    #html_scores={}                     #В этом блоке проверка счета матча. Решил ее не делать т.к. все равно буду проверять вручную                   
                    #for g in j.parent:
                        #try:
                        #    if g.get("class")[0] in ("livescore","total"):
                        #        try:
                        #            html_scores["map" + g.span["data-livescore-map"]] = g.string
                        #        except KeyError as e:
                        #            html_scores["total"] = g.string
                        #except AttributeError as e:
                        #    continue
                    message = "https://www.hltv.org"+i.a["href"]
                    return message
        except AttributeError as e:
            continue
    message = "Твой матч сейчас не в эфире!"
    return message

#ВАЖНЫЕ КОНСТАНТЫ ДЛЯ ДРУГИХ МОДУЛЕЙ
####################################
html_csgopositive = get_html(url_csgopositive)
html_hltv = get_html(url_hltv)

list_csgopositive = get_upcoming_matches_list(html_csgopositive)
final_list = get_matches_today(list_csgopositive)
ref_text = get_hltv_match_page(html_hltv,'asd')#Второй аргумент будет браться из сообщения
#########################################################################################

#################################################################################################################
#################################################################################################################
#################################################################################################################
#НИЖЕ ПРЕДСТАВЛЕНЫ ФУНКЦИИ РАБОТЫ СО ВРЕМЕНЕМ
#################################################################################################################
def datetime_now(): #Возвращает текущее время
    now_datetime = datetime.now()   #Текущее время и дата
    return now_datetime #Возвращает текущее время
    
def next_match_datetime():  #Смотрит время следующего матча и возвращает его
    str_time = final_list[0]['data-start'] #Данные из исходного массива(Date and time)
    
    hours = int(str_time[11:13])    #Вытаскиваем оттуда часы
    minutes = int(str_time[14:16])  #И тащим оттуда же минуты

    month = int(str_time[0:2])
    day = int(str_time[3:5])
    year = int(str_time[6:10])

    next_match_datetime = datetime(year=year,month=month,day=day,hour=hours,minute=minutes)

    return next_match_datetime

def need_to_bet(next_match_datetime):   #Принимаем бъект datetime следующего матча
    now_datetime = datetime_now()
    match_start_datetime = next_match_datetime

    delta = match_start_datetime - now_datetime

    if  delta.seconds in {600,300}:
        print('''/n''','Нужно ставить!','''/n''','До матча осталось 10 минут!')
        return 1
    else:
        print(delta.seconds)
        return 0