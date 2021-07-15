from os import name
from selectorlib import Extractor
import requests 
import json 
from time import sleep


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selectors.yml')

def scrape(url, referer):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': referer,
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    #print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)

def checkprice():
    product={}
    product['info'] = []
    with open("amazonurls.txt",'r') as urllist:
        length=len(urllist.read().splitlines())
    for i in range(length):
        print(f"\nProduct {i+1}: ")
        with open("amazonurls.txt",'r') as urllist:
            data = scrape(urllist.read().splitlines()[i], 'https://www.amazon.in/')
            print(f"Name: {data['name'][:25]}")
            pname = data['name'][:20]
            if(isinstance(data['price'], str)):
                print(f"Amazon: {data['price']}")
                amazonprice = data['price'] 
            elif(isinstance(data['price2'], str)):
                print(f"Amazon: {data['price2']}")
                amazonprice = data['price2'] 
            elif(isinstance(data['price3'], str)):
                print(f"Amazon: {data['price3']}")
                amazonprice = data['price3'] 
            else:
                print("notfound")
                amazonprice = False
        with open("flipkarturls.txt",'r') as urllist:
            data = scrape(urllist.read().splitlines()[i], 'https://www.flipkart.com/')
            if(isinstance(data['price5'], str)):
                print(f"Flipkart: {data['price5']}")
                flipkartprice = data['price5'] 
            else:
                print("Not found")
                flipkartprice = False
        with open("paytmurls.txt",'r') as urllist:
            data = scrape(urllist.read().splitlines()[i], 'https://www.paytmmall.com/')
            if(isinstance(data['price4'], str)):
                print(f"Paytm: {data['price4']}")
                Paytmprice = data['price4'] 
            else:
                print("Not found")
                Paytmprice = False 
        with open("vijayurls.txt",'r') as urllist:
            data = scrape(urllist.read().splitlines()[i], 'https://www.vijaysales.com/')
            if(isinstance(data['price6'], str)):
                print(f"VijaySales: {data['price6']}")
                vijayprice = data['price6'] 
            else:
                print("Not found")
                vijayprice = False
        amazonpriceconverted = amazonprice[2:10]
        amazonpriceconverted1 = float(amazonpriceconverted.replace(',',''))
        flipkartpriceconverted = flipkartprice[1:7]
        flipkartpriceconverted1 = float(flipkartpriceconverted.replace(',',''))
        Paytmpriceconverted = Paytmprice
        Paytmpriceconverted1 = float(Paytmpriceconverted.replace(',',''))
        vijaypriceconverted = vijayprice[2:8]
        vijaypriceconverted1 = float(vijaypriceconverted.replace(',',''))
        product['info'].append({
            'name': pname,
            'amazon': amazonpriceconverted1,
            'flipkart': flipkartpriceconverted1,
            'paytm' : Paytmpriceconverted1,
            'vijay' : vijaypriceconverted1
        })
            
    with open('price.jsonl','w') as outfile:
        json.dump(product, outfile)
            


while(True):    
    print('----------------------')
    checkprice()
    #sleep(30)
    