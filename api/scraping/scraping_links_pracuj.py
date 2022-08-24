import logging
from bs4 import BeautifulSoup
from requests import get

logging.getLogger(__name__)


def get_links_to_offers_pracuj(city: str, category: str):
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
        'kielce': 'kielce;wp'
    }
    categories = {
        'Administracja biurowa': 5001,
        'Badania i rozwój': 5002,
        'Bankowość': 5003,
        'BHP / Ochrona środowiska': 5004,
        'Budownictwo': 5005,
        'Call Center': 5006,
        'Doradztwo / Konsulting': 5037,
        'Energetyka': 5036,
        'Edukacja / Szkolenia': 5007,
        'Finanse / Ekonomia': 5008,
        'Franczyza / Własny biznes': 5009,
        'Hotelarstwo / Gastronomia / Turystyka': 5010,
        'Human Resources / Zasoby ludzkie': 5011,
        'Internet / e-Commerce / Nowe media': 5013,
        'Inżynieria': 5014,
        'IT - Administracja': 5015,
        'IT - Rozwój oprogramowania': 5016,
        'Kontrola jakości': 5034,
        'Łańcuch dostaw': 5017,
        'Marketing': 5018,
        'Media / Sztuka / Rozrywka': 5019,
        'Nieruchomości': 5020,
        'Obsługa klienta': 5021,
        'Praca fizyczna': 5022,
        'Prawo': 5023,
        'Produkcja': 5024,
        'Public Relations': 5025,
        'Reklama / Grafika / Kreacja / Fotografia': 5026,
        'Sektor publiczny': 5027,
        'Sprzedaż': 5028,
        'Transport / Spedycja / Logistyka': 5031,
        'Ubezpieczenia': 5032,
        'Zakupy': 5033,
        'Zdrowie / Uroda / Rekreacja': 5035,
        'Inne': 5012
    }

    while True:
        try:
            page = get(
                f"https://www.pracuj.pl/praca/{cities[city]}?cc={categories[category]}?pn={page_number}"
            ).content
            bs = BeautifulSoup(page, 'html.parser')
            offers = bs.find('div', {'class': 'results', 'id': 'results'})

            scrap = offers.find_all('a', class_='offer__click-area')
            page_number += 1

            if len(scrap) == 0:
                break

            for item in scrap:
                links.append(item['href'])

        except Exception as e:
            logging.error(f'get_links_to_offers_pracuj: {e}')

    return links
