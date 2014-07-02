from .model import *

class Account(Versioned, Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(Enum("user", "placeholder", name="account_type"), nullable=False)
    balance = Column(Numeric, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __mapper_args__ = {'polymorphic_on':type}

    def __init__(self, name, balance=0.0):
        self.name = name
        self.balance = balance


class PlaceholderAccount(Account):
    __mapper_args__ = {'polymorphic_identity': 'placeholder'}


def make_account(name):
    t = DBSession.query(PlaceholderAccount).filter(PlaceholderAccount.name == name).first()
    if t:
        return t
    t = PlaceholderAccount(name)
    DBSession.add(t)
    DBSession.flush()
    return t
