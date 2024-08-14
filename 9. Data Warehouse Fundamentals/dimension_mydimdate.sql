CREATE TABLE MyDimDate (
   date_id INT NOT NULL PRIMARY KEY,
   date_ DATE NOT NULL,
   year INT NOT NULL,
   quarter VARCHAR(2) NOT NULL,
   month INT NOT NULL,
   monthname VARCHAR(20) NOT NULL,
   day INT NOT NULL,
   weekday_ VARCHAR(20) NOT NULL
);