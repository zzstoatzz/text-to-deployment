from prefect import flow

@flow
def _ai_imputer_base(context: str) -> cls:
    import requests
    from time import sleep

    def get_eth_price():
        url = 'https://api.coinbase.com/v2/exchange-rates?currency=ETH'
        response = requests.get(url)
        data = response.json()
        return float(data['data']['rates']['USD'])

    def track_eth_price():
        while True:
            eth_price = get_eth_price()
            print(f'ETH Price in USD: {eth_price}')
            sleep(300)

    return track_eth_price