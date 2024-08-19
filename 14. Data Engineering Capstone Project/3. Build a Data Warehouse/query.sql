-- Grouping sets

SELECT country, category, SUM(amount) as totalsales
FROM public."FactSales" AS F
LEFT JOIN public."DimCountry" AS T
ON F.country_id = T.country_id
LEFT JOIN public."DimCategory" as C
ON F.category_id = C.category_id
GROUP BY GROUPING SETS(country, category);


-- Rollup

SELECT year, country, SUM(amount) as totalsales
FROM public."FactSales" AS F
LEFT JOIN public."Dimdate" AS D
ON F.date_id = D.date_id
LEFT JOIN public."DimCountry" AS  T
ON F.country_id = T.country_id
GROUP BY ROLLUP(year, country);


-- Cube

SELECT year, country, AVG(amount) as averagesales
FROM public."FactSales" AS F
LEFT JOIN public."Dimdate" AS D
ON F.date_id = D.date_id
LEFT JOIN public."DimCountry" AS T
ON F.country_id = T.country_id
GROUP BY CUBE(year, country);


-- MQT, Materialized Views

CREATE MATERIALIZED VIEW total_sales_per_country (country, total_sales) AS
(SELECT country, SUM(amount)
	FROM public."FactSales" as F
	LEFT JOIN public."DimCountry" AS T
	ON F.country_id = T.country_id
	GROUP BY country
);
REFRESH MATERIALIZED VIEW total_sales_per_country;

SELECT * FROM total_sales_per_country:
