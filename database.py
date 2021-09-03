from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mariokart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def add_new_user():
        username = input("Enter username: ")
        email = input("Enter email: ")
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_all_users():
        rows = db.session.execute(text("SELECT * FROM User"))
        for row in rows:
            print(row)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    image = db.Column(db.String(), nullable=False, unique=True)
    prep_time_min = db.Column(db.Integer())
    cook_time_min = db.Column(db.Integer())
    total_time_min = db.Column(db.Integer())
    servings = db.Column(db.Integer())
    ingredients = db.Column(db.String())
    instructions = db.Column(db.String())
    nutrition = db.Column(db.String())

    def __repr__(self):
        return '<Recipe %r>' % self.name

    @staticmethod
    def add_new_recipe(name, image, prep_time_min, cook_time_min, total_time_min, servings,
                       ingredients, instructions, nutrition):

        new_recipe = Recipe(
            name=name,
            image=image,
            prep_time_min=prep_time_min,
            cook_time_min=cook_time_min,
            total_time_min=total_time_min,
            servings=servings,
            ingredients=ingredients,
            instructions=instructions,
            nutrition=nutrition
        )

        db.session.add(new_recipe)
        db.session.commit()

    @staticmethod
    def get_all_recipes():
        rows = db.session.execute(text("SELECT * FROM Recipe"))
        for row in rows:
            print(row)


if __name__ == '__main__':
    Recipe.get_all_recipes()
