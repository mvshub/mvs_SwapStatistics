import sys
import json
import time

from mvs_rpc import mvs_api as mvs_rpc
from etherscan.tokens import Tokens
from etherscan.proxies import Proxies
API_KEY = '3WSKI5YSSVJP1JA8S6WZ5PPVT71AHGGPI8'
eth_address = "0xc1e5fd24fa2b4a3581335fc3f2850f717dd09c86"

import app

def get_mvs_height():
    em, height = mvs_rpc.getheight()
    assert (em == None)
    return height

def get_mvs_token_circulation(token):
    '''
    get token in circulation(expect the issue account) on mvs
    '''
    em, result = mvs_rpc.getasset(token)
    assert( em == None)

    total_supply = sum( [i["maximum_supply"] for i in result if i["status"] == "issued"] )

    global mvs_address
    em, result = mvs_rpc.getaddressasset(mvs_address, symbol=token)

    assert (em == None)
    frozen = sum([  (i["locked_quantity"] + i["quantity"]) for i in result ])
    return total_supply - frozen

def get_eth_height():
    proxy = Proxies(api_key=API_KEY)
    return int(proxy.get_most_recent_block(), 16)

def get_eth_token_deposit(token_cfg):
    api = Tokens(contract_address=token_cfg['address'], api_key=API_KEY)
    balance = int( api.get_token_balance(eth_address) )
    if token_cfg["decimal"] > 8:
        return int(balance / (10 ** (token_cfg["decimal"] - 8)))
    else:
        return int(balance)

def draw(token_class):
    # just show latest 24 hours ?
    from_ = int(time.time()) - 24 * 60 * 60
    objs = app.db.session.query(token_class).filter(token_class.timestamp >= from_).order_by(
        token_class.iden.desc()).all()
    x = []  # the timestamp
    y1 = []  # Metaverse
    y2 = []  # Ethereum
    for obj in objs:
        x.append(obj.timestamp)
        y1.append(obj.circulation)
        y2.append(obj.deposit)

    import matplotlib.pyplot as plt
    #group_labels = ['64k', '128k', '256k', '512k', '1024k', '2048k', '4096k', '8M', '16M', '32M', '64M', '128M', '256M',
    #                '512M']
    plt.title('Token:%s -- Metaverse vs Ethereum' % token_class.__tablename__)
    plt.xlabel('time(s)')
    plt.ylabel('Token Balance(wei)')

    plt.plot(x, y1, 'r', label='Metaverse')
    plt.plot(x, y2, 'b', label='Ethereum')
    #plt.xticks(x, group_labels, rotation=0)
    plt.legend(bbox_to_anchor=[0.3, 1])
    plt.grid()
    plt.show()

def main():
    token_class_lst = app.init_app()
    while True:
        now = int(time.time())
        heightM = get_mvs_height()
        heightE = get_eth_height()
        for token_class in token_class_lst:
            last_records = app.db.session.query(token_class).order_by(token_class.iden.desc()).limit(2).all()

            new_record = token_class()
            new_record.timestamp = now
            new_record.heightM = heightM
            new_record.heightE = heightE
            new_record.circulation = get_mvs_token_circulation('ERC20.'+token_class.__tablename__)
            new_record.deposit = get_eth_token_deposit(token_class.contract_cfg)

            if len(last_records) == 2:
                # with the same balance
                if new_record == last_records[0] and last_records[0] == last_records[1]:
                    last_records[0].timestamp = new_record.timestamp
                    last_records[0].heightM = new_record.heightM
                    last_records[0].heightE = new_record.heightE
                    app.db.session.add(last_records[0])
                    app.db.session.commit()
                    continue

            app.db.session.add(new_record)
            app.db.session.commit()
        time.sleep(10)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        mvs_address = [i['address'] for i in mvs_rpc.getdid("droplet")[1] if i['status'] == 'current'][0]
        main()
    elif sys.argv[1] == 'draw':
        token_class_lst = app.init_app()
        for token_class in token_class_lst:
            draw(token_class)

