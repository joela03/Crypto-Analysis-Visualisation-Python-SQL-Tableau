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

