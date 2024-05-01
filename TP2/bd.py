import psycopg2
import csv
import json

def chamarSQL(id):
    conn = psycopg2.connect("dbname=mydb user=afonsoni")
    cur = conn.cursor()
    cena = ""
    cur.execute(f'SELECT text FROM dreapp_documenttext WHERE document_id = {id};')
    sel = cur.fetchone()
    print("Selected: ", sel)
    if sel is not None:
        cena = sel
    return cena

id = "100111"
exemplo = ""
dic = {}
map = csv.reader(open('id_mapping__.csv', 'r'))
for row in map:
    dic[row[0]] = row[1]

print(dic[id])
