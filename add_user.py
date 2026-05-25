import pymysql
from werkzeug.security import generate_password_hash
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

username = input("Username: ")
email = input("Email: ")
password = input("Password: ")
role = input("Role (admin/user): ")

if role not in ["admin", "user"]:
    print("Role must be admin or user.")
    exit()

password_hash = generate_password_hash(password)

conn = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
        """, (username, email, password_hash, role))

    conn.commit()
    print("User added successfully.")

except pymysql.err.IntegrityError:
    print("Username or email already exists.")

finally:
    conn.close()