import requests
from bs4 import BeautifulSoup
import platform
import subprocess
from flask import Flask, render_template
import datetime
import webbrowser



def get_page(url:str,send_notif:bool=True):

    response = requests.get(url)
    html = response.text

    if response.status_code == 200:
        soup = BeautifulSoup(html, 'html.parser')
        print("tonlunetier")

        articles = soup.find_all('li', class_="grid__item")
        articles_form = {}
        for article in articles:
            name_element = article.find('a', class_="full-unstyled-link")
            name = name_element.text.strip() if name_element else "Nom non disponible"

            price_element = article.find('span', class_="price-item price-item--regular")
            price = price_element.text.strip() if price_element else "Prix non disponible"

            articles_form[name] = price
        if send_notif:
            if platform.system() == 'Linux':
                try:
                    subprocess.run(['notify-send', '--version'], check=True)
                except FileNotFoundError:
                    print("notify-send n'est pas disponible sur ce système.")
                else:
                    for name, price in articles_form.items():
                        subprocess.run(['notify-send', f"{name}", f"Prix: {price}"])
            else:
                print("Ce script est destiné à être exécuté sur un système Linux.")
        return articles_form
    else:
        print("La page n'a pas pu être téléchargée. Vérifiez l'URL ou votre connexion Internet.")




app = Flask(__name__)

# Définition des routes
@app.route('/')
def generate_report():
    articles_form =get_page('https://tg.tonlunetier.com/collections/all',False)
    current_time = datetime.datetime.now()

    # Rendu du template HTML avec les données
    return render_template('report.html', report_data=articles_form, current_time=current_time)
    

if __name__ == '__main__':
    app.run(debug=True,port=52424)
