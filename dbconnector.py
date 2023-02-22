import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "pw",
    database = "db"
)

mycursor = db.cursor()

## CREATE DATABASE
# mycursor.execute("CREATE DATABASE nikedb")

# # CREATE TABLE
# mycursor.execute("CREATE TABLE shoes ( id varchar(255), name varchar(255), last_updated datetime, gender varchar(255), price float, status varchar(255), pic varchar(255), pagelink varchar(255), release_day int, release_month int, release_time varchar(10), timezone varchar(10), localized_size float, nike_size float, gtin int, sku_id varchar(36), stock_level varchar(10) )")

# INSERT INTO
mycursor.execute("INSERT INTO test (name,created,gender) VALUES (%s,%s,%s)",("Tim",datetime.now(),'M'),('Jane',datetime.now(),'M'))
db.commit()

## SELECT
# mycursor.execute("SELECT name,gender FROM test WHERE gender = 'M'")
# for i in mycursor:
#     print(i)

## ADD COLUMN
# mycursor.execute("ALTER TABLE test ADD COLUMN food VARCHAR(255) NOT NULL")
# mycursor.execute("DESCRIBE test")
# for i in mycursor:
#     print(i)

## DROP COLUMN
# mycursor.execute("ALTER TABLE test DROP food")
# mycursor.execute("DESCRIBE test")
# for i in mycursor:
#     print(i)

# # CHANGE COLUMN NAME
# mycursor.execute("ALTER TABLE test CHANGE name first_name VARCHAR(50)")
# mycursor.execute("DESCRIBE test")
# for i in mycursor:
#     print(i)







