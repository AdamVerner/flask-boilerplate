from app import create_app, db
from app.models import Admin

app = create_app()


def add_admin(username, password):
    """
    Add admin to the application database

    :param username: name the admin will sign in with
    :param password: 'cleartext password (will be hashed)'
    """
    admin = Admin(username, password)
    db.session.add(admin)
    db.session.commit()


@app.shell_context_processor
def make_shell_context():
    return {'add_admin': add_admin, 'db': db}
