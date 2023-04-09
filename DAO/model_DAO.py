from DAO.model import User

class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def register(self, email, password, name):
        user = User(email=email, password=password, name=name, status="user")
        self.session.add(user)
        self.session.commit()

    def updater(self, email, data):
        user = self.get_email(email)
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        self.session.add(user)
        self.session.commit()
        return user

    def update_password(self, my_email, password):
        user = self.get_email(my_email)
        user.password = password
        self.session.add(user)
        self.session.commit()

    def update_status(self, email, status):
        user = self.get_email(email)
        user.status = status

    def delete(self, email):
        user = self.get_email(email)
        self.session.delete(user)
        self.session.commit()

