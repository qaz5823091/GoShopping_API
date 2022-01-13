from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route("/")
def hello():
    return "hello, world"

def db_connect():
    connect = None
    try:
        connect = sqlite3.connect('db.sqlite')

    except sqlite3.error as e:
        print(e)

    return connect

@app.route("/products", methods=["GET", "POST"])
def products():
    connect = db_connect()
    cursor = connect.cursor()


    if request.method == "GET":
        cursor = connect.execute("select * from products")
        products = [
            dict(id = row[0], name = row[1], price = row[2], amount = row[3])
            for row in cursor.fetchall()
        ]
        if products is not None:
            return jsonify(products)

    elif request.method == "POST":
        new_name = request.form["name"]
        new_price = request.form["price"]
        new_amount = request.form["amount"]
        sql_query = """ insert into products(name, price, amount)
            values (?, ?, ?)
        """
        cursor = cursor.execute(sql_query, (new_name, new_price, new_amount))
        connect.commit()
        return f"Product with the id: {cursor.lastrowid} created successfully", 201

@app.route("/product/<int:id>", methods = ["GET", "PUT", "DELETE"])
def single_product(id: int):
    id = int(id)
    connect = db_connect()
    cursor = connect.cursor()
    product = None

    if request.method == "GET":
        cursor.execute("select * from products where id=?", (id,))
        rows = cursor.fetchall()
        for item in rows:
            product = item

        if product is not None:
            return jsonify(product), 200
        else:
            return "Product not found", 404

    elif request.method == "POST":
        sql_query = """ update products
            set name = ?,
                price = ?,
                amount = ?
            where id = ?
        """

        name = request.form["name"]
        price = request.form["price"]
        amount = request.form["amount"]

        updated_product = {
            "id": id,
            "name": name,
            "price": price,
            "amount": amount
        }
        connect.execute(sql_query, (name, price, amount, id))
        connect.commit()
        return jsonify(updated_product)

    else:
        sql_query = """ delete from products where id = ? """
        connect.execute(sql_query, (id,))
        connect.commit()
        return f"The product with id: {id} has been deleted.", 200

if __name__ == "__main__":
    app.run()
