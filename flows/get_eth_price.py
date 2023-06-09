from prefect import flow

@flow(log_prints=True)
def get_eth_price():
    import httpx
    response = httpx.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
    price = response.json()['data']['amount']
    print(f'ETH price in USD: {price}')

if __name__ == "__main__":
    get_eth_price()