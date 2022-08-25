from sqlalchemy import Column, String, Integer, ForeignKey, Boolean

from db.database import Base


class Responsibility(Base):
    __tablename__ = "responsibility"
    id = Column(Integer, primary_key=True, index=True)
    responsibility = Column(String(512))
    job_offer_id = Column(Integer, ForeignKey("job_offer.id", ondelete="CASCADE"))


class Requirement(Base):
    __tablename__ = "requirement"
    id = Column(Integer, primary_key=True, index=True)
    requirement = Column(String(512))
    must_have = Column(Boolean)
    job_offer_id = Column(Integer, ForeignKey("job_offer.id", ondelete="CASCADE"))


class Benefit(Base):
    __tablename__ = "benefit"
    id = Column(Integer, primary_key=True, index=True)
    benefit = Column(String(512))
    job_offer_id = Column(Integer, ForeignKey("job_offer.id", ondelete="CASCADE"))
