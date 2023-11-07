import streamlit as st
import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysqlroot",
    database="bs"
)

# In the global scope, initialize the flag using st.session_state
if 'flag' not in st.session_state:
    st.session_state.flag = 0

mycursor = mydb.cursor()

# User registration function
def register_user(name, email, password):
    sql = "INSERT INTO user (username, email, password) VALUES (%s, %s, %s)"
    val = (name, email, password)
    mycursor.execute(sql, val)
    mydb.commit()

# User login function
def login_user(email, password):
    sql = "SELECT * FROM user WHERE email = %s AND password = %s"
    val = (email, password)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    print(user)
    if user is not None:
        st.session_state.flag = 1  # Update flag in st.session_state
    print("Flag is now:", st.session_state.flag)
    return user

# User logout function
def logout_user():
    st.session_state.flag = 0  # Reset flag in st.session_state

st.title("Library Management System")
options = st.sidebar.selectbox("Select an Operation", ("Register", "Login", "Search Book", "Rent", "Logout"))

if options == "Register":
    st.subheader("User Registration")
    name = st.text_input("Enter UserName")
    email = st.text_input("Enter Email")
    password = st.text_input("Enter Password", type="password")
    if st.button("Register"):
        register_user(name, email, password)
        st.write("Registration successful!")
        st.write("Now you can log in with Email Id")

if options == "Login":
    st.subheader("User Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.write(f"Welcome, {user[1]}!")
        else:
            st.write("Login failed. Please check your credentials")

if options == "Search Book":
    print("Flag inside search book is:", st.session_state.flag)
    print('---')
    st.subheader("Search a Book")
    bookName = st.text_input("Enter the book name: ")
    if st.button("Search Book"):
        sql = "SELECT name FROM book WHERE name = %s"
        val = (bookName,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if result and st.session_state.flag == 1:
            st.subheader("Book Found")
            st.subheader("Go to the rent page to borrow the book!")
            for row in result:
                st.write(row[0])
        else:
            if st.session_state.flag == 0:
                st.write("Flag is 0")
            st.write("Book Not Found!!")

if options == "Rent":
    st.subheader("Dashboard")
    bookName = st.text_input("Enter the book name: ")
    rentName = st.text_input("Enter your name: ")

    if st.button("Rent"):
        sql = "INSERT INTO rented_books (book_name, user_name) VALUES (%s, %s)"
        val = (bookName, rentName)
        mycursor.execute(sql, val)
        mydb.commit()
        st.write("Book rented successfully!")

if options == "Logout":
    logout_user()
    st.write("You have been logged out")

mydb.close()
