#!/usr/bin/python3
# Coyright Caguete Bot
import os
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

# Run every 12h (43200 seconds)
# It's necessary when we don't have a cron
every = 43200

# Define main function
def main():

    # Call what do you want to post
    deputados_rs()

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
    soup = BeautifulSoup(page.context, "lxml")

    # Get all dep data
    dep_name  = soup.findAll("a", {"class": "hlklstdeputado"})
    dep_email = soup.findAll("span", {"class": "lbllstdeputadoemail"})
    dep_part  = soup.findAll("span", {"class": "lbllstdeputadosiglapartido"})
    dep_tel   = soup.findAll("span", {"class": "lbllstdeputadotelefone"})

    for num in range(len(dep_name)):
        # Post 1 dep each 10 seconds
        time.sleep(10)
        fonte = "http://www.al.rs.gov.br/deputados/ListadeDeputados.aspx"
        post = "Deputado: " + dep_name + "\n" + "Partido: " + dep_part + "\n" + "E-mail: " + dep_email + "\n" + "Telefone: " + dep_tel + "\n" + "Fonte: " + fonte
        twitter(post)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(every)
