import logging

from celery import Task

from .celery import app
from db.database import db_session
from scraping.scraping_links_pracuj import get_links_to_offers_pracuj
from scraping.scraping_offer_pracuj import scrap_info_for_empty_offers_pracuj
from scraping.scraping_links_gowork import get_links_to_offers_gowork
from scraping.scraping_offer_gowork import scrap_info_for_empty_offers_gowork
from scraping.scraping_links_praca import get_links_to_offers_praca
from scraping.scraping_offer_praca import scrap_info_for_empty_offers_praca
from scraping.scraping_links_aplikuj import get_links_to_offers_aplikuj
from scraping.scraping_offer_aplikuj import scrap_info_for_empty_offers_aplikuj

logging.getLogger(__name__)

cities = [
        'Gdańsk',
        # 'Szczecin',
        # 'Białystok',
        # 'Toruń',
        # 'Bydgoszcz',
        # 'Olsztyn',
        # 'Warszawa',
        # 'Lublin',
        # 'Rzeszow',
        # 'Kraków',
        # 'Katowice',
        # 'Opole',
        # 'Wrocław',
        # 'Łódź',
        # 'Poznań',
        # 'Zielona Góra',
        # 'Gorzów Wielkopolski',
        # 'Kielce'
    ]


class SQLAlchemyTask(Task):
    """
    An abstract Celery Task that ensures that the connection the
    database is closed on task completion
    """
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.remove()


@app.task(name="get_links_pracuj", base=SQLAlchemyTask)
def get_links_pracuj():
    categories = [
        'Administracja biurowa',
        'Badania i rozwój',
        'Bankowość',
        'BHP / Ochrona środowiska',
        'Budownictwo',
        'Call Center',
        'Doradztwo / Konsulting',
        'Energetyka',
        'Edukacja / Szkolenia',
        'Finanse / Ekonomia',
        'Franczyza / Własny biznes',
        'Hotelarstwo / Gastronomia / Turystyka',
        'Human Resources / Zasoby ludzkie',
        'Internet / e-Commerce / Nowe media',
        'Inżynieria',
        'IT - Administracja',
        'IT - Rozwój oprogramowania',
        'Kontrola jakości',
        'Łańcuch dostaw',
        'Marketing',
        'Media / Sztuka / Rozrywka',
        'Nieruchomości',
        'Obsługa klienta',
        'Praca fizyczna',
        'Prawo',
        'Produkcja',
        'Public Relations',
        'Reklama / Grafika / Kreacja / Fotografia',
        'Sektor publiczny',
        'Sprzedaż',
        'Transport / Spedycja / Logistyka',
        'Ubezpieczenia',
        'Zakupy',
        'Zdrowie / Uroda / Rekreacja',
        'Inne'
    ]
    for city in cities:
        for category in categories:
            get_links_to_offers_pracuj(db_session, city, category)
    logging.info("DB filled with new links - pracuj.pl")


@app.task(name="get_offers_info_pracuj", base=SQLAlchemyTask)
def get_offers_info_pracuj():
    scrap_info_for_empty_offers_pracuj(db_session)
    logging.info("Offers filled with info - pracuj.pl")


@app.task(name="get_links_gowork", base=SQLAlchemyTask)
def get_links_gowork():
    categories = [
        'Administracja biurowa',
        'Badania i rozwój',
        'Bankowość',
        'BHP / Ochrona środowiska',
        'Budownictwo',
        'Call Center',
        'Edukacja / Szkolenia',
        'Finanse / Ekonomia',
        'Franczyza / Własny biznes',
        'Hotelarstwo / Gastronomia / Turystyka',
        'Human Resources / Zasoby ludzkie',
        'Inżynieria',
        'IT - Rozwój oprogramowania',
        'Kadra zarządzająca',
        'Kontrola jakości',
        'Marketing',
        'Media / Sztuka / Rozrywka',
        'Nieruchomości',
        'Opieka',
        'Opieka zdrowotna',
        'Praca fizyczna',
        'Praca za granicą',
        'Prawo',
        'Produkcja',
        'Reklama / Grafika / Kreacja / Fotografia',
        'Sprzedaż',
        'Transport / Spedycja / Logistyka',
        'Ubezpieczenia',
        'Zdrowie / Uroda / Rekreacja'
    ]
    for city in cities:
        for category in categories:
            get_links_to_offers_gowork(db_session, city, category)
    logging.info("DB filled with new links - gowork.pl")


@app.task(name="get_offers_info_gowork", base=SQLAlchemyTask)
def get_offers_info_gowork():
    scrap_info_for_empty_offers_gowork(db_session)
    logging.info("Offers filled with info - gowork.pl")


@app.task(name="get_links_praca", base=SQLAlchemyTask)
def get_links_praca():
    categories = [
        'Administracja biurowa',
        'Administracja publiczna / Służba publiczna',
        'Architektura',
        'Badania i rozwój',
        'BHP / Ochrona środowiska',
        'Budownictwo',
        'Doradztwo / Konsulting',
        'Energetyka',
        'Edukacja / Szkolenia',
        'Farmaceutyka / Biotechnologia',
        'Finanse / Ekonomia',
        'Franczyza / Własny biznes',
        'Gastronomia / Catering',
        'Hotelarstwo / Gastronomia / Turystyka',
        'Human Resources / Zasoby ludzkie',
        'Internet / e-Commerce / Nowe media',
        'Inżynieria',
        'IT - Administracja',
        'IT - Rozwój oprogramowania',
        'Kadra zarządzająca',
        'Kontrola jakości',
        'Księgowość',
        'Łańcuch dostaw',
        'Marketing',
        'Montaż / Serwis / Technika',
        'Motoryzacja',
        'Nieruchomości',
        'Ochrona osób i mienia',
        'Opieka zdrowotna',
        'Praca fizyczna',
        'Prawo',
        'Produkcja',
        'Reklama / Grafika / Kreacja / Fotografia',
        'Sport',
        'Sprzedaż',
        'Telekomunikacja',
        'Tłumaczenia',
        'Transport / Spedycja / Logistyka',
        'Ubezpieczenia',
        'Zakupy',
        'Zdrowie / Uroda / Rekreacja'
    ]
    for city in cities:
        for category in categories:
            get_links_to_offers_praca(db_session, city, category)
    logging.info("DB filled with new links - praca.pl")


@app.task(name="get_offers_info_praca", base=SQLAlchemyTask)
def get_offers_info_praca():
    scrap_info_for_empty_offers_praca(db_session)
    logging.info("Offers filled with info - praca.pl")


@app.task(name="get_links_aplikuj", base=SQLAlchemyTask)
def get_links_aplikuj():
    categories = [
        'Administracja biurowa',
        # 'Administracja publiczna / Służba publiczna',
        # 'Badania i rozwój',
        # 'BHP / Ochrona środowiska',
        # 'Budownictwo',
        # 'Call Center',
        # 'Doradztwo / Konsulting',
        # 'Energetyka',
        # 'Edukacja / Szkolenia',
        # 'Finanse / Ekonomia',
        # 'Franczyza / Własny biznes',
        # 'Hotelarstwo / Gastronomia / Turystyka',
        # 'Human Resources / Zasoby ludzkie',
        # 'Internet / e-Commerce / Nowe media',
        # 'Inżynieria',
        # 'IT - Rozwój oprogramowania',
        # 'Kadra zarządzająca',
        # 'Księgowość',
        # 'Łańcuch dostaw',
        # 'Marketing',
        # 'Montaż / Serwis / Technika',
        # 'Motoryzacja',
        # 'Nieruchomości',
        # 'Opieka zdrowotna',
        # 'Praca fizyczna',
        # 'Prawo',
        # 'Produkcja',
        # 'Reklama / Grafika / Kreacja / Fotografia',
        # 'Rolnictwo',
        # 'Rzemiosło',
        # 'Sport',
        # 'Sprzedaż',
        # 'Sztuka / Rozrywka / Rekreacja / Projektowanie',
        # 'Telekomunikacja',
        # 'Transport / Spedycja / Logistyka',
        # 'Ubezpieczenia',
        # 'Zdrowie / Uroda / Rekreacja',
        # 'Inne',
    ]
    for city in cities:
        for category in categories:
            get_links_to_offers_aplikuj(db_session, city, category)
    logging.info("DB filled with new links - aplikuj.pl")


@app.task(name="get_offers_info_aplikuj", base=SQLAlchemyTask)
def get_offers_info_aplikuj():
    scrap_info_for_empty_offers_aplikuj(db_session)
    logging.info("Offers filled with info - aplikuj.pl")
