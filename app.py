from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask (__name__)

# Database Connections
def get_conn_company():
    return mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "root", 
        database = "company_db")

def get_conn_school():
    return mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "root", 
        database = "school_db")

def get_conn_store():
    return mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "root", 
        database = "store_db")

# EMPLOYEE ROUTES (company_db)
@app.route('/employees')
def employees():
    conn = get_conn_company()
    cursor = conn.cursor (dictionary=True)
    cursor.callproc('ShowAllEmployees')
    for result in cursor.stored_results():
        data = result.fetchall() 
    cursor.close(); conn.close()
    return render_template('employees.html', employees=data) 

@app.route ('/employees/add', methods = ['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        name = request.form['emp_name']
        dept = request.form['dept']
        salary = request.form['salary']
        conn = get_conn_company(); cursor = conn.cursor()
        cursor.callproc('AddEmployee', (emp_id, name, dept, salary))
        conn.commit(); cursor.close(); conn.close()
        return redirect('/employees')
    return render_template('add_employee.html')

@app.route ('/employees/edit/<int:id>', methods = ['GET', 'POST'])
def edit_employee(id):
    conn = get_conn_company()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc('GetEmployeeByID', [id])
    for result in cursor.stored_results():
        emp = result.fetchone()
    cursor.close(); conn.close()
    if request.method == 'POST':
        name = request.form['emp_name']
        dept = request.form['dept']    
        salary = request.form['salary']
        conn = get_conn_company(); cursor = conn.cursor()
        cursor.callproc('UpdateEmployee', (id, name, dept, salary))
        conn.commit(); cursor.close(); conn.close()
        return redirect('/employees')
    return render_template('edit_employee.html', emp=emp)

@app.route ('/employees/delete/<int:id>')
def delete_employee(id):
    conn = get_conn_company(); cursor = conn.cursor()
    cursor.callproc('DeleteEmployee', [id])
    conn.commit(); cursor.close(); conn.close()
    return redirect ('/employees')

@app.route ('/')
def home():
    return render_template('home.html')


# STUDENT ROUTES (school_db)

@app.route('/students')
def students():
    conn = get_conn_school()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc('ShowAllStudents')
    for result in cursor.stored_results():
        data = result.fetchall()
    cursor.close(); conn.close()
    return render_template('students.html', students=data)
                           
@app.route('/students/add',methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        sid=request.form['sid']
        name = request.form['name']
        course=request.form['course']
        marks=request.form['marks']
        conn=get_conn_school();cursor=conn.cursor()
        cursor.callproc('AddStudent',(sid,name,course,marks))
        conn.commit();cursor.close();conn.close()
        return redirect('/students')
    return render_template('add_student.html')

@app.route('/students/edit/<int:id>',methods=['GET','POST'])
def edit_student(id):
    conn = get_conn_school()
    cursor=conn.cursor(dictionary=True)
    cursor.callproc('GetStudentByID',[id])
    for result in cursor.stored_results():
        stu=result.fetchone()
    cursor.close();conn.close()
    if request.method == 'POST':
        name=request.form['name']
        course=request.form['course']
        marks=request.form['marks']
        conn=get_conn_school(); cursor=conn.cursor()
        cursor.callproc('UpdateStudent',(id,name,course,marks))
        conn.commit();cursor.close();conn.close()
        return redirect('/students')
    return render_template('edit_student.html',stu=stu)


@app.route('/students/delete/<int:id>')
def delete_student(id):
    conn = get_conn_school(); cursor = conn.cursor()
    cursor.callproc('DeleteStudentM', [id])
    conn.commit(); cursor.close(); conn.close()
    return redirect('/students')
 
 
# ================= PRODUCTS (store_db) =================

@app.route('/products')
def products():
    conn = get_conn_store(); cursor = conn.cursor(dictionary=True)
    cursor.callproc('ShowAllProducts')
    for result in cursor.stored_results(): data = result.fetchall()
    cursor.close(); conn.close()
    return render_template('products.html', products=data)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        conn = get_conn_store(); cursor = conn.cursor()
        cursor.callproc('AddProduct', (request.form['pid'], request.form['name'], request.form['category'], request.form['price']))
        conn.commit(); cursor.close(); conn.close()
        return redirect('/products')
    return render_template('add_product.html')

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = get_conn_store(); cursor = conn.cursor(dictionary=True)
    cursor.callproc('GetProductById', [id])
    for result in cursor.stored_results(): prod = result.fetchone()
    cursor.close(); conn.close()
    if request.method == 'POST':
        conn = get_conn_store(); cursor = conn.cursor()
        cursor.callproc('UpdateProduct', (id, request.form['name'], request.form['category'], request.form['price']))
        conn.commit(); cursor.close(); conn.close()
        return redirect('/products')
    return render_template('edit_product.html', prod=prod)

@app.route('/products/delete/<int:id>')
def delete_product(id):
    conn = get_conn_store(); cursor = conn.cursor()
    cursor.callproc('DeleteProduct', [id])
    conn.commit(); cursor.close(); conn.close()
    return redirect('/products')

if __name__ == '__main__':
    app.run(debug=True)