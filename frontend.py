import streamlit as st
import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="books"
)

global flag
flag = 0
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
    return user

def main():
    # global flag
    # flag = 0
    st.title("Library Management System")
    options = st.sidebar.selectbox("Select an Operation", ("Register", "Login", "Search Book", "Rent"))

    if options == "Register":
        st.subheader("User Registration")
        name = st.text_input("Enter UserName")
        email = st.text_input("Enter Email")
        password = st.text_input("Enter Password", type="password")
        if st.button("Register"):
            register_user(name, email, password)
            st.write("Registration successful!")
            st.write("Now you can login with Email Id")

    if options == "Login":
        st.subheader("User Login")
        email = st.text_input("Emails")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            hashed_password = (password)
            user = login_user(email, hashed_password)
            if user:
                st.write(f"Welcome, {user[1]}!")    
                flag = 1
            else:
                st.write("Login failed. Please check your credentials.")

    if(options == "Search Book"):
        if(flag == 0):
            st.write("Please Login First!")
        else:
            st.subheader("Search a Book")
            bookName = st.text_input("Enter the book name: ")
            if st.button("Search Book"):
                sql = "select book_name from book where book_name = %s" ## Change the sql query
                val = (bookName)
                result = mycursor.execute(sql, val)
                if(result):
                    st.subheader("Book Found")
                    st.subheader("Go to the rent page to borrow the book!")
                    st.write(result) 
                else:
                    st.write("Book Not Found!!")   

    if(options == "Rent"):
        st.subheader("DashBoard")
        bookName = st.text_input("Enter the book name: ")
        rentName = st.text_input("Enter your name: ")
    
        if st.button("Rent"):
            sql = ""
            val = (bookName,rentName)

            result = mycursor.execute(sql, val)
            if(result):
                st.write(result)
            else:
                st.write("Something went wrong!!")


if __name__ == "__main__":
    main()

