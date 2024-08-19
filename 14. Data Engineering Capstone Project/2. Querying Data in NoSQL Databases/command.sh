wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/nosql/catalog.json

mongoimport -u root -p MTc3ODEtYWFudG9u --authenticationDatabase admin --db catalog --colection electronics --file catalog.json

#go into mongodb CLI

show dbs

use catalog
show collections

db.electronics.createIndex({"type":1})

db.electronics.find({"type":"laptop"}).count()

db.electronics.find({"type":"smart phone", "screen size": {$eq: 6}}).count()

db.electronics.aggregate([
{
	$match: {"type": "smart phone"}
},
{
	"$group":{
		"_id":null,
		"average_screen_size":{"$avg":"$screen size"}
	}
}
])


mongoexport -u root -p MTc3ODEtYWFudG9u --authenticationDatabase admin --db catalog --collection electronics --out electronics.csv --type=csv --fields _id,type,model



