import requests
import psycopg2


def get_crypto_info(crypto_id: str) -> list[dict]:
    """Get's information for a crypto currency from the Coingecko API"""
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin{
        crypto_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails
        data = response.json()
        return data
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

    curs.execute(query, {
        'id': crypto_data['id'],
        'symbol': crypto_data['symbol'],
        'name': crypto_data['name'],
        'current_price': crypto_data['current_price'],
        'market_cap': crypto_data['market_cap'],
        'market_cap_rank': crypto_data['market_cap_rank'],
        'fully_diluted_valuation': crypto_data['fully_diluted_valuation'],
        'total_volume': crypto_data['total_volume'],
        'high_24h': crypto_data['high_24h'],
        'low_24h': crypto_data['low_24h'],
        'price_change_24h': crypto_data['price_change_24h'],
        'price_change_percentage_24h': crypto_data['price_change_percentage_24h'],
        'market_cap_change_24h': crypto_data['market_cap_change_24h'],
        'market_cap_change_percentage_24h': crypto_data['market_cap_change_percentage_24h'],
        'circulating_supply': crypto_data['circulating_supply'],
        'total_supply': crypto_data['total_supply'],
        'max_supply': crypto_data['max_supply'],
        'ath': crypto_data['ath'],
        'ath_change_percentage': crypto_data['ath_change_percentage'],
        'ath_date': crypto_data['ath_date'],
        'atl': crypto_data['atl'],
        'atl_change_percentage': crypto_data['atl_change_percentage'],
        'atl_date': crypto_data['atl_date'],
        'roi': json.dumps(crypto_data['roi']) if crypto_data['roi'] else None,
        'last_updated': crypto_data['last_updated']
    })

    columns_touched = curs.rowcount()
    conn.commit()

    return columns_touched > 0
