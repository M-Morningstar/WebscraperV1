import os, subprocess
from bs4 import BeautifulSoup
import re, requests, country_converter as coco
import hsCode as hsCode
from fake_useragent import UserAgent

class Product:
    def __init__(self):
        pass

    def __str__(self):
        return f'name: {self.name} about: {self.about} tarife kodu: {self.tarifeKodu} country of origin: {self.countryOfOrigin} original price: {self.originalPrice} currency: {self.currencyType} price in USD: {self.priceInUSD}'
    
    def currencyConvertionRate(self):
        url = f'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To={self.currencyType}'
        backupURL = f'https://www.oanda.com/currency-converter/en/?from={self.currencyType}&to=USD&amount=1'
        newUrl = f'https://wise.com/gb/currency-converter/{self.currencyType.lower()}-to-usd-rate?amount=1'

        userAgent = UserAgent(platforms='pc')

        r = requests.get(newUrl, headers={'User-Agent': userAgent.random})

        soup = BeautifulSoup(r.content, 'lxml')

        try:
            rate = soup.find('span', class_='text-success').text
        except:
            rate = '1'

        return rate

    def formatNumber(self, number):
        # Remove the LRM character
        number = number.replace('\u200e', '')
        # Remove thousand separators
        number = re.sub(r'[,.](?=\d{3}(?:[,.]|$))', '', number)
        # Replace comma with dot for decimal separator
        number = number.replace(',', '.')
        return number

    def fillProductInfo(self, filepath):
        cc = coco.CountryConverter()
        with open(filepath, 'r') as file:
            html_content = file.read()
        
        fileSplit = (filepath.split('/')[-1]).split('_')
        self.currencyType = (fileSplit[1].split('.'))[0]

        soup = BeautifulSoup(html_content, 'lxml')

        try:
            self.name = soup.find('span', class_='a-size-large product-title-word-break').text.strip()
        except:
            self.name = 'Title not Found'

        try:
            self.about = soup.find('ul', class_='a-unordered-list a-vertical a-spacing-mini').text
        except:
            self.about = 'No about information provided for this product'

        self.countryOfOrigin = cc.convert(names = fileSplit[0], to = 'name_short')
        if self.countryOfOrigin == 'Türkiye':
            self.countryOfOrigin = 'Turkey'

        try:
            description = soup.find_all('a', class_='a-link-normal a-color-tertiary')[-1].text
        except:
            description = self.name

        codeFinder = hsCode.HSCode(self.countryOfOrigin, description)
        self.tarifeKodu = codeFinder.findCode()

        try:
            self.originalPrice = soup.find('span', class_='a-price-whole').text + soup.find('span', class_='a-price-fraction').text
            self.originalPrice = self.formatNumber(self.originalPrice)
        except:
            self.originalPrice = 'Price not found'

        rate = self.currencyConvertionRate()

        if self.originalPrice != 'Price not found':
            self.priceInUSD = float(self.originalPrice) * float(rate)
        else:
            self.priceInUSD = "Common price can't be calculated"

    def convertToDict(self):
        return {
            'Title': self.name,
            'About': self.about,
            'Country of Origin': self.countryOfOrigin,
            'Tariff Code': self.tarifeKodu,
            'Price': self.originalPrice,
            'Original Currency Type': self.currencyType,
            'Price in USD': f'{self.priceInUSD} USD'
        }


# Your main Python code here
print("Running main Python program...")

productList = []
        