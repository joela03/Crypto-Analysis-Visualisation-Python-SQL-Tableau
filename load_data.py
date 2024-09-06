import os
from dotenv import load_dotenv
import requests
import random
import time
import psycopg2
import psycopg2.extras
import json

load_dotenv()


def fetch_crypto_ids():
    """Fetch cryptocurrency IDs from CoinGecko API."""
    url = "https://api.coingecko.com/api/v3/coins/list"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        crypto_ids = [crypto['id'] for crypto in data]
        return crypto_ids
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


def select_random_crypto_ids(crypto_ids, num_samples=50) -> list[str]:
    """Select a random sample of cryptocurrency IDs."""
    if len(crypto_ids) < num_samples:
        print(f"""Warning: Only {
              len(crypto_ids)} cryptocurrency IDs available. Adjusting sample size.""")
        num_samples = len(crypto_ids)

    return random.sample(crypto_ids, num_samples)


def get_crypto_info(crypto_id: str) -> dict:
    """Get's information for a crypto currency from the Coingecko API"""
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={
        crypto_id}"

    headers = {
        'Authorization': f'Bearer {os.getenv("COINGECKO_API_KEY")}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def get_cursor(connection: psycopg2.extensions.connection) -> psycopg2.extensions.cursor:
    """Sets up cursor"""
    return connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def insert_cryptocurrencies(conn, crypto_data):
    """Insert cryptocurrency information into the PostgreSQL database."""
    curs = get_cursor(conn)

    query = """INSERT INTO cryptocurrencies (
                id, symbol, name, current_price, market_cap, market_cap_rank,
                fully_diluted_valuation, total_volume, high_24h, low_24h, price_change_24h,
                price_change_percentage_24h, market_cap_change_24h, market_cap_change_percentage_24h,
                circulating_supply, total_supply, max_supply, ath, ath_change_percentage,
                ath_date, atl, atl_change_percentage, atl_date, roi, last_updated
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,%s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (id) DO UPDATE
            SET
                symbol = EXCLUDED.symbol,
                name = EXCLUDED.name,
                current_price = EXCLUDED.current_price,
                market_cap = EXCLUDED.market_cap,
                market_cap_rank = EXCLUDED.market_cap_rank,
                fully_diluted_valuation = EXCLUDED.fully_diluted_valuation,
                total_volume = EXCLUDED.total_volume,
                high_24h = EXCLUDED.high_24h,
                low_24h = EXCLUDED.low_24h,
                price_change_24h = EXCLUDED.price_change_24h,
                price_change_percentage_24h = EXCLUDED.price_change_percentage_24h,
                market_cap_change_24h = EXCLUDED.market_cap_change_24h,
                market_cap_change_percentage_24h = EXCLUDED.market_cap_change_percentage_24h,
                circulating_supply = EXCLUDED.circulating_supply,
                total_supply = EXCLUDED.total_supply,
                max_supply = EXCLUDED.max_supply,
                ath = EXCLUDED.ath,
                ath_change_percentage = EXCLUDED.ath_change_percentage,
                ath_date = EXCLUDED.ath_date,
                atl = EXCLUDED.atl,
                atl_change_percentage = EXCLUDED.atl_change_percentage,
                atl_date = EXCLUDED.atl_date,
                roi = EXCLUDED.roi,
                last_updated = EXCLUDED.last_updated"""

    id = crypto_data.get('id')
    symbol = crypto_data.get('symbol')
    name = crypto_data.get('name')
    current_price = crypto_data.get('current_price')
    market_cap = crypto_data.get('market_cap')
    market_cap_rank = crypto_data.get('market_cap_rank')
    fully_diluted_valuation = crypto_data.get('fully_diluted_valuation')
    total_volume = crypto_data.get('total_volume')
    high_24h = crypto_data.get('high_24h')
    low_24h = crypto_data.get('low_24h')
    price_change_24h = crypto_data.get('price_change_24h')
    price_change_percentage_24h = crypto_data.get(
        'price_change_percentage_24h')
    market_cap_change_24h = crypto_data.get('market_cap_change_24h')
    market_cap_change_percentage_24h = crypto_data.get(
        'market_cap_change_percentage_24h')
    circulating_supply = crypto_data.get('circulating_supply')
    total_supply = crypto_data.get('total_supply')
    max_supply = crypto_data.get('max_supply')
    ath = crypto_data.get('ath')
    ath_change_percentage = crypto_data.get('ath_change_percentage')
    ath_date = crypto_data.get('ath_date')
    atl = crypto_data.get('atl')
    atl_change_percentage = crypto_data.get('atl_change_percentage')
    atl_date = crypto_data.get('atl_date')
    roi = json.dumps(crypto_data.get(
        'roi')) if crypto_data.get('roi') else None
    last_updated = crypto_data.get('last_updated')

    curs.execute(query, (
        id, symbol, name, current_price, market_cap, market_cap_rank,
        fully_diluted_valuation, total_volume, high_24h, low_24h, price_change_24h,
        price_change_percentage_24h, market_cap_change_24h, market_cap_change_percentage_24h,
        circulating_supply, total_supply, max_supply, ath, ath_change_percentage,
        ath_date, atl, atl_change_percentage, atl_date, roi, last_updated,
    ))
    conn.commit()


def main():
    ids = fetch_crypto_ids()
    random_ids = select_random_crypto_ids(ids, 50)
    print(f"Selected ID's: {random_ids}")

    if random_ids:
        try:
            conn = psycopg2.connect(
                dbname='crypto',
                user='joel',
                host='localhost',
                port='5432'
            )

            with conn:
                with conn.cursor() as cursor:
                    start_time = time.time()
                    request_count = 0

                    for id in random_ids:
                        current_time = time.time()

                        if request_count >= 30:
                            elapsed_time = current_time - start_time
                            if elapsed_time < 60:
                                sleep_time = 60 - elapsed_time
                                print(f"""Rate limit reached. Sleeping for {
                                      sleep_time:.2f} seconds...""")
                                time.sleep(sleep_time)

                            start_time = time.time()
                            request_count = 0

                        crypto_data = get_crypto_info(id)

                        if crypto_data:
                            print(f"Inserting data for {id}")
                            success = insert_cryptocurrencies(
                                conn, crypto_data)

                            if not success:
                                print(f"Failed to insert data for {id}")
                        else:
                            print(f"No data returned for {id}")

                        request_count += 1
                        time.sleep(2)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    return "Data for all random IDs added successfully"


if __name__ == "__main__":
    main()
