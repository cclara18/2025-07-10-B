from database.DB_connect import DBConnect
from model.prodotti import Prodotti


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("""
        select distinct c.* 
from categories as c 
order by c.category_name asc
                 """)

        cursor.execute(query)

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(categoriaid):

            conn = DBConnect.get_connection()

            results = []

            cursor = conn.cursor(dictionary=True)
            query = ("""
           select distinct p.*,  sum(oi.quantity) as q
from categories as c, products as p , order_items as oi   
where c.category_id = p.category_id and c.category_id = %s and oi.product_id = p.product_id 
group by p.product_id 
                     """)

            cursor.execute(query,(categoriaid, ))

            for row in cursor:
                results.append(Prodotti(**row))

            cursor.close()
            conn.close()
            return results

    @staticmethod
    def getAllEdges(categoriaid, datai, dataf, categoriaid1,datai1, datai2):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("""
               select distinct p1.product_id as p1, p2.product_id as p2
from (select distinct p.product_id 
	from categories as c, products as p , order_items as oi  , orders as o 
	where c.category_id = p.category_id and c.category_id = %s and oi.product_id = p.product_id and oi.order_id=o.order_id and o.order_date between %s and %s) 
	as p1
join (select distinct p.product_id
	from categories as c, products as p , order_items as oi  , orders as o 
	where c.category_id = p.category_id and c.category_id = %s and oi.product_id = p.product_id and oi.order_id=o.order_id and o.order_date between %s and %s)
	as p2 on p1.product_id > p2.product_id
                         """)

        cursor.execute(query, (categoriaid, datai, dataf, categoriaid1, datai1, datai2))

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results
