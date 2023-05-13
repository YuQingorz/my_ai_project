from flask import render_template, request, redirect, url_for, flash, session, g
from app import app, db
from app.models import User, AITool, Comment, Favorite, WorkspaceProject, ForumPost, PostReply
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class SubmitAIToolForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired()])
    description = TextAreaField('描述', validators=[DataRequired()])
    url = StringField('网址', validators=[DataRequired()])

class CreateWorkspaceProjectForm(FlaskForm):
    name = StringField('项目名称', validators=[DataRequired()])
    description = TextAreaField('项目描述', validators=[DataRequired()])

class CreateForumPostForm(FlaskForm):
    title = StringField('帖子标题', validators=[DataRequired()])
    content = TextAreaField('帖子内容', validators=[DataRequired()])

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# 首页
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # 检查用户名和邮箱是否已被使用
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('用户名或邮箱已存在，请更换后重试。')
        else:
            # 创建新用户并添加到数据库
            new_user = User(username=username, email=email)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            flash('注册成功！请登录。')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 检查用户名和密码是否匹配
        user = User.query.filter_by(username=username).first()

        if user is not None and user.check_password(password):
            # 设置session并重定向到首页
            session['user_id'] = user.id
            flash('登录成功！')
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误，请重试。')

    return render_template('login.html')

# 登出
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('已成功登出。')
    return redirect(url_for('index'))

# AI工具列表页
@app.route('/ai_tools')
def ai_tools():
    tools = AITool.query.all()
    return render_template('ai_tools.html', tools=tools)

# AI工具详情页
@app.route('/ai_tools/<int:tool_id>')
def ai_tool_detail(tool_id):
    tool = AITool.query.get_or_404(tool_id)
    comments = Comment.query.filter(Comment.ai_tool_id == tool_id).all()
    return render_template('ai_tool_detail.html', tool=tool, comments=comments)

# 提交新AI工具
@app.route('/submit_ai_tool', methods=['GET', 'POST'])
def submit_ai_tool():
    form = SubmitAIToolForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        url = form.url.data

        ai_tool = AITool(name=name, description=description, url=url)
        db.session.add(ai_tool)
        db.session.commit()

        flash('AI工具已成功提交！')
        return redirect(url_for('ai_tools'))

    return render_template('submit_ai_tool.html', form=form)

# 评论AI工具
@app.route('/ai_tools/<int:tool_id>/comment', methods=['POST'])
def comment_ai_tool(tool_id):
    if g.user is None:
        flash('请先登录。')
        return redirect(url_for('login'))

    content = request.form['content']

    if not content:
        flash('评论内容不能为空。')
    else:
        comment = Comment(content=content, user_id=g.user.id, ai_tool_id=tool_id)
        db.session.add(comment)
        db.session.commit()
        flash('评论已发布。')

    return redirect(url_for('ai_tool_detail', tool_id=tool_id))

# 收藏AI工具
@app.route('/ai_tools/<int:tool_id>/favorite', methods=['POST'])
def favorite_ai_tool(tool_id):
    if g.user is None:
        flash('请先登录。')
        return redirect(url_for('login'))

    existing_favorite = Favorite.query.filter(Favorite.user_id == g.user.id, Favorite.ai_tool_id == tool_id).first()

    if existing_favorite:
        flash('您已收藏过此AI工具。')
    else:
        favorite = Favorite(user_id=g.user.id, ai_tool_id=tool_id)
        db.session.add(favorite)
        db.session.commit()
        flash('AI工具已收藏。')

    return redirect(url_for('ai_tool_detail', tool_id=tool_id))

# 取消收藏AI工具
@app.route('/ai_tools/<int:tool_id>/unfavorite', methods=['POST'])
def unfavorite_ai_tool(tool_id):
    if g.user is None:
        flash('请先登录。')
        return redirect(url_for('login'))

    favorite = Favorite.query.filter(Favorite.user_id == g.user.id, Favorite.ai_tool_id == tool_id).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash('已取消收藏此AI工具。')
    else:
        flash('您未收藏此AI工具。')

    return redirect(url_for('ai_tool_detail', tool_id=tool_id))

# 个人中心
@app.route('/profile')
def profile():
    if g.user is None:
        flash('请先登录。')
        return redirect(url_for('login'))

    favorites = Favorite.query.filter(Favorite.user_id == g.user.id).all()
    projects = WorkspaceProject.query.filter(WorkspaceProject.creator_id == g.user.id).all()
    
    return render_template('profile.html', user=g.user, favorites=favorites, projects=projects)

# 项目列表页
@app.route('/workspace_projects')
def workspace_projects():
    projects = WorkspaceProject.query.all()
    return render_template('workspace_projects.html', projects=projects)

# 创建新项目
@app.route('/create_workspace_project', methods=['GET', 'POST'])
def create_workspace_project():
    if g.user is None:
        flash('请先登录。')
        return redirect(url_for('login'))

    form = CreateWorkspaceProjectForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        project = WorkspaceProject(name=name, description=description, creator_id=g.user.id)
        db.session.add(project)
        db.session.commit()

        flash('项目已成功创建！')
        return redirect(url_for('workspace_projects'))

    return render_template('create_workspace_project.html', form=form)

# 论坛帖子列表页
@app.route('/forum_posts')
def forum_posts():
    posts = ForumPost.query.all()
    return render_template('forum_posts.html', posts=posts)

# 论坛帖子详情页
@app.route('/forum_posts/<int:post_id>')
def forum_post_detail(post_id):
    post = ForumPost.query.get_or_404(post_id)
    replies = PostReply.query.filter(PostReply.post_id == post_id).all()
    return render_template('forum_post_detail.html', post=post, replies=replies)

# 发布新帖子
@app.route('/create_forum_post', methods=['GET', 'POST'])
def create_forum_post():
    if g.user is None:
        flash('请先登录。')
        return redirect(url_for('login'))

    form = CreateForumPostForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        post = ForumPost(title=title, content=content, user_id=g.user.id)
        db.session.add(post)
        db.session.commit()

        flash('帖子已成功发布！')
        return redirect(url_for('forum_posts'))

    return render_template('create_forum_post.html', form=form)

# 回复帖子
@app.route('/forum_posts/<int:post_id>/reply', methods=['POST'])
def reply_forum_post(post_id):
    if g.user is None:
        flash('请先登录。')
        return redirect(url_for('login'))

    content = request.form['content']

    if not content:
        flash('回复内容不能为空。')
    else:
        reply = PostReply(content=content, user_id=g.user.id, post_id=post_id)
        db.session.add(reply)
        db.session.commit()
        flash('回复已发布。')

    return redirect(url_for('forum_post_detail', post_id=post_id))
