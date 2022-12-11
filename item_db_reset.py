import sqlite3
coninv = sqlite3.connect("./db/invt.db")
curinv = coninv.cursor()
items =[
(0, 'Shovel', 200, 1),
(1, 'Digging License', 500, 1)
]

curinv.execute("DROP TABLE IF EXISTS item")
curinv.execute("CREATE TABLE IF NOT EXISTS item(id INTEGER PRIMARY KEY, name STRING, price INTEGER, lim INTEGER)")
for j in range(len(items)):
    curinv.execute("INSERT INTO item VALUES (?,?,?,?)", items[j])
coninv.commit()
