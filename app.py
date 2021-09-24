import signal, sys
from flask import Flask, jsonify, make_response, request, url_for
import sqlite3


def db_connection():
    conn_f = None
    try:
        conn_f = sqlite3.connect('book.sqlite', check_same_thread=False)
    except sqlite3.error as e:
        print(e)
    return conn_f


conn = db_connection()
cursor = conn.cursor()

app = Flask(__name__)


@app.route('/books', methods=["GET", "POST"])
def books():
    if request.method == "GET":
        cursors = conn.execute("SELECT * FROM book")
        books_sql = [
            dict(id=row[0], author=row[1], title=row[2], page_number=row[3])
            for row in cursors.fetchall()
        ]
        if books_sql is not None:
            return jsonify(books_sql)

    if request.method == "POST":
        author = request.json['author']
        title = request.json['title']
        page_number = request.json['page_number']

        sql = """INSERT INTO book (author, title, page_number) VALUES (?, ?, ?)"""

        conn.execute(sql, (author, title, page_number))
        conn.commit()
        return jsonify(f"Book created successfully !"), 201


@app.route('/books/<id_book>', methods=['GET', 'PUT', 'DELETE'])
def get_book(id_book):
    book = None

    if request.method == "GET":
        cursors = conn.execute(f"SELECT * FROM book WHERE id={id_book}")
        rows = cursors.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something wrong", 404

    if request.method == "PUT":
        sql = """UPDATE book SET author=?, title=?, page_number=? WHERE id=? """
        author = request.json["author"]
        title = request.json["title"]
        page_number = request.json["page_number"]

        updated_book = {
            "id": id_book,
            "author": author,
            "title": title,
            "page_number": page_number,
        }
        conn.execute(sql, (author, title, page_number, id_book))
        conn.commit()
        return jsonify(updated_book)

    if request.method == "DELETE":
        sql = """ DELETE FROM book WHERE id=? """
        conn.execute(sql, (id_book,))
        conn.commit()
        return jsonify(f'The book with id: {id_book} has been deleted.'), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def signal_handler(sig, frame):
    cursor.close()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    app.run()
