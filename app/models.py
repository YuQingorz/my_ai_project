from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(200))
    registration_date = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class AITool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    thumbnail = db.Column(db.String(200))
    resource_url = db.Column(db.String(200))
    submission_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    submitter = db.relationship('User', backref='submitted_ai_tools')

    def __repr__(self):
        return '<AITool {}>'.format(self.name)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ai_tool_id = db.Column(db.Integer, db.ForeignKey('ai_tool.id'), nullable=False)

    commenter = db.relationship('User', backref='comments')
    ai_tool = db.relationship('AITool', backref='comments')

    def __repr__(self):
        return '<Comment {}>'.format(self.id)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ai_tool_id = db.Column(db.Integer, db.ForeignKey('ai_tool.id'))
    favorite_date = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref='favorites')
    ai_tool = db.relationship('AITool', backref='favorited_by')

    def __repr__(self):
        return '<Favorite {}>'.format(self.id)

class WorkspaceProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    creation_date = db.Column(db.DateTime, nullable=False)
    last_modified = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref='workspace_projects')

    def __repr__(self):
        return '<WorkspaceProject {}>'.format(self.name)

class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref='forum_posts')

    def __repr__(self):
        return '<ForumPost {}>'.format(self.title)

class PostReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.id'))

    replier = db.relationship('User', backref='post_replies')
    forum_post = db.relationship('ForumPost', backref='replies')

    def __repr__(self):
        return '<PostReply {}>'.format(self.id)
