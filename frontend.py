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
def register_user(full_name, name, email, password):
    sql = "INSERT INTO user (full_name, username, email, password) VALUES (%s, %s, %s, %s)"
    val = (full_name, name, email, password)
    mycursor.execute(sql, val)
    mydb.commit()

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

# Lend Feature
def lend_book(book_name, owner_username, author, genre, book_info):
    try:
        # Get the owner_id based on the provided username
        mycursor.execute("SELECT id FROM user WHERE username = %s", (owner_username,))
        owner_id_result = mycursor.fetchone()

        if owner_id_result:
            owner_id = owner_id_result[0]

            # Insert into the book table
            mycursor.execute("INSERT INTO book (name, owner_id, author, genre, book_info, available, times_rented) VALUES (%s, %s, %s, %s, %s, 1, 0)",
                             (book_name, owner_id, author, genre, book_info))

            # Update books_shared for the owner
            mycursor.execute("UPDATE user SET books_shared = books_shared + 1 WHERE id = %s", (owner_id,))

            # Get the last inserted book_id
            mycursor.execute("SELECT LAST_INSERT_ID()")
            book_id_result = mycursor.fetchone()
            book_id = book_id_result[0] if book_id_result else None

            if book_id:
                # Set a sentinel value for rentee_id
                rentee_id = -1  # You can use any sentinel value you prefer

                # Insert into the rent table
                sql = "INSERT INTO rent (rent_date, book_id, rentee_id, renter_id, status) VALUES (NOW(), %s, %s, %s, 'A')"
                val = (book_id, rentee_id, owner_id)
                mycursor.execute(sql, val)

                mydb.commit()
                st.write("Book lent successfully!")
            else:
                st.write("Failed to get book_id.")
        else:
            st.write("Owner not found.")
    except Exception as e:
        st.write(f"An error occurred: {e}")

# Rent Feature
def rent_book(book_name, rentee_name):
    try:
        # Check if the book is available for rent
        mycursor.execute("SELECT id, available FROM book WHERE name = %s", (book_name,))
        book_info = mycursor.fetchone()

        if book_info and book_info[1] == 1:
            # Set the book as unavailable
            mycursor.execute("UPDATE book SET available = 0 WHERE id = %s", (book_info[0],))

            # Update the rentee's information
            mycursor.execute("UPDATE user SET books_rented = books_rented + 1 WHERE username = %s", (rentee_name,))

            # Update books_rented for the rentee
            mycursor.execute("UPDATE user SET books_rented = books_rented + 1 WHERE username = %s", (rentee_name,))

            # Update the existing rent record
            sql = "UPDATE rent SET rent_date = NOW(), status = 'rented', rentee_id = (SELECT id FROM user WHERE username = %s) WHERE book_id = %s AND rentee_id IS NULL"
            val = (rentee_name, book_info[0])
            mycursor.execute(sql, val)

            mydb.commit()
            st.write("Book rented successfully!")
        else:
            st.write("Book is not available for rent.")
    except Exception as e:
        st.write(f"An error occurred: {e}")

# User logout function
def logout_user():
    st.session_state.flag = 0  # Reset flag in st.session_state

st.title("Library Management System")
options = st.sidebar.selectbox("Select an Operation", ("Register", "Login", "Search Book", "Lend", "Rent", "WishList", "Logout"))

if options == "Register":
    st.subheader("User Registration")
    full_name = st.text_input("Enter Full Name:")
    name = st.text_input("Enter UserName")
    email = st.text_input("Enter Email")
    password = st.text_input("Enter Password", type="password")
    if st.button("Register"):
        register_user(full_name, name, email, password)
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
    st.subheader("Search a Book")
    bookName = st.text_input("Enter the book name: ")
    if st.button("Search Book"):
        sql = "SELECT name FROM book WHERE name LIKE %s"
        val = ('%' + bookName + '%',)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if result and st.session_state.flag == 1:
            st.subheader("Books Found")
            st.subheader("Go to the rent page to borrow the book!")
            for row in result:
                st.write(row[0])
        else:
            if st.session_state.flag == 0:
                st.write("Please Login First")
            else:
                st.write("No books found matching the given name.")

# ... (rest of your code)

if options == "Rent":
    st.subheader("Dashboard")
    bookName = st.text_input("Enter the book name: ")

    # Fetch matching book names from the database
    mycursor.execute("SELECT name FROM book WHERE name LIKE %s", ('%' + bookName + '%',))
    matching_books = mycursor.fetchall()
    matching_book_names = [book[0] for book in matching_books]

    # Dropdown for book names
    selected_book_name = st.selectbox("Select book name:", matching_book_names)

    rentName = st.text_input("Enter your username: ")

    if st.button("Rent"):
        rent_book(selected_book_name, rentName)

# ... (rest of your code)


if options == "Lend":
    st.subheader("Lend a Book")
    book_name_lend = st.text_input("Enter the book name: ")
    author = st.text_input("Enter the author: ")
    
    # Dropdown for genres
    genres = ["Mystery", "Science Fiction", "Fantasy", "Romance", "Thriller", "Historical Fiction", "Non-fiction", "Biography", "Self-Help", "Adventure"]
    selected_genre = st.selectbox("Select genre:", genres)
    
    book_info = st.text_area("Enter book information: ")
    lender_name = st.text_input("Enter your username: ")
    
    if st.button("Lend"):
        lend_book(book_name_lend, lender_name, author, selected_genre, book_info)

if options == "Logout":
    logout_user()
    st.write("You have been logged out")

mydb.close()