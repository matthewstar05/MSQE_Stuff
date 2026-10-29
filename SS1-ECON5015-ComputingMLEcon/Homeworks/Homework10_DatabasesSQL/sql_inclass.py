"""
ECON 5015: Homework 10
Matthew Suban
@matthewsuban
"""
import sqlite3
import pandas as pd

con = sqlite3.connect("chinook.db")
con.text_factory = lambda b: b.decode(errors = 'ignore')  #a "hack" because some album names in this database have characters that cause an error to be thrown

# 1. tracks sold for more than $0.99 (sales are in InvoiceLine)
d1 = pd.read_sql_query("select TrackId, UnitPrice, Quantity from InvoiceLine where UnitPrice > 0.99;", con)

# 2. ArtistId for Pink Floyd
d2 = pd.read_sql_query("select ArtistId from Artist where Name = 'Pink Floyd';", con)

# 3. total length of every album in minutes (60000 ms per minute, .0 keeps it from rounding down)
d3 = pd.read_sql_query("select AlbumId, sum(Milliseconds)/60000.0 as Minutes from Track group by AlbumId;", con)

# 4. same as 3 but only albums 60 minutes or longer, longest first
d4 = pd.read_sql_query("select AlbumId, sum(Milliseconds)/60000.0 as Minutes from Track group by AlbumId having Minutes >= 60 order by Minutes desc;", con)

con.close()
