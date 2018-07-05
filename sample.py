#!/usr/bin/python3
# Coyright Caguete Bot
import os
import sys
import time
import datetime
import requests
from bs4 import BeautifulSoup
from TwitterAPI import TwitterAPI
from dotenv import load_dotenv
from os.path import join, dirname

# Loading environments variables
# Create .env file path
dotenv_path = join(dirname(__file__), '.env')
# Load file from path
load_dotenv(dotenv_path)

# Define main function
def main():

    # Call what do you want to post
    sys.exit() if deputados_rs() == True else False

# Twitter function
def twitter(post):
    api = TwitterAPI(os.getenv('T_KEY'),
                     os.getenv('T_SECRET'),
                     os.getenv('T_TOKEN'),
                     os.getenv('T_TOKEN_SECRET'))
    r = api.request('statuses/update', {'status': post})
    return 'SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text

# Get data from web
def deputados_rs():
    # Get page
    page = requests.get('http://www.al.rs.gov.br/deputados/ListadeDeputados.aspx')
    # Load page content by lxml
    soup = BeautifulSoup(page.content, "lxml")

    # Get all dep data
    dep_name  = soup.findAll("a", {"class": "hlklstdeputado"})
    dep_email = soup.findAll("span", {"class": "lbllstdeputadoemail"})
    dep_part  = soup.findAll("span", {"class": "lbllstdeputadosiglapartido"})
    dep_tel   = soup.findAll("span", {"class": "lbllstdeputadotelefone"})

    for num in range(len(dep_name)):
        fonte = "https://goo.gl/cRQ8RH"
        post = "RS" + "\n" + "Deputado estadual: " + str(dep_name[num].getText()) + "\n" + "Partido: " + str(dep_part[num].getText()) + "\n" + "E-mail: " + str(dep_email[num].getText()) + "\n" + "Telefone: " + str(dep_tel[num].getText()) + "\n" + "Fonte: " + fonte
        time.sleep(60) # Post one dep each 60 seconds
        print(twitter(post))
    return True


if __name__ == '__main__':
    while True:
        main()
