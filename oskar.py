# IMPORTAR AS LIBS
import requests
import json
import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

import wikipedia

from PIL import Image  # pip install Pillow

# INSTANCIAR CHATBOT
#chatbot = ChatBot('Ananda')
#trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train('chatterbot.corpus.portuguese')
#trainerer = ListTrainer(chatbot)

# ARMAZENAR DIRETORIO PRINCIPAL EM VARIAVEL
dir_path = os.getcwd()
print('dir_path.....:  ' + dir_path)
# INICIAR APLICAÇÃO
driver = webdriver.Chrome(dir_path+'/chromedriver')
driver.get('https://web.whatsapp.com/')
driver.implicitly_wait(15)
print(driver.title)

# FUNÇÕES BÁSICAS DE COMUNICAÇÃO


def pegaConversa():
    try:
        print("iniciou pegaConversa: ")
        post = driver.find_elements_by_class_name('_12pGw')
        ultimo = len(post) - 1
        texto = post[ultimo].find_element_by_css_selector("span.selectable-text").text
        return texto
    except Exception as inst:
        print(inst)
        pass


def enviaMensagem(mensagem):
    try:
        caixa_de_texto = driver.find_element_by_class_name('_3u328')
        #valor = "*Ananda:* "+str(mensagem)
        valor = str(mensagem)
        for part in valor.split("\n"):
            caixa_de_texto.send_keys(part)
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).perform()
        time.sleep(0.5)
        botao_enviar = driver.find_element_by_class_name('_3M-N-')
        botao_enviar.click()
    except Exception as inst:
        print(inst)
        pass


# NOTÍCIAS


def noticias():
    try:
        print(1+1)
        req = requests.get(
            'https://newsapi.org/v2/top-headlines?country=br&category=technology&apiKey=3271a593d94141b78581547903ed3b85')
        noticias = json.loads(req.text)
        for news in noticias['articles']:
                titulo = news['title']
                link = news['url']
                desc = news['description']
                mensagem = "{}\n{}\n{}".format(titulo, desc, link)
                enviaMensagem(mensagem)
                time.sleep(1)
    except:
        enviaMensagem("agora não...")
        pass

def rpg():
    try:
        print(1+1)
        req = requests.get('http://dnd5eapi.co/api/classes/')
        resposta = json.loads(req.text)
        for resp in resposta['results']:
            print (resp)
            codigo = resp['url'][35:]
            print(codigo)
            mensagem = "*Classe:* {}\n *Código:* {}".format(resp['name'], codigo)
            enviaMensagem(mensagem)
            time.sleep(1)
    except:
        enviaMensagem("agora não...")
        pass

def rpg_class(codigo):
    try:
        print(1+1)
        req = requests.get('http://dnd5eapi.co/api/classes/'+codigo)
        resposta = json.loads(req.text)
        mensagem = "*Classe:*\n *Nome:* {}\n *hit_die: *{}".format(resposta['name'], resposta['hit_die'])
        enviaMensagem(mensagem)
        for resp in resposta['proficiencies']:
            mensagem = "\n\n *proficiencies: *\n *name:* {} ".format(resp['name'])
            enviaMensagem(mensagem)
            time.sleep(1)


        # for resp in resposta['results']:
        #     print (resp)
        #     codigo = resp['url'][35:]
        #     print(codigo)
        #     mensagem = "*Classe:* {}\n *Código:* {}".format(resp['name'], codigo)
        #     enviaMensagem(mensagem)
        #     time.sleep(1)
    except:
        enviaMensagem("agora não...")
        pass

# BLOCO PRINCIPAL DE EXECUÇÃO
salva = pegaConversa()
while True:
    try:
        
        # if pegaConversa().strip().lower() == 'noticias' or pegaConversa().strip().lower() == 'notícias':
        #     noticias()
        if pegaConversa().strip().lower() == 'rpg/classes':
            rpg()
        elif  pegaConversa().strip().lower()[:19] == 'rpg/classes/codigo/':
            rpg_class(pegaConversa().strip().lower()[19:])

    except:
        pass
