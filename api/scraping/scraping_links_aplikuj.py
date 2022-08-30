import logging
from bs4 import BeautifulSoup
from requests import get

from models.model_job_offer import JobOffer

logging.getLogger(__name__)


def get_links_to_offers_aplikuj(db, city: str, category: str):
    page_number = 1
    links = []

    cities = {
        'Gdańsk': 'gdansk',
        'Szczecin': 'szczecin',
        'Białystok': 'bialystok',
        'Toruń': 'torun',
        'Bydgoszcz': 'bydgoszcz',
        'Olsztyn': 'olsztyn',
        'Warszawa': 'warszawa',
        'Lublin': 'lublin',
        'Rzeszow': 'rzeszow',
        'Kraków': 'krakow',
        'Katowice': 'katowice',
        'Opole': 'opole',
        'Wrocław': 'wroclaw',
        'Łódź': 'lodz',
        'Poznań': 'poznan',
        'Zielona Góra': 'zielona-gora',
        'Gorzów Wielkopolski': 'gorzow-wielkopolski',
        'Kielce': 'kielce'
    }

    categories = {
        'Administracja biurowa': 'administracja-biurowa-praca-biurowa',
        'Administracja publiczna / Służba publiczna': 'sektor-publiczny-sluzby-mundurowe',
        'Badania i rozwój': 'badania-i-rozwoj',
        'BHP / Ochrona środowiska': 'bhp-ochrona-srodowiska',
        'Budownictwo': 'budownictwo-architektura-geodezja',
        'Call Center': 'obsluga - klienta - call - center',
        'Doradztwo / Konsulting': 'doradztwo-konsulting-audyt',
        'Energetyka': 'energetyka-energia-odnawialna',
        'Edukacja / Szkolenia': 'edukacja-badania-naukowe-szkolenia-tlumaczenia',
        'Finanse / Ekonomia': 'bankowosc-finanse',
        'Franczyza / Własny biznes': 'franczyza-wlasny-biznes',
        'Hotelarstwo / Gastronomia / Turystyka': 'hotelarstwo-gastronomia-turystyka',
        'Human Resources / Zasoby ludzkie': 'hr-kadry',
        'Internet / e-Commerce / Nowe media': 'internet-e-commerce-nowe-media',
        'Inżynieria': 'inzynieria-technologia-technika',
        'IT - Rozwój oprogramowania': 'it-informatyka',
        'Kadra zarządzająca': 'zarzadzanie-dyrekcja',
        'Księgowość': 'ksiegowosc-ekonomia',
        'Łańcuch dostaw': 'magazyn',
        'Marketing': 'media-pr-reklama-marketing',
        'Montaż / Serwis / Technika': 'serwis-montaz',
        'Motoryzacja': 'motoryzacja',
        'Nieruchomości': 'nieruchomosci',
        'Opieka zdrowotna': 'medycyna-farmacja-zdrowie',
        'Praca fizyczna': 'praca-fizyczna',
        'Prawo': 'prawo-i-administracja-panstwowa',
        'Produkcja': 'produkcja-przemysl',
        'Reklama / Grafika / Kreacja / Fotografia': 'grafika-i-fotografia',
        'Rolnictwo': 'rolnictwo-hodowla',
        'Rzemiosło': 'wytworstwo-rzemioslo',
        'Sport': 'rekreacja-i-sport',
        'Sprzedaż': 'sprzedaz-zakupy',
        'Sztuka / Rozrywka / Rekreacja / Projektowanie': 'sztuka-rozrywka-kreacja-projektowanie',
        'Telekomunikacja': 'telekomunikacja',
        'Transport / Spedycja / Logistyka': 'logistyka-spedycja-transport',
        'Ubezpieczenia': 'ubezpieczenia',
        'Zdrowie / Uroda / Rekreacja': 'uroda-pielegnacja-dietetyka',
        'Inne': 'inne'
    }

    while True:
        try:
            page = get(
                f"https://www.aplikuj.pl/praca/{cities[city]}/{categories[category]}/strona-{page_number}",
                allow_redirects=False
            ).content
            bs = BeautifulSoup(page, 'html.parser')

            section = bs.find('ul', class_="offer-list")
            offers_list = section.find_all(
                'li',
                class_=[
                    'offer-card sm:border-secondary',
                    'offer-card sm:border-gray-400',
                    'offer-card card-promote sm:border-tertiary'
                ]
            )
            if len(offers_list) == 0:
                break

            for item in offers_list:
                item_filter = item.find('span', class_='text-sm')
                if item_filter.get_text() == city:
                    offer_link = item.find('a', class_="offer-title")
                    links.append(f"https://www.aplikuj.pl{offer_link['href']}")
            page_number += 1

        except Exception as e:
            print(f'get_links_to_offers_aplikuj: {e}')

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
