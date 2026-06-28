import csv
import sqlite3

con = sqlite3.connect("data/scifi_books.db") 
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS books ('Book_Title', 'Original_Book_Title', 'Author_Name', 'Edition_Language', 'Rating_score', 'Rating_votes', 'Review_number', 'Book_Description', 'Year_published', 'Genres', 'url', 'Subgenre');") 

columns = ['Book_Title', 'Original_Book_Title', 'Author_Name', 'Edition_Language', 'Rating_score', 'Rating_votes', 'Review_number', 'Book_Description', 'Year_published', 'Genres', 'url', 'Subgenre']

with open('data/scifi_books.csv','r') as fin:
    dr = csv.DictReader(fin) 
    to_db = [(i['Book_Title'], i['Original_Book_Title'], i['Author_Name'], i['Edition_Language'], i['Rating_score'], i['Rating_votes'], i['Review_number'], i['Book_Description'], i['Year_published'], i['Genres'], i['url'], i['Subgenre']) for i in dr]

cur.executemany("INSERT INTO books (Book_Title, Original_Book_Title, Author_Name, Edition_Language, Rating_score, Rating_votes, Review_number, Book_Description, Year_published, Genres, url, Subgenre) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()