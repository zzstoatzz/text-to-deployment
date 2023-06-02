from prefect import flow

@flow
def fetch_eth_price():
    import requests
    response = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
    data = response.json()
    price = data['data']['amount']
    return price