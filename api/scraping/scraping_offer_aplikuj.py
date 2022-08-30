from bs4 import BeautifulSoup
from requests import get
from datetime import date, timedelta

from models.model_job_offer import JobOffer
from models.model_extras import Responsibility, Requirement, Benefit


def scraping(link):
    page = get(link).content
    bs = BeautifulSoup(page, 'html.parser')
    return bs


def scraping_job_offer_aplikuj(db, link):
    offer_to_edit = JobOffer.get_offer_by_link(db, link)

    bs = scraping(link)
    title = None
    company_name = None
    contract_type = None
    working_mode = None
    working_time = None
    remote_recruitment = None
    immediate_employment = None
    earning_value_from = None
    earning_value_to = None
    offer_deadline = None
    responsibilities = []
    requirements = []
    benefits = []

    if bs.find('section', class_='relative md:container md:max-w-7xl md:mx-auto md:-mt-14 md:mb-24 z-30'):
        if bs.find('h1'):
            title = bs.find('h1').get_text().strip()
        company_name_cursor = bs.find('a', class_='text-primary sm:hover:underline font-semibold')
        if company_name_cursor:
            company_name = company_name_cursor.get_text().strip()

        earning_values_cursor = bs.find('div', class_='md:pb-4')
        if earning_values_cursor:
            text = earning_values_cursor.get_text().split('-')
            earning_value_from = int(''.join([i for i in text[0] if i.isdigit()]))
            earning_value_to = int(''.join([i for i in text[1] if i.isdigit()]))
            if earning_value_to < 300:
                earning_value_to *= 160
            if earning_value_from < 300:
                earning_value_from *= 160

        offer_deadline_cursor = bs.find('div', class_='space-y-2 md:py-6')
        items = offer_deadline_cursor.find_all('div', class_='flex items-center')
        for item in items:
            text = item.get_text().strip()
            if text.startswith('Wygasa'):
                days = ''.join([i for i in text.split('(')[1] if i.isdigit()])
                try:
                    offer_deadline = date.today() + timedelta(int(days))
                except ValueError:
                    offer_deadline = date.today()

        elements = bs.find_all('div', class_='relative flex items-center space-x-3')
        for element in elements:
            if element.find('svg', class_='svg-inline--fa fa-file-signature fa-lg'):
                contract_type = element.get_text().strip()
            if element.find('svg', class_='svg-inline--fa fa-chart-pie-alt fa-lg'):
                working_time = element.get_text().strip()
            if element.find('svg', class_='svg-inline--fa fa-home-lg-alt fa-lg'):
                working_mode = element.get_text().strip()
            if element.find('svg', class_='svg-inline--fa fa-video fa-lg'):
                remote_recruitment = True
            if element.find('svg', class_='svg-inline--fa  fa-lg'):
                immediate_employment = True

        extras_cursor = bs.find('div', class_='pt-6')
        if extras_cursor:
            extras = extras_cursor.find_all('div', class_='pb-12')
            for item in extras:
                items = item.find_all('li', class_='leading-6 flex py-1')
                if item == extras[0]:
                    for i in items:
                        responsibilities.append(i.get_text().strip())
                if item == extras[1]:
                    for i in items:
                        requirements.append(i.get_text().strip())
                if item == extras[2]:
                    for i in items:
                        benefits.append(i.get_text().strip())

        more_benefits_cursor = bs.find_all(
            'div',
            'col-span-1 flex flex-col justify-center py-4 px-4 md:py-8 md:px-8 bg-gray-50 text-center'
        )
        for i in more_benefits_cursor:
            benefits.append(i.get_text().strip())

    if bs.find('section', class_='relative md:container md:max-w-4xl md:mx-auto md:-mt-14 md:mb-24 z-30'):
        if bs.find('h1'):
            span = bs.find('h1').find('span', id='uwagiDoStanowiska')
            if span:
                title = bs.find('h1').get_text().strip().split(span.get_text())[0]
            else:
                title = bs.find('h1').get_text().strip()

        company_name_cursor = bs.find('div', class_='o-icon-box')
        if company_name_cursor:
            elements = company_name_cursor.find_all('div', class_='o-icon-box__body')
            for item in elements:
                if item.find('div', class_='o-icon-box__title').get_text() == 'Pracodawca':
                    company_name = item.find('div', class_='o-icon-box__data').get_text().strip()

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
            requirement=requirement,
            must_have=True,
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
    offer_to_edit.offer_deadline = offer_deadline
    offer_to_edit.working_mode = working_mode
    offer_to_edit.working_time = working_time
    offer_to_edit.remote_recruitment = remote_recruitment
    offer_to_edit.immediate_employment = immediate_employment
    db.commit()
    db.refresh(offer_to_edit)


def scrap_info_for_empty_offers_aplikuj(db):
    empty_offers = JobOffer.get_empty_offers(db).filter(JobOffer.link.contains('www.aplikuj.pl')).all()
    for offer in empty_offers:
        scraping_job_offer_aplikuj(db, offer.link)
