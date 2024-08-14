CREATE MATERIALIZED VIEW max_waste_stats AS
SELECT DS.City, 
FT.Stationid, 
DT.TruckType,
MAX(FT.Wastecollected) AS MaxWasteCollected
FROM FactTrips FT
JOIN DimStation DS
ON FT.Stationid = DS.Stationid
JOIN DimTruck DT
ON FT.Truckid = DT.Truckid
GROUP BY DS.City, FT.Stationid, DT.TruckType;

SELECT * FROM max_waste_stats;
