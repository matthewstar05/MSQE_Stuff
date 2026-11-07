"""
ECON 5015: SQL Assignment (Northwind)
Matthew Suban
@matthewsuban
"""
import sqlite3
import pandas as pd

# northwind.db is assumed to be in the working directory
con = sqlite3.connect("northwind.db")

# Real names differ from the schema handout: tables are Orders, Customer, OrderDetail,
# and each table's key is Id (Orders.Id is the OrderID, Customer.Id is the CustomerID).

# 1. every field from Orders, only orders shipped to the USA
d1 = pd.read_sql_query("select * from Orders where ShipCountry = 'USA';", con)

# 2. each country with at least one customer, listed once
d2 = pd.read_sql_query("select distinct Country from Customer;", con)

# 3. countries with more than one customer and how many, most customers first
d3 = pd.read_sql_query("""select Country, count(*) as NumCustomers from Customer
                          group by Country having count(*) > 1
                          order by NumCustomers desc;""", con)

# 4. orders shipped to a different country than the customer's own country
d4 = pd.read_sql_query("""select o.Id as OrderID from Orders o
                          join Customer c on o.CustomerId = c.Id
                          where o.ShipCountry <> c.Country;""", con)

# 5. total revenue of each order: sum over its products of (1-discount)*UnitPrice*Quantity
d5 = pd.read_sql_query("""select OrderId as OrderID, sum((1 - Discount) * UnitPrice * Quantity) as TotalRevenue
                          from OrderDetail group by OrderId;""", con)

# 6. order id, order date, and total revenue for orders placed by customers based in the USA
d6 = pd.read_sql_query("""select o.Id as OrderID, o.OrderDate, sum((1 - d.Discount) * d.UnitPrice * d.Quantity) as TotalRevenue
                          from Orders o
                          join Customer c on o.CustomerId = c.Id
                          join OrderDetail d on d.OrderId = o.Id
                          where c.Country = 'USA'
                          group by o.Id, o.OrderDate;""", con)

# 7. companies that shipped at least one order to Eugene
d7 = pd.read_sql_query("""select distinct c.CompanyName from Customer c
                          join Orders o on o.CustomerId = c.Id
                          where o.ShipCity = 'Eugene';""", con)

# 8. companies that shipped at least two orders to Eugene
d8 = pd.read_sql_query("""select c.CompanyName from Customer c
                          join Orders o on o.CustomerId = c.Id
                          where o.ShipCity = 'Eugene'
                          group by c.Id, c.CompanyName having count(*) >= 2;""", con)

con.close()


def orderlookup(city: str, country: str) -> pd.DataFrame:
    """All Orders fields for orders shipped to the given city and country."""
    con = sqlite3.connect("northwind.db")
    result = pd.read_sql_query("select * from Orders where ShipCity = ? and ShipCountry = ?;",
                               con, params=(city, country))
    con.close()
    return result


output = True
if output:
    for name, d in [("d1", d1), ("d2", d2), ("d3", d3), ("d4", d4),
                    ("d5", d5), ("d6", d6), ("d7", d7), ("d8", d8)]:
        print(name, d.shape)
        print(d.head())
    print(orderlookup("Eugene", "USA"))
