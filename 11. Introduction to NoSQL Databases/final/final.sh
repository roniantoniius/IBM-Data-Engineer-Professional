# Task 1 - Import 'movies.json' into mongodb server
# into a database named 'entertainment' and a collection named 'movies'
mongoimport -u root -p NDU0OC1qZW9uZ2tp --authenticationDatabase admin --db entertainment --collection movies --file movies.json

# Task 4 - Write a query to find out the average
# votes for movies released in 2007
db.movies.aggregate([
    {
        "$match":{
            "year":2007
            }
            },
    {
        "$group":{
            "_id":"$year",
            "average":{
                "$avg":"$Votes"}
    }
    }
])

# Task 6 - Export the fields '_id', 'title', 'year',
# 'rating', and 'director' from the 'movies' collection
# into a file named 'partial_data.csv'
mongoexport -u root -p NDU0OC1qZW9uZ2tp --authenticationDatabase admin --db entertainment --collection movies --out partial_data.csv --type=csv --fields id,title,year,rating,director

# Task 7 - Import 'partial_data.csv' into cassandra server
# into a keyspace named 'entertainment' and a table named 'movies'
CREATE KEYSPACE entertainment  
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};
use entertainment;
CREATE TABLE movies(
id text PRIMARY KEY,
title text,
year text,
rating text,
director text
);
COPY entertainment.movies(id,title,year,rating,director) FROM 'partial_data.csv' WITH DELIMITER=',' AND HEADER=TRUE;

# Task 8 - Write a cql query to count the number of rows
# in the 'movies' table
SELECT count(*) FROM movies;

# Task 9 - Create an index for the 'rating' column
# in the 'movies' table using cql
CREATE index rating_index ON movies(rating);

# Task 10 - Write a cql query to count the number of
# movies that are rated 'G'
SELECT count(*) FROM movies WHERE rating='G';
