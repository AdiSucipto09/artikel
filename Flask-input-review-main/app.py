from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import pymysql
import os
from flask import send_file

app = Flask(__name__)

# Database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'review',
}

# Folder for upload img
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'gif'}
@app.route('/get_image/<path:filename>')
def get_image(filename):
    return send_file(os.path.join(os.path.dirname(__file__), "uploads/{filename}"), mimetype='image/jpeg')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to insert data into MySQL
def insert_data_to_mysql(data):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Modify the SQL statement to include id_review as auto-increment
            sql = """
                CREATE TABLE IF NOT EXISTS input_review (
                    id_review INT AUTO_INCREMENT PRIMARY KEY,
                    nama VARCHAR(255) NOT NULL,
                    tanggal DATE NOT NULL,
                    review TEXT NOT NULL
                )
            """
            cursor.execute(sql)

            # Insert data into the table
            sql_insert = "INSERT INTO input_review (nama, tanggal, review) VALUES (%s, %s, %s)"
            cursor.execute(sql_insert, (data['nama'], data['tanggal'], data['review']))
        connection.commit()
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

# Function to insert article data into MySQL with image upload
def insert_article_to_mysql(article_data):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Modify the SQL statement to include id_article as auto-increment
            sql = """
                CREATE TABLE IF NOT EXISTS articles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    judul VARCHAR(255) NOT NULL,
                    gambar VARCHAR(255) NOT NULL,
                    link VARCHAR(255) NOT NULL
                )
            """
            cursor.execute(sql)

            # Save the uploaded image using secure_filename
            image_file = request.files['gambar']
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                gambar = filename
                # image_file.save(os.path.join(app.config['UPLOAD_FOLDER'],image_file.filename))

                # Insert data into the table
                sql_insert = "INSERT INTO articles (judul, gambar, link) VALUES (%s, %s, %s)"
                cursor.execute(sql_insert, (article_data['judul'], gambar, article_data['link']))

                connection.commit()
                print("Article data with image inserted successfully!")
            else:
                print("Invalid or missing image file.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def fetch_article_by_id(article_id):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql_select = "SELECT * FROM articles WHERE id = %s"
            cursor.execute(sql_select, (article_id,))
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def update_article_in_mysql(data):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Check if a new image file is provided
            if 'gambar' in data and data['gambar']:
                # Save the uploaded image using secure_filename
                image_file = data['gambar']
                if allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)
                    gambar = image_file.filename
                    gambar1 = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
                    image_file.save(gambar1)

                    # Update data in the table with the new image path
                    sql_update = "UPDATE articles SET judul = %s, link = %s, gambar = %s WHERE id = %s"
                    cursor.execute(sql_update, (data['judul'], data['link'], gambar, data['id']))
                else:
                    print("Invalid or missing image file.")
            else:
                # Update data in the table without changing the image
                sql_update = "UPDATE articles SET judul = %s, link = %s WHERE id = %s"
                cursor.execute(sql_update, (data['judul'], data['link'], data['id']))

            connection.commit()
            print("Article data updated successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

# Function to delete article from MySQL
def delete_article_from_mysql(article_id):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql_delete = "DELETE FROM articles WHERE id = %s"
            cursor.execute(sql_delete, (article_id,))
            connection.commit()
            print("Article deleted successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

# Function to get all articles from MySQL
def get_all_articles():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql_select = "SELECT * FROM articles"
            cursor.execute(sql_select)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

# Enable CORS for all routes
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

app.after_request(add_cors_headers)

# Route to render the form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('berita.html')

@app.route('/article')
def article():
    # Assume get_all_articles() returns a list of tuples representing articles
    articles_data = get_all_articles()
    return render_template('daftarArtikel.html', data=articles_data)

# Route to handle form submission
@app.route('/submit', methods=['POST', 'OPTIONS'])
def submit_form():
    if request.method == 'OPTIONS':
        # Preflight request, respond successfully
        return jsonify({'status': 'success'})

    data_to_insert = request.get_json()
    insert_data_to_mysql(data_to_insert)
    return jsonify({'status': 'success'})


# Route to handle article submission with image upload
@app.route('/submit_article', methods=['POST', 'OPTIONS'])
def submit_article_with_image():
    if request.method == 'OPTIONS':
        # Preflight request, respond successfully
        return jsonify({'status': 'success'})

    # Check if the request contains the expected form fields
    # if 'judul' not in request.form or 'gambar' not in request.files or 'link' not in request.form:
    #     return jsonify({'status': 'error', 'message': 'Invalid request data'})

    article_data_to_insert = {
        'judul': request.form['judul'],
        'gambar':request.files['gambar'].filename,  # Save only the filename
        'link': request.form['link']
    }

    insert_article_to_mysql(article_data_to_insert)

    # Save the uploaded image using secure_filename
    image_file = request.files['gambar']
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        gambar = image_file.filename
        gambar1 = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(gambar1)

    return redirect(url_for('article'))

# Route to handle article edit
@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    if request.method == 'GET':
        # Fetch the article data based on the article_id
        article_data = fetch_article_by_id(article_id)  # Implement this function as needed
        return render_template('edit_article.html', article_data=article_data)

    elif request.method == 'POST':
        # Process the form submission for article editing
        edited_data = {
            'id': article_id,
            'judul': request.form['judul'],
            'link': request.form['link'],
            'gambar': request.files['gambar']
        }
        update_article_in_mysql(edited_data)  # Implement this function to update the article
        return redirect(url_for('article'))  # Redirect to the article list page after editing

@app.route('/delete_article/<int:article_id>', methods=['GET', 'POST'])
def delete_article(article_id):
    # Implement the logic to delete the article by its ID
    delete_article_from_mysql(article_id)  # Implement this function to delete the article
    return redirect('/article')  # Redirect to the article list page after deletion

# Route to get all articles
@app.route('/get_articles', methods=['GET', 'OPTIONS'])
def get_articles():
    if request.method == 'OPTIONS':
        # Preflight request, respond successfully
        return jsonify({'status': 'success'})

    articles = get_all_articles()
    return jsonify({'status': 'success', 'articles': articles})

# Route to login
@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        # Preflight request, respond successfully
        return jsonify({'status': 'success'})

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validation logic
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            query = 'SELECT * FROM admin WHERE username = %s AND password = %s'
            cursor.execute(query, (username, password))
            result = cursor.fetchall()

            if result:
                return jsonify({'success': True, 'message': 'Login successful'})
            else:
                return jsonify({'success': False, 'message': 'Invalid credentials'})
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
