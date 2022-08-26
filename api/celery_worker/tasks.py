import logging

from celery import Task

from .celery import app
from db.database import db_session
from scraping.scraping_links_pracuj import get_links_to_offers_pracuj
from scraping.scraping_offer_pracuj import scrap_info_for_empty_offers_pracuj
from scraping.scraping_links_gowork import get_links_to_offers_gowork

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
    An abstract Celery Task that ensures that the connection the the
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
        # 'Administracja biurowa',
        # 'Badania i rozwój',
        # 'Bankowość',
        # 'BHP / Ochrona środowiska',
        # 'Budownictwo',
        # 'Call Center',
        # 'Edukacja / Szkolenia',
        # 'Finanse / Ekonomia',
        # 'Franczyza / Własny biznes',
        # 'Hotelarstwo / Gastronomia / Turystyka',
        # 'Human Resources / Zasoby ludzkie',
        # 'Inżynieria',
        # 'IT - Rozwój oprogramowania',
        # 'Kadra zarządzająca',
        # 'Kontrola jakości',
        # 'Marketing',
        # 'Media / Sztuka / Rozrywka',
        # 'Nieruchomości',
        # 'Opieka',
        # 'Opieka zdrowotna',
        # 'Praca fizyczna',
        # 'Praca za granicą',
        # 'Prawo',
        # 'Produkcja',
        # 'Reklama / Grafika / Kreacja / Fotografia',
        # 'Sprzedaż',
        # 'Transport / Spedycja / Logistyka',
        # 'Ubezpieczenia',
        'Zdrowie / Uroda / Rekreacja'
    ]
    for city in cities:
        for category in categories:
            get_links_to_offers_gowork(db_session, city, category)
    logging.info("DB filled with new links - gowork.pl")
