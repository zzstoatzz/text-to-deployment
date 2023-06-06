def get_eth_price():
    import httpx
    response = httpx.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
    price = response.json()['data']['amount']
    print(f'ETH price in USD: {price}')