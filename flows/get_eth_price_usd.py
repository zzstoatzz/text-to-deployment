from prefect import flow

@flow
def get_eth_price_usd():
    import requests

    url = 'https://api.coinbase.com/v2/prices/ETH-USD/spot'
    response = requests.get(url)
    data = response.json()
    return float(data['data']['amount'])