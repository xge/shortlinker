from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String

Base = declarative_base()

class Redirect(Base):
    __tablename__ = 'redirects'

    slug = Column(String(255), primary_key=True, unique=True)
    target = Column(String(512), nullable=False)
    expiration_date = Column(DateTime)

    def __repr__(self):
        return '<Redirect(slug=\'{}\', target=\'{}\', expiration_date=\'{}\')>'.format(self.slug, self.target, self.expiration_date)
