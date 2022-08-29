from .helpers_schemas import BaseConfig, OffersPagination
from .extras_schemas import BenefitBase, RequirementBase, ResponsibilityBase
from datetime import date


class JobOfferBase(BaseConfig):
    id: int
    city: str
    category: str
    title: str
    company_name: str | None
    earning_value_from: int | None
    earning_value_to: int | None
    contract_type: str | None
    seniority: str | None
    offer_deadline: date | None
    working_mode: str | None
    working_time: str | None
    remote_recruitment: bool | None
    immediate_employment: bool | None


class JobOfferPagination(OffersPagination):
    records: list[JobOfferBase] = []


class JobOffer(JobOfferBase):
    responsibilities: list[ResponsibilityBase] = []
    requirements: list[RequirementBase] = []
    benefits: list[BenefitBase] = []
