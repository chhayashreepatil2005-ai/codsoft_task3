import sqlite3
import hashlib

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")
conn.commit()


def register():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if len(username) < 3:
        print("Username must contain at least 3 characters.")
        return

    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute(
            "INSERT INTO students (username, password) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        print("Registration successful!")
    except sqlite3.Error:
        print("Registration failed.")


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute(
        "SELECT * FROM students WHERE username = ? AND password = ?",
        (username, password_hash)
    )

    user = cursor.fetchone()

    if user:
        print("\nLogin successful!")
        print("Welcome,", username)
    else:
        print("\nInvalid username or password.")


def main():
    while True:
        print("\n===== STUDENT LOGIN SYSTEM =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Thank you for using the application.")
            break
        else:
            print("Invalid choice.")


main()
conn.close()
