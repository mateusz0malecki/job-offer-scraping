from bs4 import BeautifulSoup
from requests import get

from models.model_job_offer import JobOffer


def scraping(link):
    page = get(link).content
    bs = BeautifulSoup(page, 'html.parser')
    return bs


def scraping_job_offer_gowork(db, link):
    offer_to_edit = JobOffer.get_offer_by_link(db, link)

    bs = scraping(link)

    company_name = None
    earning_value_from = None
    earning_value_to = None
    contract_type = None
    working_mode = None
    working_time = None
    remote_recruitment = None

    title = bs.find('h1', class_='job-offer-header__title').get_text().strip()

    if bs.find('div', class_='job-offer-header__links'):
        company_name = bs.find('div', class_='job-offer-header__links').get_text().split('(')[0].strip()

    job_offer_tags = bs.find_all('div', class_='g-job-offer-tags')

    for tag in job_offer_tags:
        if tag.find('img', src="/_nuxt/img/contract.eb1bde1.svg"):
            contract_type = tag.get_text().strip()
        if tag.find('img', src='/_nuxt/img/time.64eae53.svg'):
            working_time = tag.get_text().strip()
        if tag.find('img', src='data:image/svg+xml;base64,PCEtLSBHZW5lcmF0ZWQgYnkgSWNvTW9vbi5pbyAtLT4KPHN2ZyB2ZXJzaW9uP'
                               'SIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiB2'
                               'aWV3Qm94PSIwIDAgMzIgMzIiPgo8dGl0bGU+aG9tZTwvdGl0bGU+CjxwYXRoIGZpbGw9IiM0OTUwNTciIGQ9Ik0'
                               'zMS42NiAxMy4wMDRsLTE1LjE2OC0xMS4xMDZjLTAuMjkzLTAuMjE0LTAuNjktMC4yMTQtMC45ODIgMGwtMTUuMT'
                               'Y5IDExLjEwNmMtMC4zNyAwLjI3MS0wLjQ1MSAwLjc5Mi0wLjE4IDEuMTYyczAuNzkyIDAuNDUxIDEuMTYyIDAuM'
                               'ThsMTQuNjc3LTEwLjc0NiAxNC42NzcgMTAuNzQ2YzAuMTQ4IDAuMTA4IDAuMzIgMC4xNjEgMC40OTEgMC4xNjEg'
                               'MC4yNTYgMCAwLjUwOS0wLjExOCAwLjY3MS0wLjM0IDAuMjcxLTAuMzcgMC4xOTEtMC44OTEtMC4xOC0xLjE2Mnp'
                               'NMjcuNjQgMTQuNTM0Yy0wLjQ1OSAwLTAuODMxIDAuMzcyLTAuODMxIDAuODMxdjEzLjIzNGgtNi42NTF2LTcuMj'
                               'I0YzAtMi4yOTMtMS44NjUtNC4xNTctNC4xNTctNC4xNTdzLTQuMTU3IDEuODY1LTQuMTU3IDQuMTU3djcuMjI0a'
                               'C02LjY1MXYtMTMuMjM0YzAtMC40NTktMC4zNzItMC44MzEtMC44MzEtMC44MzFzLTAuODMxIDAuMzcyLTAuODMx'
                               'IDAuODMxdjE0LjA2NmMwIDAuNDU5IDAuMzcyIDAuODMxIDAuODMxIDAuODMxaDguMzE0YzAuNDM3IDAgMC43OTU'
                               'tMC4zMzggMC44MjgtMC43NjcgMC4wMDItMC4wMTkgMC4wMDMtMC4wNDEgMC4wMDMtMC4wNjV2LTguMDU2YzAtMS'
                               '4zNzYgMS4xMTktMi40OTUgMi40OTUtMi40OTVzMi40OTUgMS4xMTkgMi40OTUgMi40OTV2OC4wNTZjMCAwLjAyN'
                               'CAwLjAwMSAwLjA0NSAwLjAwMyAwLjA2NCAwLjAzMyAwLjQyOSAwLjM5MSAwLjc2NyAwLjgyOCAwLjc2N2g4LjMx'
                               'NGMwLjQ1OSAwIDAuODMxLTAuMzcyIDAuODMxLTAuODMxdi0xNC4wNjZjLTAtMC40NTktMC4zNzItMC44MzItMC4'
                               '4MzEtMC44MzJ6Ij48L3BhdGg+Cjwvc3ZnPgo='):
            working_mode = tag.get_text().strip()

    if bs.find('div', class_='job-salary'):
        salary = bs.find('div', class_='job-salary').get_text()

        value_from = salary.split('-')[0].strip()
        earning_value_from = int(''.join([i for i in value_from if i.isdigit()]))
        if len(salary.split('-')) > 1:
            value_to = salary.split('-')[1].strip().split(' ')[0]
            earning_value_to = int(''.join([i for i in value_to if i.isdigit()]))

        if earning_value_from < 300:
            earning_value_from *= 160

    if bs.find('div', class_='job-online-interview'):
        remote_recruitment = True

    offer_to_edit.title = title
    offer_to_edit.company_name = company_name
    offer_to_edit.earning_value_from = earning_value_from
    offer_to_edit.earning_value_to = earning_value_to
    offer_to_edit.contract_type = contract_type
    offer_to_edit.working_mode = working_mode
    offer_to_edit.working_time = working_time
    offer_to_edit.remote_recruitment = remote_recruitment
    db.commit()
    db.refresh(offer_to_edit)


def scrap_info_for_empty_offers_gowork(db):
    empty_offers = JobOffer.get_empty_offers(db).filter(JobOffer.link.contains('www.gowork.pl')).all()
    for offer in empty_offers:
        scraping_job_offer_gowork(db, offer.link)
