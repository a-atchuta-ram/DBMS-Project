import streamlit as st
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1234",
    database = "dbms"
)

mycursor = mydb.cursor()

bi = """
    <style>
    body {
        background-image: url("https://images2.alphacoders.com/261/26102.jpg");
        background-size: cover;
    }
    </style>
"""


st.markdown(bi, unsafe_allow_html=True)


def main():

    st.title("Library Management System")
    options = st.sidebar.selectbox("Select an Operation",("Search Book", "Rent", "Update", "Delete"))

    if(options == "Search Book"):
        st.subheader("Search a Book")
        bookName = st.text_input("Enter the book name: ")
        #email = st.text_input("Enter Email")
        if st.button("Search Book"):

            #sql = "select book_name from users where book_name = %s" ## Change the sql query
            sql = ""
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

