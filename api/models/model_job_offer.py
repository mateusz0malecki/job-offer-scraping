from sqlalchemy import Column, String, Integer, DateTime, Date, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class JobOffer(Base):
    __tablename__ = "job_offer"
    id = Column(Integer, primary_key=True, index=True)
    link = Column(String(256))
    city = Column(String(64))
    category = Column(String(64))
    title = Column(String(256))
    company_name = Column(String(256))
    earning_value_from = Column(Integer)
    earning_value_to = Column(Integer)
    contract_type = Column(String(64))
    seniority = Column(String(64))
    offer_deadline = Column(Date)
    working_mode = Column(String(64))
    working_time = Column(String(64))
    remote_recruitment = Column(Boolean)
    immediate_employment = Column(Boolean)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    responsibilities = relationship("Responsibilities", backref="job_offer", cascade="all, delete-orphan")
    requirements = relationship("Requirements", backref="job_offer", cascade="all, delete-orphan")
    benefits = relationship("Benefits", backref="job_offer", cascade="all, delete-orphan")

    @staticmethod
    def get_offer_by_link(db, link):
        return db.query(JobOffer).filter(JobOffer.link == link).first()

    @staticmethod
    def get_empty_offers(db):
        return db.query(JobOffer).filter(JobOffer.title == None).all()
