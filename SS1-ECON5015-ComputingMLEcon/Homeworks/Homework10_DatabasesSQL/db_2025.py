import sqlite3
import pandas as pd

con = sqlite3.connect("chinook.db") 
con.text_factory = lambda b: b.decode(errors = 'ignore')  #a "hack" because some album names in this database have characters that cause an error to be thrown 

pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';",con)
df = pd.read_sql_query("select * from Track",con)
df = pd.read_sql_query("select Name from Track",con)
df = pd.read_sql_query("select Name,Milliseconds from Track",con)

df = pd.read_sql_query("select * from Track order by Milliseconds",con)
df = pd.read_sql_query("select * from Track order by Milliseconds desc",con)
df = pd.read_sql_query("select * from Track order by Milliseconds desc limit 20",con)


df = pd.read_sql_query("select * from Track where Name='Resolve'",con)
name="Resolve"
df = pd.read_sql_query("select * from Track where Name=? or Name=?",con,params=[name,"Balls to the Wall"])
df = pd.read_sql_query("select * from Track where Name=?",con,params=[name])
df = pd.read_sql_query("select * from Track where Name='"+name+"'",con)

df = pd.read_sql_query("select Name, Milliseconds from Track where Milliseconds < 60*1000 order by Milliseconds",con)

df = pd.read_sql_query("select Name, Milliseconds, UnitPrice from Track where Milliseconds > 120*1000 and UnitPrice>0.99",con)
df = pd.read_sql_query("select Name, Milliseconds, UnitPrice from Track where Milliseconds > 120*1000 or UnitPrice>0.99",con)


df = pd.read_sql_query("select max(Milliseconds) from Track;",con)
df = pd.read_sql_query("select avg(Milliseconds) from Track;",con)
df = pd.read_sql_query("select avg(Milliseconds),max(Milliseconds) from Track;",con)
df = pd.read_sql_query("select avg(Milliseconds)/60000 from Track;",con)
df = pd.read_sql_query("select sum(Bytes) from Track;",con)
df = pd.read_sql_query("select count(Name) from Track where Milliseconds<120000;",con)


df = pd.read_sql_query("select * from Invoice;",con)
df = pd.read_sql_query("select CustomerId, sum(Total) from Invoice group by CustomerId;",con)
df = pd.read_sql_query("select * from Customer where country='USA';",con)
df = pd.read_sql_query("select State, count(CustomerId) from Customer where Country='USA' group by State;",con)

df = pd.read_sql_query("select CustomerId, sum(Total) as InvoiceTotal from Invoice group by CustomerId having InvoiceTotal > 40;",con)

df = pd.read_sql_query("select * from Album;",con)
df = pd.read_sql_query("select AlbumID from Track;",con)
df = pd.read_sql_query("select distinct AlbumID from Track;",con)

df = pd.read_sql_query("select Name, Title from Album join Artist using (ArtistId);",con)
df = pd.read_sql_query("select Name, Title from Album join Artist on Album.ArtistId=Artist.ArtistId;",con)
df = pd.read_sql_query("select Name, Title from Album natural join Artist;",con)

df = pd.read_sql_query("select Artist.Name, Title, Track.Name from Album join Artist using (ArtistId) join Track using (AlbumId);",con)
df = pd.read_sql_query("select Artist.Name as ArtistName, Title as AlbumTitle, Track.Name as TrackName from Album join Artist using (ArtistId) join Track using (AlbumId);",con)
df = pd.read_sql_query("select Artist.Name, Title, Track.Name from Track join (Album join Artist using (ArtistId)) using (AlbumId);",con)

df = pd.read_sql_query("select Name from Track join Album using (AlbumId) where Title='Supernatural';",con)
df = pd.read_sql_query("select Artist.Name as ArtistName, Title as AlbumTitle, Track.Name as TrackName from Album join Artist using (ArtistId) join Track using (AlbumId) order by ArtistName, AlbumTitle;",con)
df = pd.read_sql_query("select Artist.Name as ArtistName, Title as AlbumTitle, sum(Milliseconds)/1000 as Length from Album join Artist using (ArtistId) join Track using (AlbumId) group by AlbumId order by ArtistName, AlbumTitle;",con)
df = pd.read_sql_query("select Artist.Name as ArtistName, Title as AlbumTitle, sum(Milliseconds)/1000 as Length from Album join Artist using (ArtistId) join Track using (AlbumId) group by AlbumId having Length>1000 order by Length desc;",con)
df = pd.read_sql_query("select A.Name as ArtistName, Title as AlbumTitle, T.Name as TrackName from Album join Artist as A using (ArtistId) join Track as T using (AlbumId) order by ArtistName, AlbumTitle;",con)

df = pd.read_sql_query("select distinct Title from Album join Track as T1 using (AlbumId) join Track as T2 using (AlbumId) where T1.Milliseconds<60000 and T2.Milliseconds>360000;",con)
df = pd.read_sql_query("select distinct AlbumId from Track as T1 join Track as T2 using (AlbumId) where T1.Milliseconds<60000 and T2.Milliseconds>360000;",con)
df = pd.read_sql_query("select distinct AlbumId from Track where Milliseconds<60000 or Milliseconds>360000;",con)

df = pd.read_sql_query("select customerid, count(TrackId) from Invoice join InvoiceLine using (InvoiceId) group by CustomerId;",con)
df = pd.read_sql_query("select customerid, min(numtracks) from (select customerid, count(TrackId) as numtracks from Invoice join InvoiceLine using (InvoiceId) group by CustomerId);",con)

crsr=con.cursor()

crsr.execute("create table temp (id integer, name text, primary key (id))")
pd.read_sql_query("select * from temp;",con)
crsr.execute("insert into temp values (1,'ABC')")
crsr.execute("insert into temp values (2,'DEF')")
crsr.execute("insert into temp values (3,'GHI')")
pd.read_sql_query("select * from temp;",con)

df=pd.read_sql_query("select * from temp;",con)
df["country"]=["USA","Canada","USA"]
df.to_sql("temp",con,if_exists="replace")
pd.read_sql_query("select * from temp;",con)

crsr.execute("update temp set country='United States of America' where country='USA'")
pd.read_sql_query("select * from temp;",con)

crsr.execute("drop table temp")
con.commit()
con.close()

