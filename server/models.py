from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(256), unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name.")
        
        existing_author = Author.query.filter(Author.name == name).first()
        if existing_author:
            raise ValueError("Author with this name already exists.")
        
        return name
        
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) == 10:
            return number
        else:
            raise ValueError()

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title.")
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters.")
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary cannot be longer than 250 characters.")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['fiction', 'non-fiction']:
            raise ValueError("Category must be either 'fiction' or 'non-fiction'.")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
