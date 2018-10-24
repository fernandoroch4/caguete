import os
from dotenv import load_dotenv
from os.path import join, dirname
import requests
from bs4 import BeautifulSoup

class DeputadosRS:
    textToPost = []

    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.deputados_page = os.getenv('DEP_PAGE')

    def getTextToPost(self):
        deputadosPage = self.getDom()
        deputadosName = self.getDepData(deputadosPage)

        for key, depName in enumerate(deputadosName):
            depSpent = self.getDepSpent(depName)
            depSpentSum = 0
            bigSpent = 0

            # check each dep
            for keySpent, depSpentValue in enumerate(depSpent['value']):
                spentValue = self.getSpentValueFormat(depSpentValue)
                depSpentSum += spentValue

                if spentValue > bigSpent:
                    bigSpent = spentValue
                    bigDepSpent = str(depSpentValue.getText().replace('-','')).replace('\n','')
                    bigDepSpentDesc = str(depSpent['description'][keySpent].getText())

            if depSpent['dep_quota_format'] < depSpentSum:
                text = "Em " + depSpent['month'] + " o dep. " + str(depName.getText()) + " excedeu a cota mensal. \n"
                text += "Cota: " + depSpent['dep_quota'] + "\n" + "Total de despesas: " + depSpent['dep_spent'] + "\n"
                text += "Maior depesa: " + bigDepSpentDesc + " : " + bigDepSpent
                self.textToPost.append(text)

        return self.textToPost

    # Get DOM from deputados page
    def getDom(self):
        deputadosRsPage = requests.get(self.deputados_page)
        return BeautifulSoup(deputadosRsPage.content, "lxml")

    # Get deputados name
    def getDepData(self, deputadosPage):
        return deputadosPage.findAll("a", {"class": "hlklstdeputado"})

    def getDepSpent(self, depName):
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

    def getSpentValueFormat(self, depSpentValue):
        return float(depSpentValue.getText().replace(' ','').replace('R$','').replace('-','').replace('\n-R$','').replace('\n','').replace('.','').replace(',','.'))
