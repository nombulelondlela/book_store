from flask import Flask, render_template, request, redirect, url_for, session

import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management


# Configure MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bookstoredb"
)
cursor = db.cursor()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form ['password']
    
        
        # Insert user registration data into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
    
        # Redirect to login page after registration
        return redirect(url_for('login'))

    return render_template('registration.html')
    
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return render_template('index.html')
        # Process login logic here
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Placeholder login check
        if username == 'admin' and password == 'password':
            # Successful login, redirect to index page
            return redirect(url_for('index'))
        else:
            # Failed login, render login page with error message
            error_message = "Invalid username or password"
            return render_template('login.html', error_message=error_message)
            
    return render_template('login.html')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        
        # Fetch data from the database based on the keyword
        cursor.execute("SELECT * FROM books WHERE title LIKE %s OR author LIKE %s",
                       (f"%{keyword}%", f"%{keyword}%"))
        search_results = cursor.fetchall()
        
        return render_template('search.html', keyword=keyword, search_results=search_results)

    return render_template('search.html')
    

@app.route('/books')
def books():
    # Retrieve book data from the database
    cursor.execute("SELECT * FROM books")
    books_data = cursor.fetchall()
    return render_template('books.html', books_data=books_data)


@app.route('/books/<int:book_id>')
def book_details(book_id):
    # Retrieve individual book details from the database
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    if book:
        return render_template('book_details.html', book=book)
    else:
        return "Book not found"

# Placeholder for book data (Replace with actual data or database)
books_data = {
    1: {'title': 'Book 1', 'author': 'Author 1', 'description': 'Description of Book 1'},
    2: {'title': 'Book 2', 'author': 'Author 2', 'description': 'Description of Book 2'}
}

@app.route('/new_releases')
def new_releases():
    return render_template('new_releases.html')

    
if __name__ == '__main__':
    app.run(debug=True)
