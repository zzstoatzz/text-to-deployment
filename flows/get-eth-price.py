from prefect import flow

@flow
def get_eth_price():
    import requests
    response = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
    eth_price = response.json()['data']['amount']
    return float(eth_price)