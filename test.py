import mysql.connector
import streamlit as st


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1234",
    database = "dbms"
)

mycursor = mydb.cursor()


def main():
    st.title("Testing MYSQL Connection with Streamlit")
    options = st.sidebar.selectbox("Select an Operation",("Create", "Read", "Update", "Delete"))
    if(options == "Create"):
        st.subheader("Create a record")
        name = st.text_input("Enter Name")
        email = st.text_input("Enter Email")
        if st.button("Create"):
            sql = "insert into users(name, email) values(%s, %s)"
            val = (name, email)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Record Created Successfully ")


    elif options == "Read":
        st.subheader("Read Record")
        name = st.text_input("Enter the name you want to retrieve:")
        email = st.text_input("Enter the email you want to retrieve:")
        
        if st.button("Read"):  # Corrected button usage
            sql = "SELECT name, email FROM users WHERE name = %s AND email = %s"  # Fixed SQL syntax and table name
            val = (name, email)
            mycursor.execute(sql, val)
            result = mycursor.fetchone()
         
            
            if result:
                st.subheader("Record Found:")
                st.write(f"Name: {result[0]}")
                st.write(f"Email: {result[1]}")
            else:
                st.subheader("Record Not Found")
        mydb.commit()


    elif(options == "Update"):
        st.subheader("Update Record")

        ## TODO
        
    elif(options == "Delete"):
        st.subheader("Delete Record")
        name = st.text_input("Enter the name you want to delete: ")
        email = st.text_input("Enter the email you want to delete: ")

        if st.button("Delete"):
            sql = ("DELETE FROM users WHERE name = %s AND email = %s")
            val = (name, email)
            mycursor.execute(sql, val)
            result = mycursor.fetchone()

            if result:
                st.subheader("Record not Found!!")
            else:
                st.subheader("Deleted!!")
        mydb.commit()
        
        


if __name__ == "__main__":
    main()