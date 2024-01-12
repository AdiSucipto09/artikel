from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import pymysql
import os

app = Flask(__name__)

# Database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'review',
}

#folder for upload img
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'gif'}

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
                    link VARCHAR(255) NOT NULL,
                    id_review_to_edit INT
                )
            """
            cursor.execute(sql)

            # Save the uploaded image
            image_file = article_data['gambar']
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                gambar = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(gambar)

                # Insert or update data into the table
                if 'id_review_to_edit' in article_data:
                    sql_update = "UPDATE articles SET judul = %s, gambar = %s, link = %s WHERE id_review_to_edit = %s"
                    cursor.execute(sql_update, (article_data['judul'], gambar, article_data['link'], article_data['id_review_to_edit']))
                else:
                    sql_insert = "INSERT INTO articles (judul, gambar, link) VALUES (%s, %s, %s)"
                    cursor.execute(sql_insert, (article_data['judul'], gambar, article_data['link']))

                connection.commit()
                print("Article data with image inserted or updated successfully!")
            else:
                print("Invalid or missing image file.")
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

    article_data_to_insert = {
        'judul': request.form['judul'],
        'link': request.form['link'],
        'gambar': request.files['gambar']
    }
    insert_article_to_mysql(article_data_to_insert)
    return jsonify({'status': 'success'})

# Route to handle article edit
@app.route('/edit_article', methods=['POST', 'OPTIONS'])
def edit_article():
    if request.method == 'OPTIONS':
        # Preflight request, respond successfully
        return jsonify({'status': 'success'})

    article_data_to_edit = {
        'id_review_to_edit': request.form['id_review_to_edit'],
        'judul': request.form['judul'],
        'link': request.form['link'],
        'image': request.files['gambar']
    }
    insert_article_to_mysql(article_data_to_edit)
    return jsonify({'status': 'success'})

# Route to handle article deletion
@app.route('/delete_article/<int:article_id>', methods=['DELETE', 'OPTIONS'])
def delete_article(article_id):
    if request.method == 'OPTIONS':
        # Preflight request, respond successfully
        return jsonify({'status': 'success'})

    delete_article_from_mysql(article_id)
    return jsonify({'status': 'success'})

# Route to get all articles
@app.route('/get_articles', methods=['GET', 'OPTIONS'])
def get_articles():
    if request.method == 'OPTIONS':
        # Preflight request, respond successfully
        return jsonify({'status': 'success'})

    articles = get_all_articles()
    return jsonify({'status': 'success', 'articles': articles})

#route to login
@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        # Preflight request, respond successfully
        return jsonify({'status': 'success'})

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # validation logic
    query = 'SELECT * FROM admin WHERE username = %s AND password = %s'
    cursor.execute(query, (username, password))
    result = cursor.fetchall()

    if result:
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'})

if __name__ == '__main__':
    app.run(debug=True)