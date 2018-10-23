#!/usr/bin/python3
#
# Coyright Caguete Bot
#
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
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def main():
    sys.exit() if deputados_rs() == True else False

# Twitter function
def twitterPost(post):
    apiTwitter = TwitterAPI(os.getenv('T_KEY'),
                            os.getenv('T_SECRET'),
                            os.getenv('T_TOKEN'),
                            os.getenv('T_TOKEN_SECRET'))
    response = apiTwitter.request('statuses/update', {'status': post})
    return 'SUCCESS' if response.status_code == 200 else 'PROBLEM: ' + response.text

# Get data from web
def deputados_rs():
    deputadosRsPage = requests.get('http://www.al.rs.gov.br/deputados/ListadeDeputados.aspx')
    soup = BeautifulSoup(deputadosRsPage.content, "lxml")

    # get data from DOM
    depName  = soup.findAll("a", {"class": "hlklstdeputado"})
    depEmail = soup.findAll("span", {"class": "lbllstdeputadoemail"})
    depPartido  = soup.findAll("span", {"class": "lbllstdeputadosiglapartido"})
    depTel   = soup.findAll("span", {"class": "lbllstdeputadotelefone"})

    # for num in range(len(dep_name)):
    for key1, value_dep_name in enumerate(depName):
        pageSpent = requests.get(value_dep_name.get('href') + '/Transparência/Gastos.aspx')
        soupSpent = BeautifulSoup(pageSpent.content, "lxml")

        # Get dep spent
        depSpentDescription = soupSpent.findAll("td", {"class": "lblDescricaoDespesa"})
        depsSpentValues = soupSpent.findAll("td", {"class": "lblValorDespesa"})

        # Get dep monthly allowance
        depQuota = soupSpent.findAll("span", {"class": "lblCota"})
        depQuota2 = soupSpent.findAll("span", {"class": "lblCota"})
        depQuota = float(depQuota[0].getText().replace(' ','').replace('R$','').replace('.','').replace(',','.'))
        depSpent = soupSpent.findAll("span", {"class": "lbldespesa"})
        depSpentSum = 0
        depSpentBigger = 0

        # Get month
        spentMonth = soupSpent.findAll("option", {"selected": True})
        spentMonth = spentMonth[1].getText()

        #for i in range(len(dep_spent_value)):
        for key2, value_dep_spent in enumerate(depsSpentValues):
            depSpentValue = float(value_dep_spent.getText().replace(' ','').replace('R$','').replace('-','').replace('\n-R$','').replace('\n','').replace('.','').replace(',','.'))
            depSpentSum += depSpentValue

            if depSpentValue > depSpentBigger:
                depSpentBigger = depSpentValue
                SpentBigger = value_dep_spent.getText().replace('-','')
                SpentBiggerDescription = depSpentDescription[key2].getText()

        if depQuota < depSpentSum:
            textToPost = "Em " + spentMonth + " o dep. " + str(value_dep_name.getText()) + " excedeu a cota mensal. \n"
            textToPost += "Cota: " + str(depQuota2[0].getText()) + "\n" + "Total de despesas: " + str(depSpent[0].getText().replace('-','')) + "\n"
            textToPost += "Maior depesa: " + str(SpentBiggerDescription) + " : " + str(SpentBigger.replace('\n',''))
            print(textToPost)
            #print(twitterPost(textToPost))
    return True

if __name__ == '__main__':
    while True:
        main()
