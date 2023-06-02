from prefect import flow

@flow
def fetch_eth_price_usd():
    import requests
    response = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
    eth_price_usd = float(response.json()['data']['amount'])
    return eth_price_usd