-- Checks for null value count

SELECT 
    COUNT(*) AS total_records,
    COUNT(id) AS count_id,
    COUNT(symbol) AS count_symbol,
    COUNT(name) AS count_name,
    COUNT(current_price) AS count_current_price,
    COUNT(market_cap) AS count_market_cap,
    COUNT(market_cap_rank) AS count_market_cap_rank,
    COUNT(fully_diluted_valuation) AS count_fully_diluted_valuation,
    COUNT(total_volume) AS count_total_volume,
    COUNT(high_24h) AS count_high_24h,
    COUNT(low_24h) AS count_low_24h,
    COUNT(price_change_24h) AS count_price_change_24h,
    COUNT(price_change_percentage_24h) AS count_price_change_percentage_24h,
    COUNT(market_cap_change_24h) AS count_market_cap_change_24h,
    COUNT(market_cap_change_percentage_24h) AS count_market_cap_change_percentage_24h,
    COUNT(circulating_supply) AS count_circulating_supply,
    COUNT(total_supply) AS count_total_supply,
    COUNT(max_supply) AS count_max_supply,
    COUNT(ath) AS count_ath,
    COUNT(ath_change_percentage) AS count_ath_change_percentage,
    COUNT(ath_date) AS count_ath_date,
    COUNT(atl) AS count_atl,
    COUNT(atl_change_percentage) AS count_atl_change_percentage,
    COUNT(atl_date) AS count_atl_date,
    COUNT(roi) AS count_roi,
    COUNT(last_updated) AS count_last_updated
FROM cryptocurrencies;

-- Checks summary statistics
SELECT 
    MIN(current_price) AS min_current_price,
    MAX(current_price) AS max_current_price,
    AVG(current_price) AS avg_current_price,
    STDDEV(current_price) AS stddev_current_price,
    
    MIN(market_cap) AS min_market_cap,
    MAX(market_cap) AS max_market_cap,
    AVG(market_cap) AS avg_market_cap,
    STDDEV(market_cap) AS stddev_market_cap,
    
    MIN(market_cap_rank) AS min_market_cap_rank,
    MAX(market_cap_rank) AS max_market_cap_rank,
    AVG(market_cap_rank) AS avg_market_cap_rank,
    STDDEV(market_cap_rank) AS stddev_market_cap_rank,

    MIN(ath) AS min_ath,
    MAX(ath) AS max_ath,
    AVG(ath) AS avg_ath,
    STDDEV(ath) AS stddev_ath,

    MIN(atl) AS min_atl,
    MAX(atl) AS max_atl,
    AVG(atl) AS avg_atl,
    STDDEV(atl) AS stddev_atl

FROM cryptocurrencies;

-- SELECT'S top 10 cryptocurrencies by market cap
SELECT 
    name, 
    symbol, 
    market_cap
FROM 
    cryptocurrencies
ORDER BY 
    market_cap DESC
LIMIT 10;

-- Find's price change over time
SELECT 
    name, 
    symbol, 
    last_updated, 
    current_price, 
    price_change_24h, 
    price_change_percentage_24h
FROM 
    cryptocurrencies
ORDER BY 
    last_updated DESC;

-- Find's the market cap distribution
SELECT 
    CASE
        WHEN market_cap < 10000000 THEN '< 10M'
        WHEN market_cap BETWEEN 10000000 AND 100000000 THEN '10M-100M'
        WHEN market_cap BETWEEN 100000000 AND 1000000000 THEN '100M-1B'
        ELSE '> 1B'
    END AS market_cap_range,
    COUNT(*) AS count
FROM 
    cryptocurrencies
GROUP BY 
    market_cap_range
ORDER BY 
    market_cap_range;

-- Ordering cryptocurrencies by market cap rank
SELECT 
    name, 
    symbol, 
    market_cap_rank
FROM 
    cryptocurrencies
ORDER BY 
    market_cap_rank;

-- Identify most volatile crypto currencies
SELECT 
    name, 
    symbol, 
    price_change_percentage_24h
FROM 
    cryptocurrencies
ORDER BY 
    ABS(price_change_percentage_24h) DESC
LIMIT 10;

-- Finding insights from ROI data
SELECT 
    name, 
    symbol, 
    roi->>'times' AS times_roi, 
    roi->>'currency' AS currency_roi
FROM 
    cryptocurrencies
WHERE 
    roi IS NOT NULL
ORDER BY 
    times_roi DESC;

-- ATH and ATL analysis
SELECT 
    name, 
    symbol, 
    ath, 
    ath_change_percentage, 
    atl, 
    atl_change_percentage
FROM 
    cryptocurrencies
ORDER BY 
    ath DESC;