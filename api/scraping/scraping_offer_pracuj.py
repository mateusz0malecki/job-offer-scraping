from bs4 import BeautifulSoup
from requests import get
from datetime import date, timedelta

from models.model_job_offer import JobOffer
from models.model_extras import Responsibility, Requirement, Benefit


def scraping_pracuj(link):
    page = get(link).content
    bs = BeautifulSoup(page, 'html.parser')
    return bs


def scraping_job_offer_pracuj(db, link):
    offer_to_edit = JobOffer.get_offer_by_link(db, link)

    bs = scraping_pracuj(link)

    title = bs.find('h1', class_='offer-viewkHIhn3').get_text()
    company_name = bs.find('h2', class_='offer-viewwtdXJ4').get_text().split('O firmie')[0]

    value_from = bs.find('span', class_='offer-viewZGJhIB')
    earning_value_from = ''.join([i for i in value_from.get_text() if i.isdigit()]) if value_from else None
    value_to = bs.find('span', class_='offer-viewYo2KTr')
    earning_value_to = ''.join([i for i in value_to.get_text() if i.isdigit()]) if value_to else None

    contract_type = None
    seniority = None
    offer_deadline = None
    working_mode = None
    working_time = None
    remote_recruitment = None
    immediate_employment = None
    elements = bs.find_all('li', class_='offer-viewdQMogN')
    for element in elements:
        if element.find(
                'div',
                {'class': 'offer-viewXo2dpV', "data-test": 'sections-benefit-contracts-text'}
        ):
            contract_type = element.get_text()
        if element.find(
                'div',
                {'class': 'offer-viewXo2dpV', "data-test": 'sections-benefit-employment-type-name-text'}
        ):
            seniority = element.get_text()
        if element.find(
                'div',
                {'class': 'offer-viewXo2dpV', "data-test": 'sections-benefit-work-modes-text'}
        ):
            working_mode = element.get_text()
        if element.find(
                'div',
                {'class': 'offer-viewXo2dpV', "data-test": 'sections-benefit-work-schedule-text'}
        ):
            working_time = element.get_text()
        if element.find('div', class_='offer-view5VS8w0'):
            deadline = element.find(
                'div',
                {'class': 'offer-viewRKwqEV', "data-test": 'text-benefit'}
            ).get_text()
            days = ''.join([i for i in deadline if i.isdigit()])
            if len(days) == 0:
                offer_deadline = date.today() + timedelta(days=30)
            else:
                offer_deadline = date.today() + timedelta(days=int(days) - 1)
        if element.find('div', {"data-test": "sections-benefit-remote-recruitment-text"}):
            remote_recruitment = True
        if element.find('div', {"data-test": "sections-benefit-immediate-employment-text"}):
            immediate_employment = True

    responsibilities = []
    responsibilities_table = bs.find('div', {'class': 'offer-viewIPoRwg', "data-test": 'section-responsibilities'})
    if responsibilities_table:
        responsibilities_objects = responsibilities_table.find_all('p', {"class": "offer-viewchej5g"})
        for item in responsibilities_objects:
            responsibilities.append(item.get_text())

    requirements = []
    requirements_table = bs.find('div', {'class': 'offer-viewIPoRwg', "data-test": 'section-requirements'})
    if requirements_table:
        requirements_table_expected = requirements_table.find(
            'div',
            {"class": "offer-viewfjH4z3", "data-test": "section-requirements-expected"}
        )
        if requirements_table_expected:
            requirements_objects_expected = requirements_table_expected.find_all('p', {"class": "offer-viewchej5g"})
            for item in requirements_objects_expected:
                requirements.append(
                    {
                        "requirement": item.get_text(),
                        "must_have": True
                    }
                )
        requirements_table_optional = requirements_table.find(
            'div',
            {"class": "offer-viewfjH4z3", "data-test": "section-requirements-optional"}
        )
        if requirements_table_optional:
            requirements_objects_optional = requirements_table_optional.find_all('p', {"class": "offer-viewchej5g"})
            for item in requirements_objects_optional:
                requirements.append(
                    {
                        "requirement": item.get_text(),
                        "must_have": False
                    }
                )

    benefits = []
    benefits_table = bs.find('ul', class_="offer-view7CmY-p offer-viewF0WZVq")
    if benefits_table:
        benefits_objects = benefits_table.find_all(
            'p',
            {"class": "offer-view4bdC6U", "data-test": "text-benefit-title"}
        )
        for item in benefits_objects:
            benefits.append(item.get_text())

    responsibilities_to_add = []
    for responsibility in responsibilities:
        responsibility_to_add = Responsibility(
            responsibility=responsibility,
            job_offer_id=offer_to_edit.id
        )
        responsibilities_to_add.append(responsibility_to_add)

    requirements_to_add = []
    for requirement in requirements:
        requirement_to_add = Requirement(
            requirement=requirement.get("requirement"),
            must_have=requirement.get("must_have"),
            job_offer_id=offer_to_edit.id
        )
        requirements_to_add.append(requirement_to_add)

    benefits_to_add = []
    for benefit in benefits:
        benefit_to_add = Benefit(
            benefit=benefit,
            job_offer_id=offer_to_edit.id
        )
        benefits_to_add.append(benefit_to_add)

    db.add_all(responsibilities_to_add)
    db.add_all(requirements_to_add)
    db.add_all(benefits_to_add)
    db.commit()

    offer_to_edit.title = title
    offer_to_edit.company_name = company_name
    offer_to_edit.earning_value_from = earning_value_from
    offer_to_edit.earning_value_to = earning_value_to
    offer_to_edit.contract_type = contract_type
    offer_to_edit.seniority = seniority
    offer_to_edit.offer_deadline = offer_deadline
    offer_to_edit.working_mode = working_mode
    offer_to_edit.working_time = working_time
    offer_to_edit.remote_recruitment = remote_recruitment
    offer_to_edit.immediate_employment = immediate_employment
    db.commit()
    db.refresh(offer_to_edit)


def scrap_info_for_empty_offers_pracuj(db):
    empty_offers = JobOffer.get_empty_offers(db)
    for offer in empty_offers:
        scraping_job_offer_pracuj(db, offer.link)
