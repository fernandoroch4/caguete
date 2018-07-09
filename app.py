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

    #verify: http://book.pythontips.com/en/latest/enumerate.html

    for num in range(len(dep_name)):
        page_spent = requests.get(dep_name[num].get('href') + '/Transparência/Gastos.aspx')
        soup_spent = BeautifulSoup(page_spent.content, "lxml")
        # Get dep spent
        dep_spent_description = soup_spent.findAll("td", {"class": "lblDescricaoDespesa"})
        dep_spent_value = soup_spent.findAll("td", {"class": "lblValorDespesa"})
        # Get dep monthly allowance
        dep_quota = soup_spent.findAll("span", {"class": "lblCota"})
        dep_quota2 = soup_spent.findAll("span", {"class": "lblCota"})
        dep_quota = float(dep_quota[0].getText().replace(' ','').replace('R$','').replace('.','').replace(',','.'))
        dep_spent = soup_spent.findAll("span", {"class": "lbldespesa"})
        sum_spent = 0
        big_spent = 0
        # Get month
        spent_month = soup_spent.findAll("option", {"selected": True})
        spent_month = spent_month[1].getText()
        for i in range(len(dep_spent_value)):
            dsv = float(dep_spent_value[i].getText().replace(' ','').replace('R$','').replace('-','').replace('\n-R$','').replace('\n','').replace('.','').replace(',','.'))
            sum_spent += dsv
            if dsv > big_spent:
                big_spent = dsv
                biggest_spent = dep_spent_value[i].getText().replace('-','')
                biggest_spent_d = dep_spent_description[i].getText()
        if dep_quota < sum_spent:
            post = "Em " + spent_month + " o dep. " + str(dep_name[num].getText()) + " excedeu a cota mensal. \n"
            post += "Cota: " + str(dep_quota2[0].getText()) + "\n" + "Total de despesas: " + str(dep_spent[0].getText().replace('-','')) + "\n"
            post += "Maior depesa: " + str(biggest_spent_d) + " : " + str(biggest_spent.replace('\n',''))
            #for d in range(len(dep_spent_description)):
            #    post +=  dep_spent_description[d].getText() + ":" + dep_spent_value[d].getText().replace('\n','').replace('-','') + "\n"
            #print("cota: {} total: {} diferença: {}".format(round(dep_quota,2),round(sum_spent,2),round(dep_quota-sum_spent,2)))
            #post = "RS" + "\n" + "Deputado estadual: " + str(dep_name[num].getText()) + "\n" + "Partido: " + str(dep_part[num].getText()) + "\n" + "E-mail: " + str(dep_email[num].getText()) + "\n" + "Telefone: " + str(dep_tel[num].getText()) + "\n" + "Fonte: " + fonte
            #time.sleep(60) # Post one dep each 60 seconds
            print(post)
            #print(twitter(post))
    return True
    
if __name__ == '__main__':
    while True:
        main()
