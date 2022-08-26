import logging
from bs4 import BeautifulSoup
from requests import get

from models.model_job_offer import JobOffer

logging.getLogger(__name__)


def get_links_to_offers_pracuj(db, city: str, category: str):
    page_number = 1
    links = []
    cities = {
        'Gdańsk': 'gdansk;wp',
        'Szczecin': 'szczecin;wp',
        'Białystok': 'bialystok;wp',
        'Toruń': 'torun;wp',
        'Bydgoszcz': 'bydgoszcz;wp',
        'Olsztyn': 'olsztyn;wp',
        'Warszawa': 'warszawa;wp',
        'Lublin': 'lublin;wp',
        'Rzeszow': 'rzeszow;wp',
        'Kraków': 'krakow;wp',
        'Katowice': 'katowice;wp',
        'Opole': 'opole;wp',
        'Wrocław': 'wroclaw;wp',
        'Łódź': 'lodz;wp',
        'Poznań': 'poznan;wp',
        'Zielona Góra': 'zielona%20gora;wp',
        'Gorzów Wielkopolski': 'gorzow%20wielkopolski;wp',
        'Kielce': 'kielce;wp'
    }
    categories = {
        'Administracja biurowa': 'administracja%20biurowa;cc,5001',
        'Badania i rozwój': 'badania%20i%20rozwój;cc,5002',
        'Bankowość': 'bankowość;cc,5003',
        'BHP / Ochrona środowiska': 'bhp%20ochrona%20środowiska;cc,5004',
        'Budownictwo': 'budownictwo;cc,5005',
        'Call Center': 'call%20center;cc,5006',
        'Doradztwo / Konsulting': 'doradztwo%20konsulting;cc,5037',
        'Energetyka': 'energetyka;cc,5036',
        'Edukacja / Szkolenia': 'edukacja%20szkolenia;cc,5007',
        'Finanse / Ekonomia': 'finanse%20ekonomia;cc,5008',
        'Franczyza / Własny biznes': 'franczyza%20własny%20biznes;cc,5009',
        'Hotelarstwo / Gastronomia / Turystyka': 'hotelarstwo%20gastronomia%20turystyka;cc,5010',
        'Human Resources / Zasoby ludzkie': 'human%20resources%20zasoby%20ludzkie;cc,5011',
        'Internet / e-Commerce / Nowe media': 'internet%20e-commerce%20nowe%20media;cc,5013',
        'Inżynieria': 'inżynieria;cc,5014',
        'IT - Administracja': 'it%20-%20administracja;cc,5015',
        'IT - Rozwój oprogramowania': 'it%20-%20rozwój%20oprogramowania;cc,5016',
        'Kontrola jakości': 'kontrola%20jakości;cc,5034',
        'Łańcuch dostaw': 'łańcuch%20dostaw;cc,5017',
        'Marketing': 'marketing;cc,5018',
        'Media / Sztuka / Rozrywka': 'media%20sztuka%20rozrywka;cc,5019',
        'Nieruchomości': 'nieruchomości;cc,5020',
        'Obsługa klienta': 'obsługa%20klienta;cc,5021',
        'Praca fizyczna': 'praca%20fizyczna;cc,5022',
        'Prawo': 'prawo;cc,5023',
        'Produkcja': 'produkcja;cc,5024',
        'Public Relations': 'public%20relations;cc,5025',
        'Reklama / Grafika / Kreacja / Fotografia': 'reklama%20grafika%20kreacja%20fotografia;cc,5026',
        'Sektor publiczny': 'sektor%20publiczny;cc,5027',
        'Sprzedaż': 'sprzedaż;cc,5028',
        'Transport / Spedycja / Logistyka': 'transport%20spedycja%20logistyka;cc,5031',
        'Ubezpieczenia': 'ubezpieczenia;cc,5032',
        'Zakupy': 'zakupy;cc,5033',
        'Zdrowie / Uroda / Rekreacja': 'zdrowie%20uroda%20rekreacja;cc,5035',
        'Inne': 'inne;cc,5012'
    }

    while True:
        try:
            page = get(
                f"https://www.pracuj.pl/praca/{cities[city]}/{categories[category]}?pn={page_number}"
            ).content
            bs = BeautifulSoup(page, 'html.parser')

            offers = bs.find('div', {'class': 'results', 'id': 'results'})
            offers_list = offers.find('ul', class_='results__list-container')
            scrap = offers_list.find_all('a', class_='offer__click-area')

            if len(scrap) != 0:
                for item in scrap:
                    links.append(item['href'])
                page_number += 1
            else:
                break

        except Exception as e:
            print(f'get_links_to_offers_pracuj: {e}')

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
