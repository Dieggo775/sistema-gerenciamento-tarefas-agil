from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Project, Task
from forms import TaskForm, ProjectForm, UserForm
from github import Github
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
# @login_required
def index():
    tasks = Task.query.all()
    projects = Project.query.all()
    return render_template('index.html', tasks=tasks, projects=projects)

@app.route('/kanban')
# @login_required
def kanban():
    # Fetch from GitHub Projects
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPO')  # e.g., 'username/repo'
    if token and repo_name:
        g = Github(token)
        repo = g.get_repo(repo_name)
        projects = list(repo.get_projects())
        if projects:
            project = projects[0]  # Use first project
            columns = project.get_columns()
            tasks = []
            for col in columns:
                cards = col.get_cards()
                for card in cards:
                    content = card.get_content()
                    if content and hasattr(content, 'title'):
                        tasks.append({
                            'title': content.title,
                            'description': content.body or '',
                            'status': col.name
                        })
        else:
            tasks = []
    else:
        tasks = Task.query.all()  # Fallback to local
    return render_template('kanban.html', tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/task/new', methods=['GET', 'POST'])
# @login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            priority=form.priority.data,
            project_id=form.project.data,
            user_id=form.assignee.data if form.assignee.data != 0 else None
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!')
        return redirect(url_for('index'))
    return render_template('task_form.html', form=form, title='New Task')

@app.route('/project/new', methods=['GET', 'POST'])
# @login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.description.data)
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!')
        return redirect(url_for('index'))
    return render_template('project_form.html', form=form, title='New Project')

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
# @login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data
        task.priority = form.priority.data
        task.project_id = form.project.data
        task.user_id = form.assignee.data if form.assignee.data != 0 else None
        db.session.commit()
        flash('Task updated successfully!')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.status.data = task.status
        form.priority.data = task.priority
        form.project.data = task.project_id
        form.assignee.data = task.user_id or 0
    return render_template('task_form.html', form=form, title='Edit Task')

@app.route('/user/new', methods=['GET', 'POST'])
# @login_required
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!')
        return redirect(url_for('index'))
    return render_template('user_form.html', form=form, title='New User')

if __name__ == '__main__':
    app.run(port=8000, debug=True)