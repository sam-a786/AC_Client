import os
from flask import Flask, redirect, request, render_template, url_for, session, flash
import time
import sqlite3
from random import randint

app = Flask(__name__)
app.secret_key = "QrfS1qPGtoCLoalDz6lmLPiqr6j6tG"

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



#route to allow users to login
@app.route("/Login", methods = ["POST", "GET"])
def login():
    if "username" in session:
        return redirect("/Dashboard")

    else:
        if request.method == "POST":

            conn = sqlite3.connect('AeronaClinicalDatabase.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM Users")
            login_details = cur.fetchall()
            conn.close()

            print(login_details)
            username = request.form["username"]
            password = request.form["password"]
            login_tuple = (username, password)

            # admin = login_details.index(login_tuple)
            # print("here is admin var", admin)
            for i in login_details:
                print(i[1:3])
                if i[1:3] == login_tuple:
                    # I (mohammed h) made this global so i can reference it later.
                    global user_session_details
                    user_session_details = i[0:3]
                    admin = i[3]
                    if admin == "true":
                        session["username"] = username
                        session["userID"] = user_session_details[0]
                        print("This admin is true:", admin)
                        session["admin"] = "True"

                    elif admin == "false":
                        session["username"] = username
                        session["userID"] = user_session_details[0]
                        print("This admin is false:", admin)
                        session["admin"] = "False"

                    else:
                        return redirect("/Login")

                    print("Logged in")
                    return redirect("/Dashboard")
                else:
                    print("check in next login details")
                    continue

            flash("Invalid Username or Password","danger")
            return render_template("Login.html")
        else:
            return render_template("Login.html")

@app.route("/Dashboard")
def dashboard_panel():
    if "username" in session:                                   #Checking to see if there is a user logged into the session
        userID = session["userID"]                              #found from "https://pythonbasics.org/flask-sessions/"
        print(session)
        # print(username)
        for k,v in session.items():                             #Checking through the dictionary to find the admin key
            if k == "admin":
                if v == "True":                                 #If there is an admin key value check if the admin key is true or false
                    conn = sqlite3.connect('AeronaClinicalDatabase.db')
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM Orders")
                    value = cur.fetchall()
                    conn.close()
                    return render_template("dashboard.html", data = value,userInformation = session['username'].title())        #If admin value is true return all the forms
                elif v == "False":
                    conn = sqlite3.connect('AeronaClinicalDatabase.db')
                    cur = conn.cursor()
                    Orders = '''SELECT * FROM Orders where userID = %s ''' % userID
                    cur.execute(Orders)
                    value = cur.fetchall()
                    conn.close()
                    print(userID)
                    print(session)
                    return render_template("dashboard.html", data = value, userInformation = session['username'].title())       #If the admin value is false then only return the forms of that specific user
            else:
                return redirect("/Login")


    else:
        return redirect("/Login")

@app.route("/CreateForm")
def new_form():
    if "username" in session:
        connection = sqlite3.connect("AeronaClinicalDatabase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Company")
        company_name = cursor.fetchall()
        connection.close()
        connection = sqlite3.connect("AeronaClinicalDatabase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Product")
        product_list = cursor.fetchall()
        connection.close()
        return render_template("CreateNewForm.html", companies = company_name, products = product_list)
    else:
        return redirect("/Login")

@app.route("/EditForm/<order_id>")
def edit_form(order_id):
    if "username" in session:
        connection = sqlite3.connect("AeronaClinicalDatabase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Company")
        company_name = cursor.fetchall()
        connection.close()
        connection = sqlite3.connect("AeronaClinicalDatabase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Product")
        product_list = cursor.fetchall()
        connection.close()
#Getting the Company ID and Company name so that i can prefil the edit form page
        connection = sqlite3.connect("AeronaClinicalDatabase.db")
        cursor = connection.cursor()
        company_id = ''' SELECT companyID FROM Orders WHERE orderNo = %s ''' % (order_id)
        cursor.execute(company_id)
        company_num = cursor.fetchall()
        cursor.execute(''' SELECT companyName FROM Company WHERE companyID = (%s) ''' % (company_id))
        company_detail = cursor.fetchall()
#Selecting the consignment number so that i can prefil the edit form page
        consignment_id = ''' SELECT consignmentNo FROM Orders WHERE orderNo = %s ''' % (order_id)
        cursor.execute(consignment_id)
        consignment_detail = cursor.fetchall()
#Selecting the weight so that i can prefil the edit form page
        weight_id = ''' SELECT weight FROM Orders WHERE orderNo = %s ''' % (order_id)
        cursor.execute(weight_id)
        weight_detail = cursor.fetchall()
#Selecting the number of boxes so that i can prefil the edit form page
        box_id = ''' SELECT noOfBoxes FROM Orders WHERE orderNo = %s ''' % (order_id)
        cursor.execute(box_id)
        box_detail = cursor.fetchall()
#Selecting the date so that i can prefil the edit form page
        date_id = ''' SELECT date FROM Orders WHERE orderNo = %s ''' % (order_id)
        cursor.execute(date_id)
        date_detail = cursor.fetchall()
        connection.close()
        return render_template('EditForm.html', date_detail = date_detail, consignment_detail = consignment_detail, weight_detail = weight_detail, box_detail = box_detail, companies = company_name, company_num = company_num, company_detail = company_detail, products = product_list, order_id = order_id)

    else:
        return redirect("/Login")

@app.route("/AddUser", methods = ["POST", "GET"])
def add_user():
# Paired programming, Haroon helping Rehan
    if "username" in session and session['admin'] == 'True':
        connection = sqlite3.connect("AeronaClinicalDatabase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users")
        UserInfo = cursor.fetchall()
        connection.close()

        print("User info is:", UserInfo)
        print(type(UserInfo[0]))


        if request.method == "POST":
            try:
                username = request.form['username']
                password = request.form['password']
                admin_right = request.form.get('admin')
                print(username)
                print(password)
                print("Rights:", admin_right)
                print("type:", type(admin_right))

                if admin_right == "on":
                    connection = sqlite3.connect("AeronaClinicalDatabase.db")
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO Users ('userName', 'password', 'admin')\
                    VALUES (?,?,?)",(username, password, "true") )
                    connection.commit()
                    connection.close()

                else:
                    connection = sqlite3.connect("AeronaClinicalDatabase.db")
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO Users ('userName', 'password', 'admin')\
                    VALUES (?,?,?)",(username, password, "false") )
                    connection.commit()
                    connection.close()

# End of paired programming
            except:
                userID = request.form['UserID']
                rights_admin = request.form.get('right_admin')

                if rights_admin == "true":
                    connection = sqlite3.connect("AeronaClinicalDatabase.db")
                    cursor = connection.cursor()
                    admin_privileges = '''UPDATE Users SET admin = 'true' WHERE userID = %s''' %(userID)
                    cursor.execute(admin_privileges)
                    connection.commit()
                    connection.close()
                    print("SELECT *")

                elif rights_admin == "false":
                    connection = sqlite3.connect("AeronaClinicalDatabase.db")
                    cursor = connection.cursor()
                    admin_privileges = '''UPDATE Users SET admin = 'false' WHERE userID = %s''' %(userID)
                    cursor.execute(admin_privileges)
                    connection.commit()
                    connection.close()

                else:
                    connection = sqlite3.connect("AeronaClinicalDatabase.db")
                    cursor = connection.cursor()
                    admin_privileges = '''UPDATE Users SET admin = 'null' WHERE userID = %s''' %(userID)
                    cursor.execute(admin_privileges)
                    connection.commit()
                    connection.close()

            return redirect("/AddUser")

        return render_template("addUser.html", members = UserInfo)



    else:
        return redirect("/Login")

@app.route("/FAQ", methods = ["POST", "GET"])
def faqs():
    if "username" in session:
        connection = sqlite3.connect("AeronaClinicalDatabase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM FAQ")
        QandA = cursor.fetchall()
        connection.close()

        if request.method == "POST":
            question = request.form['DBquestion']
            answer = request.form['DBanswer']

            try:
                connection = sqlite3.connect("AeronaClinicalDatabase.db")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO FAQ ('questions', 'answers')\
                VALUES (?,?)",(question, answer) )
                connection.commit()
                connection.close()

            except:
                connection.rollback()
                flash("Q and A was not added","danger")
            finally:
                connection.close()
                return redirect("/FAQ")
        return render_template("FAQ.html", quests = QandA)

    else:
        return redirect("/Login")


@app.route("/AddCompany", methods=["GET","POST"])
def add_company():
    if "username" in session and session['admin'] == 'True':
        if request.method =='GET':
            return render_template('AddCompany.html')

        if request.method =='POST':
            companyname = request.form['companyName']
            deliveryaddress = request.form['deliveryAddress']
            legaladdress = request.form['legalAddress']
            deliverycontact = request.form['deliveryContact']
            telenumber = request.form['telephoneNumber']
            try:
                conn = sqlite3.connect("AeronaClinicalDatabase.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO Company ('companyName', 'deliveryAddress', 'legalAddress', 'deliveryContact', 'telephone')\
                VALUES (?,?,?,?,?)",(companyname, deliveryaddress, legaladdress, deliverycontact, telenumber) )
                conn.commit()
                flash("Company Was Successfully Added","success")
            except:
                conn.rollback()
                flash("Company Was Not Added","danger")
            finally:
                conn.close()
            return render_template('AddCompany.html')

    else:
        return redirect("/Login")



@app.route("/RenderForm", methods=["GET", "POST"])
def render_form():
    if "username" in session:
        referrer = request.referrer                                 #Haroon adapted from "https://stackoverflow.com/questions/28593235/get-referring-url-for-flask-request"
        newref = referrer.split("/")
        print(newref[-1])
        if newref[-1] == "CreateForm":
            if request.method == 'POST':
                company_id = request.form['formCompanyName']
                date = request.form['orderDate']
                consignment_number = request.form['consignmentNumber']
                weight = request.form['weight']
                boxes = request.form['numberOfBoxes']
                connection = sqlite3.connect("AeronaClinicalDatabase.db")
                cursor = connection.cursor()
                sql = '''SELECT companyName FROM Company WHERE companyID = %s''' % (company_id)
                cursor.execute(sql)
                company_name = cursor.fetchall()
                connection.close()

                conn = sqlite3.connect("AeronaClinicalDatabase.db")
                sql = ''' INSERT INTO Orders(companyID,userID,date,accountReference,acCOD,consignmentNo,noOfPallets,noOfBoxes,weight,transportCompany)
                        VALUES(?,?,?,?,?,?,?,?,?,?) '''
                cur = conn.cursor()
                print(session['userID'])
                data_tuple = (company_id,session['userID'],date,company_name[0][0],company_name[0][0],consignment_number,boxes,boxes,weight,consignment_number)
                cur.execute(sql, data_tuple)
                conn.commit()
                conn.close()


                conn = sqlite3.connect("AeronaClinicalDatabase.db")
                sql = ''' SELECT orderNo FROM Orders ORDER BY orderNo DESC LIMIT 1 '''
                cur = conn.cursor()
                cur.execute(sql)
                current_orderID = cur.fetchall()
                conn.close()


                quantities = request.form['listedQuantities']
                print("quantities from JAVASCRIPT: \n",quantities)
                quantities = quantities.split(",")
                enumerated_quantities = []
                for i in range(len(quantities)):
                    enumerated_quantities.append((i + 1, quantities[i]))
                for product in enumerated_quantities:
                    if product[1] == "0":
                        continue
                    else:
                        orderID = current_orderID[0][0]
                        productID = product[0]
                        quantity = product[1]
                        conn = sqlite3.connect("AeronaClinicalDatabase.db")
                        sql = ''' INSERT INTO OrdersToProduct(orderNo,productID,quantity)
                        VALUES(?,?,?) '''
                        cur = conn.cursor()
                        data_tuple = (orderID,productID,quantity)
                        cur.execute(sql, data_tuple)
                        conn.commit()
                        conn.close()


                conn = sqlite3.connect("AeronaClinicalDatabase.db")
                get_order = ''' SELECT * FROM Orders ORDER BY orderNo DESC LIMIT 1 '''
                cur = conn.cursor()
                cur.execute(get_order)
                latest_order = cur.fetchall()
                get_products = ''' SELECT * FROM OrdersToProduct WHERE orderNo = %s''' % (latest_order[0][0])
                cur.execute(get_products)
                latest_products_id = cur.fetchall()

                print("latest products id: ",latest_products_id)

                products_list = []

                for product in latest_products_id:
                    get_prodcts_information = ''' SELECT * FROM Product WHERE productID = %s''' % (product[1])
                    cur.execute(get_prodcts_information)
                    products_information = cur.fetchall()
                    products_list.append((products_information,product[2]))

                get_company = ''' SELECT * FROM Company WHERE companyID = %s''' % (latest_order[0][1])
                cur.execute(get_company)
                company_info = cur.fetchall()
                conn.close()
                print("latestorder: ", latest_order)
                print("productslist: ",products_list)
                print("companyinfo: ", company_info)

                return redirect(url_for("view_form", order_id=latest_order[0][0]))

        elif newref[-2] == "EditForm":
            if request.method == 'POST':
                company_id = request.form['formCompanyName']
                date = request.form['orderDate']
                consignment_number = request.form['consignmentNumber']
                weight = request.form['weight']
                boxes = request.form['numberOfBoxes']

                connection = sqlite3.connect("AeronaClinicalDatabase.db")
                cursor = connection.cursor()
                sql = '''SELECT companyName FROM Company WHERE companyID = %s''' % (company_id)
                cursor.execute(sql)
                company_name = cursor.fetchall()
                connection.close()

                conn = sqlite3.connect("AeronaClinicalDatabase.db")
                cur = conn.cursor()
                print(session['userID'])
                # Haroon adapted from "https://stackoverflow.com/questions/33913742/sqlite3-operationalerror-near-syntax-error-updating-database to fix syntax errors"
                cur.execute(""" UPDATE Orders set companyID = ?, userID = ?, date = ?, accountReference = ?, acCOD = ?, consignmentNo = ?, noOfPallets = ?, noOfBoxes = ?, weight = ?, transportCompany = ? WHERE orderNo = ?;""", (company_id, session['userID'], date, company_name[0][0], company_name[0][0], consignment_number, boxes, boxes, weight, consignment_number, newref[-1]))
                # End reference
                conn.commit()
                conn.close()


                conn = sqlite3.connect("AeronaClinicalDatabase.db")
                sql = ''' SELECT orderNo FROM Orders ORDER BY orderNo DESC LIMIT 1 '''
                cur = conn.cursor()
                cur.execute(sql)
                current_orderID = cur.fetchall()
                conn.close()

                conn = sqlite3.connect("AeronaClinicalDatabase.db")
                sql = ''' DELETE from OrdersToProduct WHERE orderNO = %s ''' % newref[-1]
                print("SQL:", sql)
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                conn.close()

                quantities = request.form['listedQuantities']
                print("quantities from JAVASCRIPT: \n",quantities)
                quantities = quantities.split(",")
                enumerated_quantities = []
                for i in range(len(quantities)):
                    enumerated_quantities.append((i + 1, quantities[i]))
                for product in enumerated_quantities:
                    if product[1] == "0":
                        continue
                    else:
                        orderID = newref[-1]
                        print("orderID:", orderID)
                        productID = product[0]
                        quantity = product[1]
                        conn = sqlite3.connect("AeronaClinicalDatabase.db")
                        sql = ''' INSERT INTO OrdersToProduct(orderNo,productID,quantity)
                        VALUES(?,?,?) '''
                        cur = conn.cursor()
                        data_tuple = (orderID,productID,quantity)
                        cur.execute(sql, data_tuple)
                        conn.commit()
                        conn.close()


                conn = sqlite3.connect("AeronaClinicalDatabase.db")
                get_order = ''' SELECT * FROM Orders ORDER BY orderNo DESC LIMIT 1 '''
                cur = conn.cursor()
                cur.execute(get_order)
                latest_order = cur.fetchall()
                get_products = ''' SELECT * FROM OrdersToProduct WHERE orderNo = %s''' % (latest_order[0][0])
                cur.execute(get_products)
                latest_products_id = cur.fetchall()

                print("latest products id: ",latest_products_id)

                products_list = []

                for product in latest_products_id:
                    get_prodcts_information = ''' SELECT * FROM Product WHERE productID = %s''' % (product[1])
                    cur.execute(get_prodcts_information)
                    products_information = cur.fetchall()
                    products_list.append((products_information,product[2]))

                get_company = ''' SELECT * FROM Company WHERE companyID = %s''' % (latest_order[0][1])
                cur.execute(get_company)
                company_info = cur.fetchall()
                conn.close()
                print("latestorder: ", latest_order)
                print("productslist: ",products_list)
                print("companyinfo: ", company_info)
                return redirect(url_for("view_form", order_id = newref[-1]))

        else:
            return "What happened here"

    else:
        return redirect(url_for("login"))

@app.route('/Form/<order_id>', methods = ['POST','GET'])
def view_form(order_id):
    if "username" in session:
        conn = sqlite3.connect("AeronaClinicalDatabase.db")
        get_order = ''' SELECT * FROM Orders WHERE orderNo = %s ''' % (order_id)
        cur = conn.cursor()
        cur.execute(get_order)
        latest_order = cur.fetchall()
        get_products = ''' SELECT * FROM OrdersToProduct WHERE orderNo = %s''' % (latest_order[0][0])
        cur.execute(get_products)
        latest_products_id = cur.fetchall()

        products_list = []

        for product in latest_products_id:
            get_prodcts_information = ''' SELECT * FROM Product WHERE productID = %s''' % (product[1])
            cur.execute(get_prodcts_information)
            products_information = cur.fetchall()
            products_list.append((products_information,product[2]))

        get_company = ''' SELECT * FROM Company WHERE companyID = %s''' % (latest_order[0][1])
        cur.execute(get_company)
        company_info = cur.fetchall()
        conn.close()

        return render_template('RenderForm.html', order_details = latest_order, products = products_list, company = company_info)
    else:
        return redirect("/Login")



@app.route('/AddProduct' , methods = ['POST','GET'])
def add_product():
    if "username" in session and session['admin'] == 'True':
        if request.method =='GET':
            return render_template('addproduct.html')

        if request.method =='POST':
            addproduct = request.form['product_name']
            addcondition = request.form['_conditions']
            addbatch = request.form['_batchNo']
            addorigin = request.form['_origin']
            addexpiry = request.form['_expiryDate']
            print("adding product:", addproduct)
            print("adding conditions:", addcondition)
            print("adding batchNo:", addbatch)
            print("adding origin:", addorigin)
            print("adding expiryDate:", addexpiry)
            time.sleep(3)
            #Paired programming Haroon Mohammed helping Sami Ahmed
            try:
                conn = sqlite3.connect("AeronaClinicalDatabase.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO Product ('productName', 'conditions', 'batchNo', 'origin', 'expiryDate')\
                VALUES (?,?,?,?,?)",(addproduct, addcondition, addbatch, addorigin, addexpiry) )
            #End of paired programming
                conn.commit()
                msg = "Record successfully added"
            except:
                conn.rollback()
                msg = "error in insert operation"
            finally:
                conn.close()
            return render_template('addproduct.html')


    else:
        return redirect("/Login")



@app.route("/ProductUpdate")
def ProductConnection():
    if "username" in session and session['admin'] == 'True':
        connection = sqlite3.connect("AeronaClinicalDatabase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Product")
        product_list = cursor.fetchall()
        connection.close()
        return render_template("ProductSearch.html", products = product_list)
    else:
        return redirect("/Login")


@app.route("/update_product/<Product_ID>", methods=["GET", "POST"])
def UpdatingProduct(Product_ID):
    if request.method =='GET':
        return redirect("/Dashboard")
    if request.method == 'POST':
        Nproduct = request.form['new_product_name']
        Ncondition = request.form['new_product_condition']
        Nbatch = request.form['new_product_Batch']
        Norigin = request.form['new_product_origin']
        Nexpiry = request.form['new_product_ED']
        conn = sqlite3.connect("AeronaClinicalDatabase.db")
        cur = conn.cursor()
        time.sleep(3)
        cur.execute(""" UPDATE Product set productName = ?, conditions = ?, batchNo = ?, origin = ?, expiryDate = ? WHERE productID = ?;""", (Nproduct, Ncondition, Nbatch, Norigin, Nexpiry, Product_ID))
        print(Nproduct)
        conn.commit()
        conn.close()
        return redirect("/ProductUpdate")

@app.route("/DuplicateForm/<order_id>")
def duplicate_Form(order_id):
    if "username" in session:
        conn = sqlite3.connect('AeronaClinicalDatabase.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM Orders WHERE orderNo = %s"%(order_id))
        form = cur.fetchall()
        cur.execute("SELECT orderNo FROM Orders")
        numbers = cur.fetchall()
        count = 0
        #print(numbers)
        #print(form)
        '''for i in numbers:
            if i[0] > count:
                count = i[0]
        count += 1'''

        #print(form)
        print("form before:", form)
        form = form[0]
        print("form after:", form)
        cur.execute("INSERT INTO Orders ('companyID', 'userID', 'date', 'accountReference', 'acCOD', 'consignmentNo', 'noOfPallets', 'noOfBoxes', 'weight', 'transportCompany')\
        VALUES (?,?,?,?,?,?,?,?,?,?)",(form[1:]))
        conn.commit()
        conn.close()
        return redirect("/Dashboard")
    else:
        return redirect("/Login")

@app.route("/ProductDelete")
def ProducttableConnection():
    if "username" in session and session['admin'] == 'True':
        connection = sqlite3.connect("AeronaClinicalDatabase.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Product")
        product_list = cursor.fetchall()
        connection.close()
        return render_template("ProductDelete.html", products = product_list)
    else:
        return redirect("/Login")

@app.route("/delete_product/<Product_ID>", methods=["GET", "POST"])
def DeleteProduct(Product_ID):
    if request.method =='GET':
        return redirect("/Dashboard")
    if request.method == 'POST':
        conn = sqlite3.connect("AeronaClinicalDatabase.db")
        cur = conn.cursor()
        cur.execute(""" DELETE FROM Product WHERE productID = ?;""", (Product_ID))
        print("success")
        conn.commit()
        conn.close()
        return redirect("/ProductDelete")

@app.route("/logout")
def logout():
    try:
        session.clear()           #Session.Clear() taken from "https://stackoverflow.com/questions/27747578/how-do-i-clear-a-flask-session#:~:text=There%20is%20no%20way%20to,session%20dictionary%20will%20get%20erased."
        flash("Log Out Successful","info")
    except:
        pass
    return redirect(url_for("login"))
#############################

#Here is where the code was

#############################
'''@app.route("/createNewForm")
def createNewForm():
    pass
'''
if __name__ == "__main__":
    app.run(debug=True)
