#!/usr/bin/python3
#
# Coyright Caguete Bot
#
import os
import sys
import requests
from bs4 import BeautifulSoup
from TwitterAPI import TwitterAPI
from dotenv import load_dotenv
from os.path import join, dirname

# Loading environments variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Variables
DEPUTADOS_PAGE = "http://www.al.rs.gov.br/deputados/ListadeDeputados.aspx"

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

# Check deputados Spent
def deputados_rs():

    deputadosPage = getDom(DEPUTADOS_PAGE)
    deputadosName = getDepData(deputadosPage)

    for key, depName in enumerate(deputadosName):
        depSpent = getDepSpent(depName)
        depSpentSum = 0
        bigSpent = 0

        # check each dep
        for keySpent, depSpentValue in enumerate(depSpent['value']):
            spentValue = getSpentValueFormat(depSpentValue)
            depSpentSum += spentValue

            if spentValue > bigSpent:
                bigSpent = spentValue
                bigDepSpent = str(depSpentValue.getText().replace('-','')).replace('\n','')
                bigDepSpentDesc = str(depSpent['description'][keySpent].getText())

        if depSpent['dep_quota_format'] < depSpentSum:
            textToPost = "Em " + depSpent['month'] + " o dep. " + str(depName.getText()) + " excedeu a cota mensal. \n"
            textToPost += "Cota: " + depSpent['dep_quota'] + "\n" + "Total de despesas: " + depSpent['dep_spent'] + "\n"
            textToPost += "Maior depesa: " + bigDepSpentDesc + " : " + bigDepSpent
            print(textToPost)
            #print(twitterPost(textToPost))
    return True

# Get DOM from deputados page
def getDom(DEPUTADOS_PAGE):
    deputadosRsPage = requests.get(DEPUTADOS_PAGE)
    return BeautifulSoup(deputadosRsPage.content, "lxml")

# Get deputados name
def getDepData(deputadosPage):
    return deputadosPage.findAll("a", {"class": "hlklstdeputado"})

def getDepSpent(depName):
    depPageSpent = requests.get(depName.get('href') + '/Transparência/Gastos.aspx')
    soupSpent = BeautifulSoup(depPageSpent.content, "lxml")

    # Dep spent
    depSpentDescription = soupSpent.findAll("td", {"class": "lblDescricaoDespesa"})
    depsSpentValues = soupSpent.findAll("td", {"class": "lblValorDespesa"})

    # Spent monthly allowance
    depQuotaFormat = soupSpent.findAll("span", {"class": "lblCota"})
    depQuotaFormat = float(depQuotaFormat[0].getText().replace(' ','').replace('R$','').replace('.','').replace(',','.'))
    depQuota = soupSpent.findAll("span", {"class": "lblCota"})
    depQuota = str(depQuota[0].getText())
    depSpent = soupSpent.findAll("span", {"class": "lbldespesa"})
    depSpent = str(depSpent[0].getText().replace('-',''))

    # Get month
    spentMonth = soupSpent.findAll("option", {"selected": True})
    spentMonth = spentMonth[1].getText()

    return {
        'description': depSpentDescription,
        'value': depsSpentValues,
        'dep_quota_format': depQuotaFormat,
        'dep_quota': depQuota,
        'dep_spent': depSpent,
        'month': spentMonth
    }

def getSpentValueFormat(depSpentValue):
    return float(depSpentValue.getText().replace(' ','').replace('R$','').replace('-','').replace('\n-R$','').replace('\n','').replace('.','').replace(',','.'))

if __name__ == '__main__':
    while True:
        main()
