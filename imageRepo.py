from flask import Flask, render_template
import sqlite3 as sql

app = Flask(__name__)

# gather cursor and connection from sqlite3 to query against the database
def get_cursor():
    conn = sql.connect("image.db")
    cur = conn.cursor()
    return (cur, conn)

# Used to convert images to display on website
def convertToBinaryData(filename):

  with open(filename, 'rb') as file:
      blobData = file.read()
  return blobData


# intialize the database Images
def initialize_db():
    (cur, conn) = get_cursor()

    # Create the Products table
    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("CREATE TABLE products ( \
    image TEXT, product_id int AUTO_INCREMENT, \
    product_name VARCHAR(255), price int, quantity int,\
    seller_ID int AUTO_INCREMENT, \
    PRIMARY KEY (product_id));");

    # Insert products into the Product table
    cur.execute("INSERT INTO products (image, product_id, product_name, price, quantity, seller_ID) VALUES ('/book.jpg', 1, 'Book Art', 5, 5, 1);")
    cur.execute("INSERT INTO products (image, product_id, product_name, price, quantity, seller_ID) VALUES ('/tree.jfif', 2, 'Tree Art', 12, 10, 1);")
    cur.execute("INSERT INTO products (image, product_id, product_name, price, quantity, seller_ID) VALUES ('/eiffel.jpg', 3, 'Eiffel Tower Art', 200, 10, 2);")
    cur.execute("INSERT INTO products (image, product_id, product_name, price, quantity, seller_ID) VALUES ('/mountain.jpg', 4, 'Moraine Lake Art', 100, 30, 3);")
    cur.execute("INSERT INTO products (image, product_id, product_name, price, quantity, seller_ID) VALUES ('/cow.jfif', 5, 'Cow Art', 20, 25, 3);")
    
    # Create the seller orders tables
    cur.execute("DROP TABLE IF EXISTS seller_orders")
    cur.execute("CREATE TABLE seller_orders ( \
    seller_ID int AUTO_INCREMENT,\
    total_orders int, total_amount int,\
    PRIMARY KEY (seller_ID), \
    FOREIGN KEY (seller_ID) REFERENCES sellers(seller_ID) \
    );");
        
    cur.execute("DROP TABLE IF EXISTS sellers")
    cur.execute("CREATE TABLE sellers (seller_ID int AUTO_INCREMENT, \
                 first_name varchar(255), last_name varchar(255),\
                 product_id int, total_profits int , seller_length_years int,\
                 PRIMARY KEY (seller_ID),FOREIGN KEY (product_id) REFERENCES product(product_id));");
    
    # Commit the database changes
    conn.commit()
    print("Initialized database")

@app.route("/")
def home_page():
    
    # display the table using a prepopulated array gathered from the following query
    (cur, _) = get_cursor()
    cur.execute("SELECT * FROM products")
    
    rows = cur.fetchall()
    
    # Used to show the total number of products left - once a product is delete this will be auto-updated on the website!
    total_prod_num = len(rows)
    
    #used to prepopulate the table to help querying in HTML
    products = []
    for values in rows:
        products.append({
            "src":   "/static/%s" % (values[0]),
            "id":    values[1],
            "name":  values[2],
            "price": "$ %d" % (values[3]),
            "stock": "%d available" % (values[4]),
        })
    
   
    # Used to gather the total amount that the buyer has bought from the Image E-Shop
    cur.execute("SELECT SUM(total_amount) FROM seller_orders ")
    sqlResult = cur.fetchone()[0]
    spending = sqlResult if sqlResult else 0

    return render_template("index.html", products=products, spending=spending, total_prod_num=total_prod_num)

@app.route("/showSeller")
def showSeller():
    # display the table using a prepopulated array gathered from the following query

    (cur, _) = get_cursor()
    cur.execute("SELECT * FROM seller_orders")
    rows = cur.fetchall()
    
    
    #used to prepopulate the table to help querying in HTML
    orders = []
    for values in rows:
        orders.append({
            "seller_id":    values[0],
            "tl_orders":  "%d orders" % (values[1]),
            "tl_amount": "$ %d sold" % (values[2]),
        })
        
    #display the sellers in the seller page
    return render_template("sellers.html",orders=orders)

@app.route("/buy/<product_id>")
def buy(product_id):
    
    #check if the correct id exists
    if not product_id:
        return render_template("message.html", message="This is not a correct productID, please try agian!")

    (cur, conn) = get_cursor()

    #query to get the price and seller id to update the seller order history table
    cur.execute("SELECT price, seller_ID FROM products WHERE product_id = ?", (product_id,))
    result = cur.fetchone()
  
    if not result:
           return render_template("message.html", message="Invalid product ID!")
    (price, seller_ID) = result

   
   # add seller ID if doesnt exist to the seller_orders
   # if exists then update the seller with the new total sold and profits
    cur.execute( "INSERT INTO seller_orders (seller_ID, total_orders, total_amount) VALUES(?, 1, ?) ON CONFLICT(seller_ID) DO UPDATE SET total_orders=total_orders+1,total_amount = total_amount + ?"
                , (seller_ID, price, price))

   # update the total quantity left
    cur.execute("UPDATE products SET quantity = quantity - 1 WHERE product_id = ?", (product_id,))
    cur.execute("SELECT quantity FROM products WHERE product_id = ?", (product_id,))
    quantity_result = cur.fetchone()
    (new_quantity,) = quantity_result
   
   #if the total quantity is 0 now then delete the product from the table to restrict people from buying it anymore
    if new_quantity <= 0:
       cur.execute("DELETE FROM products WHERE product_id = ?", (product_id))
    
    conn.commit()
    return render_template("message.html", message="Purchase successful!")
 


@app.route("/reset")
def reset():
   # reset the table
    initialize_db()
    return render_template("message.html", message="Database reset! Click Main page link to return to the Homepage!")

if __name__ == '__main__':
    initialize_db()
    app.run(debug = True)