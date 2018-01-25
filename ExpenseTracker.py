import json

from flask import Flask, jsonify, request, Response, render_template
import pgdb

app = Flask(__name__)

# dbconnection = pgdb.connect(host="localhost", user="postgres", password="qwerty123", database="expensetracker")

#
# def create_table(conn):
#     # sql = """CREATE TABLE users (user_id SERIAL PRIMARY KEY,username VARCHAR(255) NOT NULL,password VARCHAR(255) NOT NULL,email_id VARCHAR(255) NOT NULL);"""
#
#     # sql = """CREATE TABLE category (category_id SERIAL PRIMARY KEY,category_name VARCHAR(255) NOT NULL);"""
#     sql = """CREATE TABLE user_expenses (expense_id SERIAL PRIMARY KEY,category_id VARCHAR(255) NOT NULL,user_id VARCHAR(255) NOT NULL,amount VARCHAR(255) NOT NULL);"""
#     cur = conn.cursor()
#     cur.execute(sql)
#     conn.commit()
#     dbconnection.close()
#
# create_table(dbconnection)




@app.route('/')
def IndexPage():
    return render_template("login.html")


@app.route('/register')
def RegisterPage():
    return render_template("register.html")

@app.route('/add_category')
def AddCategory():
    return render_template("add_category.html")

@app.route('/user_expenses')
def UserExpenses():
    return render_template("user_expense_list.html")


@app.route('/category_list/', methods=['GET'])
def Category_list():
    json_category_list = []
    dbconnection = pgdb.connect(host="localhost", user="postgres", password="qwerty123", database="expensetracker")
    sql = """SELECT * from category;"""
    cur = dbconnection.cursor()
    cur.execute(sql)
    category_list = cur.fetchall()
    print(category_list)
    for i in category_list:
        json_category_list.append({
            "category_id":i[0],
            "category_name":i[1]
        })
    return Response(json.dumps(json_category_list),  mimetype='application/json')





@app.route('/user_register/', methods=['POST'])
def UserRegister():
    username = request.form['username']
    email_id = request.form['email_id']
    password = request.form['password']
    dbconnection = pgdb.connect(host="localhost", user="postgres", password="qwerty123", database="expensetracker")
    sql = """SELECT email_id from users WHERE email_id = %s;"""
    cur = dbconnection.cursor()
    data = (email_id,)
    datasome = cur.execute(sql, data)
    if cur.fetchone():
        print("user exists")
        user_register_data = {
            "user": "exists",
        }
        dbconnection.close()
        return jsonify(user_register_data)
    else:
        print("not exists")
        sql = """INSERT INTO users (username, password, email_id)
                     VALUES(%s,%s,%s);"""
        cur = dbconnection.cursor()
        data = (username, password, email_id)
        cur.execute(sql, data)
        dbconnection.commit()
        user_register_data = {
            "username": username,
            "email_id": email_id
        }
        dbconnection.close()
        return jsonify(user_register_data)



@app.route('/user_login/', methods=['POST'])
def UserLogin():
    email_id = request.form['email_id']
    password = request.form['password']
    dbconnection = pgdb.connect(host="localhost", user="postgres", password="qwerty123", database="expensetracker")
    sql = """SELECT * from users WHERE email_id = %s AND password=%s;"""
    cur = dbconnection.cursor()
    data = (email_id, password)
    cur.execute(sql, data)
    result = cur.fetchone()
    print(result)
    if result:
        print("user exists")
        user_register_data = {
            "welcome": email_id,
        }
        dbconnection.close()
        return render_template("user_dashboard.html", user_id=result[0], username=result[1])

        # return jsonify(user_register_data)
    else:
        print("not exists")
        user_register_data = {
            "username or password": "is incorrect",
        }
        dbconnection.close()
        # return render_template("login.html")
        return jsonify(user_register_data)


@app.route('/create_category/', methods=['POST'])
def CreateCategory():
    category_name = request.form['category_name']
    dbconnection = pgdb.connect(host="localhost", user="postgres", password="qwerty123", database="expensetracker")
    sql = """INSERT INTO category (category_name)
                 VALUES(%s);"""
    cur = dbconnection.cursor()
    data = (category_name,)
    cur.execute(sql, data)
    dbconnection.commit()
    category_data = {
        "category_id": category_name
    }
    dbconnection.close()
    # return jsonify(category_data)
    return render_template('add_category.html')



@app.route('/create_expense/', methods=['POST'])
def CreateExpense():
    user_id = request.form['user_id']
    category_id = request.form['category_id']
    amount = request.form['amount']
    dbconnection = pgdb.connect(host="localhost", user="postgres", password="qwerty123", database="expensetracker")
    sql = """INSERT INTO user_expenses (category_id, user_id, amount)
                 VALUES(%s, %s, %s);"""
    cur = dbconnection.cursor()
    data = (category_id, user_id, amount)
    cur.execute(sql, data)
    dbconnection.commit()
    expense_data = {
        "category_id": category_id,
        "user_id": user_id,
        "amount": amount
    }
    dbconnection.close()
    return render_template('user_dashboard.html')


@app.route('/get_user_expenses/', methods=['POST'])
def GetUserExpenses():
    user_id = request.form['user_id']
    user_expense_list = []
    dbconnection = pgdb.connect(host="localhost", user="postgres", password="qwerty123", database="expensetracker")
    sql = """SELECT category_id, amount FROM user_expenses WHERE user_id = %s"""
    cur = dbconnection.cursor()
    data = (user_id)
    cur.execute(sql, data)
    results = cur.fetchall()
    for i in results:
        user_expense_list.append({
            "category_id":i[0],
            "amount":i[1]
        })
    dbconnection.commit()
    dbconnection.close()
    print(user_expense_list)
    return Response(json.dumps(user_expense_list),  mimetype='application/json')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
