from werkzeug.security import generate_password_hash

from applib.model import Users, sql_cursor


def add_new_user():
    try:
        hashed_pass = generate_password_hash('qwerty')
        print(hashed_pass)
        new_user = Users(username='khan', password=hashed_pass)

        with sql_cursor() as session_db:
            session_db.add(new_user)
            return new_user
            print(f"User added successfully with ID: {new_user.id}")

    except Exception as e:
        print(f"Error adding user : {e}")
        return None


if __name__ == '__main__':
    add_new_user()