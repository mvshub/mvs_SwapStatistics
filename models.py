import copy
import json
from app import db

class Token(object):
    @classmethod
    def load_contract(cls):
        contract_file = './config/%s.json' % cls.__tablename__
        with open(contract_file) as f:
            cls.contract_cfg = json.load(f)


def __eq__(self, other):
    if not other:
        return False
    return (self.circulation, self.deposit) == (other.circulation, other.deposit)

class_template = {
    'iden' : db.Column(db.Integer, primary_key=True, autoincrement=True),

    # the time when the statistics was executed
    'timestamp' : db.Column(db.Integer),

    # the block height of mvs
    'heightM' : db.Column(db.Integer),

    # the asset quantity in circulation (except the 'crosschain' address) on metaverse chain
    'circulation' : db.Column(db.BigInteger),#db.Column(db.Numeric(64, 18), nullable=False),

    # the block height of ethereum
    'heightE' : db.Column(db.Integer),

    # the token quantity locked by the swap address on ethereum chain
    'deposit' : db.Column(db.BigInteger),#db.Column(db.Numeric(64, 18), nullable=False),

    '__eq__':__eq__
}

def init_db():
    tokens = ['EDU', ]
    ret = []
    for token in tokens:
        classdict = {'__tablename__': token }
        classdict.update( copy.deepcopy(class_template) )
        classobj = type(token, (db.Model, Token), classdict)
        classobj.load_contract()
        ret.append(classobj)

    # db.drop_all()
    db.create_all()
    return ret

