from fastapi import APIRouter, Depends, status, Path, Query
from sqlalchemy.orm import Session

from db.database import get_db
from models.model_job_offer import JobOffer
from schemas import offers_schemas
from exceptions import exceptions

router = APIRouter(tags=['Job offers'])


@router.get(
    "/job-offers",
    status_code=status.HTTP_200_OK
)
async def get_offers(
        db: Session = Depends(get_db),
        page: int = Query(default=1),
        page_size: int = Query(default=20),
        city: str | None = Query(default=None),
        category: str | None = Query(default=None),
        earning_value_from: int | None = Query(default=None),
        earning_value_to: int | None = Query(default=None),
        remote_recruitment: bool | None = Query(default=None),
        immediate_employment: bool | None = Query(default=None),
):
    """
    Returns list of estates that matches used filter query parameters.
    Pagination included.
    """

    queryset = db.query(JobOffer)

    cities = {
        'gdansk': 'Gdańsk',
        'szczecin': 'Szczecin',
        'bialystok': 'Białystok',
        'torun': 'Toruń',
        'bydgoszcz': 'Bydgoszcz',
        'olsztyn': 'Olsztyn',
        'warszawa': 'Warszawa',
        'lublin': 'Lublin',
        'rzeszow': 'Rzeszow',
        'krakow': 'Kraków',
        'katowice': 'Katowice',
        'opole': 'Opole',
        'wroclaw': 'Wrocław',
        'lodz': 'Łódź',
        'poznan': 'Poznań',
        'zielona-gora': 'Zielona Góra',
        'gorzow-wielkopolski': 'Gorzów Wielkopolski',
        'kielce': 'Kielce'
    }

    categories = {
        'administracja-biurowa': 'Administracja biurowa',
        'badania-i-rozwój': 'Badania i rozwój',
        'bankowość': 'Bankowość',
        'bhp-ochrona-środowiska': 'BHP / Ochrona środowiska',
        'budownictwo': 'Budownictwo',
        'call-center': 'Call Center',
        'doradztwo-konsulting': 'Doradztwo / Konsulting',
        'energetyka': 'Energetyka',
        'edukacja-szkolenia': 'Edukacja / Szkolenia',
        'finanse-ekonomia': 'Finanse / Ekonomia',
        'franczyza-własny-biznes': 'Franczyza / Własny biznes',
        'hotelarstwo-gastronomia-turystyka': 'Hotelarstwo / Gastronomia / Turystyka',
        'human-resources-zasoby-ludzkie': 'Human Resources / Zasoby ludzkie',
        'internet-e-commerce-nowe-media': 'Internet / e-Commerce / Nowe media',
        'inżynieria': 'Inżynieria',
        'it-administracja': 'IT - Administracja',
        'it-rozwój-oprogramowania': 'IT - Rozwój oprogramowania',
        'kontrola-jakości': 'Kontrola jakości',
        'łańcuch-dostaw': 'Łańcuch dostaw',
        'marketing': 'Marketing',
        'media-sztuka-rozrywka': 'Media / Sztuka / Rozrywka',
        'nieruchomości': 'Nieruchomości',
        'obsługa-klienta': 'Obsługa klienta',
        'praca-fizyczna': 'Praca fizyczna',
        'prawo': 'Prawo',
        'produkcja': 'Produkcja',
        'public-relations': 'Public Relations',
        'reklama-grafika-kreacja-fotografia': 'Reklama / Grafika / Kreacja / Fotografia',
        'sektor-publiczny': 'Sektor publiczny',
        'sprzedaż': 'Sprzedaż',
        'transport-spedycja-logistyka': 'Transport / Spedycja / Logistyka',
        'ubezpieczenia': 'Ubezpieczenia',
        'zakupy': 'Zakupy',
        'zdrowie-uroda-rekreacja': 'Zdrowie / Uroda / Rekreacja',
        'inne': 'Inne'
    }

    if city:
        queryset = queryset.filter(JobOffer.city == cities[city])
    if category:
        queryset = queryset.filter(JobOffer.category == categories[category])
    if earning_value_from:
        queryset = queryset.filter(JobOffer.earning_value_from <= earning_value_from)
    if earning_value_to:
        queryset = queryset.filter(JobOffer.earning_value_from >= earning_value_to)
    if remote_recruitment:
        queryset = queryset.filter(JobOffer.remote_recruitment == remote_recruitment)
    if immediate_employment:
        queryset = queryset.filter(JobOffer.immediate_employment == immediate_employment)

    first = (page - 1) * page_size
    last = first + page_size
    response = offers_schemas.JobOfferPagination(
        queryset.all(),
        first,
        last,
        page,
        page_size
    )
    return response


@router.get(
    "/job-offers/{offer_id}",
    status_code=status.HTTP_200_OK,
    response_model=offers_schemas.JobOffer
)
async def get_offer_detail(
        offer_id: int = Path(description="Id of specific offer"),
        db: Session = Depends(get_db)
):
    """
    Displays all available data about chosen offer.
    """
    offer = JobOffer.get_offer_by_id(db, offer_id)
    if not offer:
        raise exceptions.OfferNotFound(offer_id)
    return offer
