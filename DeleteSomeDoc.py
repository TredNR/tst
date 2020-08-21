import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["CovidModel"]

#-----------------Удаление первых документов в коллекции----------------
#---------------------В документах одно и тоже поле---------------------

myquery = {"Province/State": "#adm1+name"}

Confirmed_global_narrow = mydb["Confirmed_global_narrow"]
Confirmed_global_narrow.delete_one(myquery)

Deaths_global_narrow = mydb["Deaths_global_narrow"]
Deaths_global_narrow.delete_one(myquery)

Recovered_global_narrow = mydb["Recovered_global_narrow"]
Recovered_global_narrow.delete_one(myquery)

Confirmed_global_iso3_regions = mydb["Confirmed_global_iso3_regions"]
Confirmed_global_iso3_regions.delete_one(myquery)

Deaths_global_iso3_regions = mydb["Deaths_global_iso3_regions"]
Deaths_global_iso3_regions.delete_one(myquery)

Recovered_global_iso3_regions = mydb["Recovered_global_iso3_regions"]
Recovered_global_iso3_regions.delete_one(myquery)

#----------------Изменение типов полей документов--------------------
