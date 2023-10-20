import streamlit as st
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1234",
    database = "dbms"
)

mycursor = mydb.cursor()


def main():

    st.title("Library Management System")
    options = st.sidebar.selectbox("Select an Operation",("Search Book", "Rent", "Update", "Delete"))


    if(options == "Search Book"):
        st.subheader("Search a Book")
        bookName = st.text_input("Enter the name: ")
        email = st.text_input("Enter Email")
        if st.button("Search Book"):
            sql = "insert into users(name, email) values(%s, %s)" ## Change the query
            val = (bookName, email)
            result = mycursor.execute(sql, val)
            if(result):
                st.subheader("Book Found")
                st.subheader("Go to the rent page to borrow the book!!")
                st.write(result)    

        if(options == "Rent"):
            st.subheader("DashBoard")
            bookName = st.text_input("Enter the book name: ")
            authorName = st.text_input("Enter the author name: ")





if __name__ == "__main__":
    main()

