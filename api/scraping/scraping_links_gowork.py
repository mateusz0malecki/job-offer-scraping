import logging
from bs4 import BeautifulSoup
from requests import get

from models.model_job_offer import JobOffer

logging.getLogger(__name__)


def get_links_to_offers_gowork(db, city: str, category: str):
    page_number = 1
    links = []

    cities = {
        'Gdańsk': 'gdansk;l',
        'Szczecin': 'szczecin;l',
        'Białystok': 'bialystok;l',
        'Toruń': 'torun;l',
        'Bydgoszcz': 'bydgoszcz;l',
        'Olsztyn': 'olsztyn;l',
        'Warszawa': 'warszawa;l',
        'Lublin': 'lublin;l',
        'Rzeszow': 'rzeszow;l',
        'Kraków': 'krakow;l',
        'Katowice': 'katowice;l',
        'Opole': 'opole;l',
        'Wrocław': 'wroclaw;l',
        'Łódź': 'lodz;l',
        'Poznań': 'poznan;l',
        'Zielona Góra': 'zielona-gora;l',
        'Gorzów Wielkopolski': 'gorzow-wielkopolski;l',
        'Kielce': 'kielce;l'
    }

    categories = {
        'Administracja biurowa': 'administracja-biurowa;b',
        'Badania i rozwój': 'badania-i-rozwoj;b',
        'Bankowość': 'bankowosc;b',
        'BHP / Ochrona środowiska': 'bhp-ochrona-srodowiska-rolnictwo;b',
        'Budownictwo': 'budownictwo;b',
        'Call Center': 'call-center;b',
        'Edukacja / Szkolenia': 'edukacja-szkolenia;b',
        'Finanse / Ekonomia': 'finanse-ksiegowosc;b',
        'Franczyza / Własny biznes': 'franczyza-wlasny-biznes;b',
        'Hotelarstwo / Gastronomia / Turystyka': 'hotelarstwo-gastronomia-turystyka;b',
        'Human Resources / Zasoby ludzkie': 'hr-kadry-i-place;b',
        'Inżynieria': 'inzynieria;b',
        'IT - Rozwój oprogramowania': 'it;b',
        'Kadra zarządzająca': 'kadra-zarzadzajaca;b',
        'Kontrola jakości': 'kontrola-jakosci;b',
        'Marketing': 'marketing-reklama-pr;b',
        'Media / Sztuka / Rozrywka': 'media-sztuka-rozrywka;b',
        'Nieruchomości': 'nieruchomosci;b',
        'Opieka': 'opieka;b',
        'Opieka zdrowotna': 'opieka-zdrowotna;b',
        'Praca fizyczna': 'fizyczna;b',
        'Praca za granicą': 'praca-za-granica;b',
        'Prawo': 'prawo;b',
        'Produkcja': 'produkcja;b',
        'Reklama / Grafika / Kreacja / Fotografia': 'grafika-kreacja-fotografia;b',
        'Sprzedaż': 'sprzedaz-i-obsluga-klienta;b',
        'Transport / Spedycja / Logistyka': 'transport-spedycja-logistyka;b',
        'Ubezpieczenia': 'ubezpieczenia;b',
        'Zdrowie / Uroda / Rekreacja': 'uroda-rekreacja-zdrowy-styl-zycia;b'
    }

    while True:
        try:
            page = get(
                f"https://www.gowork.pl/praca/{cities[city]}/{categories[category]}/{page_number};pg"
            ).content
            bs = BeautifulSoup(page, 'html.parser')

            offers_list = bs.find_all('ul', class_="jobs-list")

            if len(offers_list) != 0:
                for item in offers_list:
                    offers = item.find_all('h2', class_="g-job-title")
                    for offer in offers:
                        link = offer.find('a')
                        links.append(f"https://www.gowork.pl{link['href']}")
                page_number += 1
            else:
                break

        except Exception as e:
            print(f'get_links_to_offers_gowork: {e}')

    links = list(set(links))

    offers_to_add = []
    for link in links:
        if not JobOffer.get_offer_by_link(db, link):
            offer = JobOffer(
                link=link,
                city=city,
                category=category
            )
            offers_to_add.append(offer)

    db.add_all(offers_to_add)
    db.commit()
    for n in offers_to_add:
        db.refresh(n)
