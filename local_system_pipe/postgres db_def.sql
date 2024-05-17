--CREATE schema cryptoschema;
CREATE TABLE btcusdt(
Open_time timestamp,
Open float,
High float,
Low float,
Close float,
Volume float,
Quote_asset_volume float,
Num_trades bigint,
Taker_base_vol float,
Taker_quote_vol float,
Price_diff float,
Price_change float
);
