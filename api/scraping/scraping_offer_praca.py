from bs4 import BeautifulSoup
from requests import get

from models.model_job_offer import JobOffer


def scraping(link):
    page = get(link).content
    bs = BeautifulSoup(page, 'html.parser')
    return bs


def scraping_job_offer_praca(db, link):
    offer_to_edit = JobOffer.get_offer_by_link(db, link)

    bs = scraping(link)

    company_name = None
    contract_type = None
    working_time = None
    seniority = None
    remote_recruitment = None
    earning_value_from = None
    earning_value_to = None

    title = bs.find('div', class_='app-offer__title').get_text().strip()

    company_name_div = bs.find('div', class_='app-offer__main-item app-offer__main-item--employer')
    if company_name_div:
        company_name = company_name_div.get_text().split('Profil firmy')[0].strip()

    seniority_div = bs.find('div', class_='app-offer__header-item app-offer__header-item--job-level')
    if seniority_div:
        seniority = seniority_div.get_text().strip()

    working_time_div = bs.find('div', class_='app-offer__header-item app-offer__header-item--working-time')
    if working_time_div:
        working_time = working_time_div.get_text().strip()

    contract_type_div = bs.find('div', class_='app-offer__header-item app-offer__header-item--employment-type')
    if contract_type_div:
        contract_type = contract_type_div.get_text().strip()

    remote_recruitment_div = bs.find('div', class_='app-offer__header-item app-offer__header-item--online-recruitment')
    if remote_recruitment_div:
        remote_recruitment = True

    salary_div = bs.find('div', class_='app-offer__salary')
    if salary_div:
        salary_text = salary_div.get_text().strip().split('-')
        earning_value_from = int(''.join([i for i in salary_text[0].split(',')[0] if i.isdigit()]))
        earning_value_to = int(''.join([i for i in salary_text[1].split(',')[0] if i.isdigit()]))
        if earning_value_from < 300:
            earning_value_from *= 160
        if earning_value_to < 300:
            earning_value_to *= 160

    offer_to_edit.title = title
    offer_to_edit.company_name = company_name
    offer_to_edit.contract_type = contract_type
    offer_to_edit.working_time = working_time
    offer_to_edit.seniority = seniority
    offer_to_edit.remote_recruitment = remote_recruitment
    offer_to_edit.earning_value_from = earning_value_from
    offer_to_edit.earning_value_to = earning_value_to
    db.commit()
    db.refresh(offer_to_edit)


def scrap_info_for_empty_offers_praca(db):
    empty_offers = JobOffer.get_empty_offers(db).filter(JobOffer.link.contains('www.praca.pl')).all()
    for offer in empty_offers:
        scraping_job_offer_praca(db, offer.link)
