-- SQL script to create a cryptocurrencies table

CREATE TABLE cryptocurrencies (
    id TEXT PRIMARY KEY,                    
    symbol TEXT,                            
    name TEXT,                              
    current_price NUMERIC,                  
    market_cap NUMERIC,                     
    market_cap_rank INTEGER,                
    fully_diluted_valuation NUMERIC,         
    total_volume NUMERIC,                    
    high_24h NUMERIC,                        
    low_24h NUMERIC,                         
    price_change_24h NUMERIC,                
    price_change_percentage_24h NUMERIC,    
    market_cap_change_24h NUMERIC,           
    market_cap_change_percentage_24h NUMERIC,
    circulating_supply NUMERIC,              
    total_supply NUMERIC,                    
    max_supply NUMERIC,                      
    ath NUMERIC,                             
    ath_change_percentage NUMERIC,           
    ath_date TIMESTAMPTZ,                    
    atl NUMERIC,                             
    atl_change_percentage NUMERIC,           
    atl_date TIMESTAMPTZ,                    
    roi JSONB,                               
    last_updated TIMESTAMPTZ                 
);