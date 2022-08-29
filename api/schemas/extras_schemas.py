from .helpers_schemas import BaseConfig


class ResponsibilityBase(BaseConfig):
    responsibility: str


class RequirementBase(BaseConfig):
    requirement: str
    must_have: bool


class BenefitBase(BaseConfig):
    benefit: str
