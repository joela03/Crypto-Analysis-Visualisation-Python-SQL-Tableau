import requests


def get_crypto_info(crypto_id: str) -> list[dict]:
    """Get's information for a crypto currency from the Coingecko API"""
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin{
        crypto_id}"

    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request fails
    data = response.json()
    return data
