#importing libraries
from flask import Flask, render_template, url_for, redirect, flash, has_request_context, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, SelectField, EmailField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, Email, NumberRange ,Regexp
from flask_bcrypt import Bcrypt
import logging
import datetime

################################################################

#logging configuration

#customize the logging format
class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            #include the request url
            record.url = request.url
            #include the request remote address
            record.remote_addr = request.remote_addr
        else:
            #return nothing for url and remote address
            record.url = None
            record.remote_addr = None
        return super().format(record)

#configuring logging format
logFormatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)

#setting up basic logging
logger = logging.getLogger()
#lazy setup for logging
# logFormatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%")

#adding console handlers to root logger
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

#adding console handlers to root logger
fileHandler = logging.FileHandler(".audit.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

################################################################

#create flask app
app = Flask(__name__)
#create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///namelist.db'
#create secret key
app.config['SECRET_KEY'] = 'password@123'
#use Bcrypt
bcrypt = Bcrypt(app)
#introduce sqlalchemy and link the app to the database
db = SQLAlchemy(app)

################################################################

#protect app from CSRF
csrf=CSRFProtect()
csrf.init_app(app)

################################################################

#use login manager from flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

#load user into the session
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

################################################################

#create model
#the employers model
class Employees(db.Model):
    #id are in integers
    id = db.Column(db.Integer, primary_key=True, unique=True)
    #name are strings
    name = db.Column(db.String(255))
    #gender are strings
    sex=db.Column(db.String(6))
    #NRIC are strings
    nric = db.Column(db.String(255))
    #Date of birth are date
    dob = db.Column(db.Date)
    #Age are integers
    age = db.Column(db.Integer)
    #phone number are strings
    phone_number = db.Column(db.Integer)
    #email are unique strings
    email = db.Column(db.String(255))
    #home address are strings
    home_address = db.Column(db.String(255))
    #years of experience are integers
    exp = db.Column(db.Integer)
    #Grade of security are integers
    grade = db.Column(db.Integer, default=1)
    #availability are boolean
    avail = db.Column(db.Boolean, default=True)

#the hr system model
class Users(db.Model, UserMixin):
    #set id as the primary key
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    #will be stored in hash form
    password = db.Column(db.String(80),nullable=False)
    #to check whether the user is an admin
    #default set to false
    is_admin = db.Column(db.Boolean, default=False)
    #to check whether the user is a root admin
    #default set to false
    is_root = db.Column(db.Boolean, default=False)

################################################################

#create a form for registering new users
class RegisterForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[InputRequired(), 
                                       Length(min=2,max=20),
                                       Regexp(regex=r'^[a-zA-Z0-9 !@#$%^&*()_+-=]+$',
                                              message='Username only accept a-z A-Z 0-9 and !@#$%^&*()_+-=')], 
                           render_kw={"placeholder":"username"})
    password = PasswordField(label="Password",
                             validators=[InputRequired(), 
                                         Length(min=8, max=20), 
                                         Regexp(regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+-=]).{8,}$',
                                                message='Password need to contain at least one lowercase character, one uppercase character, and one special chracter [!@#$%^&*()_+-=]')], 
                             render_kw={"placeholder":"password"})
    # password = PasswordField(label="Password",
    #                          validators=[InputRequired(), 
    #                                      Length(min=4, max=20), 
    #                                      Regexp(regex=r'^[a-zA-Z0-9 ,_\-+]+$',
    #                                             message='Password only accept a-z A-Z 0-9 and ._-+')], 
    #                          render_kw={"placeholder":"password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = Users.query.filter_by(username=username.data).first()
        if existing_user_username:
            flash("Username already in use")
            raise ValidationError("The username already exist. Please choose a different one")

#create a form for logging in users
class LoginForm(FlaskForm):
    username = StringField(label="Username",
                           validators=[InputRequired(), 
                                       Length(min=2,max=255),
                                       Regexp(regex=r'^[a-zA-Z0-9 ,_\-+]+$',
                                              message='Username only accept a-z A-Z 0-9 and _-+')], 
                           render_kw={"placeholder":"username"})
    password = PasswordField(label="Password",
                             validators=[InputRequired(), 
                                         Length(min=8, max=20), 
                                         Regexp(regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+-=]).{8,}$',
                                                message='Password need to contain at least one lowercase character, one uppercase character, and one special chracter [!@#$%^&*()_+-=]')], 
                             render_kw={"placeholder":"password"})
    submit = SubmitField("Login")

################################################################

#create a form to add new employees 
class AddEmployeeForm(FlaskForm):
    name = StringField("Name",validators=[InputRequired(), 
                                          Length(min=2,max=20), 
                                          Regexp(regex=r'^[a-zA-Z0-9 ._\-+]+$',
                                                 message="Name can only be alphanumeric")])
    sex = SelectField("Sex",choices=["Male", "Female"])
    nric = StringField("Nric",validators=[InputRequired(), 
                                          Length(min=2,max=20), 
                                          Regexp(regex=r'^[a-zA-Z0-9]+$',
                                                 message="NRIC can only be alphanumeric")])
    dob = DateField("Date of Birth",validators=[InputRequired()])
    age = IntegerField("Age",validators=[InputRequired(),NumberRange(min=1,max=99)])
    phone_number = IntegerField("Phone Number",validators=[InputRequired()])
    email = EmailField("Email",validators=[InputRequired(),Email()])
    home_address = StringField("Home Address", validators=[Regexp(regex=r'^[a-zA-Z0-9 .\,_\-+]+$')])
    exp = IntegerField("Experience", validators=[InputRequired(),NumberRange(min=0,max=99)])
    grade = IntegerField("Grade",validators=[InputRequired(),NumberRange(min=1,max=5)])
    submit = SubmitField("Add")

class UpdateEmployeeForm(FlaskForm):
    name = StringField("Name",validators=[InputRequired(), 
                                          Length(min=2,max=20), 
                                          Regexp(regex=r'^[a-zA-Z0-9 ._\-+]+$',
                                                 message="Name can only be alphanumeric")])
    sex = SelectField("Sex",choices=["Male", "Female"])
    nric = StringField("Nric",validators=[InputRequired(), 
                                          Length(min=2,max=20), 
                                          Regexp(regex=r'^[a-zA-Z0-9]+$',
                                                 message="NRIC can only be alphanumeric")])
    dob = DateField("Date of Birth",validators=[InputRequired()])
    age = IntegerField("Age",validators=[InputRequired(),NumberRange(min=1,max=99)])
    phone_number = IntegerField("Phone Number",validators=[InputRequired()])
    email = EmailField("Email",validators=[InputRequired(),Email()])
    home_address = StringField("Home Address", validators=[Regexp(regex=r'^[a-zA-Z0-9 .\,_\-+]+$')])
    exp = IntegerField("Experience", validators=[InputRequired(),NumberRange(min=0,max=99)])
    grade = IntegerField("Grade",validators=[InputRequired(),NumberRange(min=1,max=5)])
    avail = BooleanField("Avail")
    submit = SubmitField("Update")

class DeleteEmployeeForm(FlaskForm):
    submit = SubmitField("Delete")

################################################################

class UpdateUserForm(FlaskForm):
    username = StringField("Username",validators=[InputRequired(), 
                                                  Length(min=2,max=20), 
                                                  Regexp(regex=r'^[a-zA-Z0-9 ._\-+)]+$',
                                                         message="Username can only be alphanumeric")])
    is_admin = BooleanField("Is Admin")
    submit = SubmitField("Update")

class DeleteUserForm(FlaskForm):
    submit = SubmitField("Delete")

################################################################

#uncomment to initialize database
#remember to comment back when database is generated
app.app_context().push()
with app.app_context():
    db.create_all()

################################################################

#route for home
@app.route('/')
def home():
    if current_user.is_authenticated:
        flash("Please log out first")
        return redirect(url_for('login'))
    else:
        return render_template('index.html')

#route for login page
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    #if the user is not logged in
    if current_user.is_authenticated==False:
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    if user.is_admin:
                        login_user(user)
                        flash('Successfully logged in as admin')
                        return redirect(url_for('admin'))
                    else:
                        login_user(user)
                        flash('Successfully logged in')
                        return redirect(url_for('dashboard'))
            else:
                flash('login failed')
    #if the user is logged in
    elif current_user.is_authenticated:
        flash("Please log out first")
        if current_user.is_admin:
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('dashboard'))
                    
    return render_template('login.html', form=form)

#route for dashboard page
@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    username = current_user.username
    namelist=Employees.query.all()
    return render_template('dashboard.html', namelist=namelist, username=username)

#route for logout system
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

#route for registration page
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash("Please logout first!")
        return redirect(url_for('login'))
    else:
        form = RegisterForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = Users(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

################################################################

#route for admin page
@app.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    if current_user.is_admin:
        username = current_user.username
        namelist=Employees.query.all()
        root = current_user.is_root
        return render_template('admin.html', namelist=namelist, root=root)
    else:
        return redirect(url_for('warning'))

#route for updating users
@app.route('/update_employee/<int:id>', methods=['GET','POST'])
@login_required
def update_employee(id):
    if current_user.is_admin:
        employee_to_update = Employees.query.filter_by(id=id).first()
        form = UpdateEmployeeForm(obj=employee_to_update)
        if form.validate_on_submit():
            employee_to_update.name =  form.name.data
            employee_to_update.sex =  form.sex.data
            employee_to_update.nric =  form.nric.data
            employee_to_update.dob =  form.dob.data
            employee_to_update.age =  form.age.data
            employee_to_update.phone_number =  form.phone_number.data
            employee_to_update.email =  form.email.data
            employee_to_update.home_address =  form.home_address.data
            employee_to_update.exp =  form.exp.data
            employee_to_update.grade =  form.grade.data
            employee_to_update.avail = form.avail.data
            db.session.commit()
            flash("Update successful")
            return redirect(url_for('admin'))
        else:
            return render_template('update_employee.html',form=form,employee_to_update=employee_to_update)
    else:
        return redirect(url_for('warning'))

@app.route('/add_employee',methods=['GET','POST'])
@login_required
def add_employee():
    form = AddEmployeeForm()
    if current_user.is_admin:
        if form.validate_on_submit():
            new_employee = Employees(
                name=form.name.data,
                sex=form.sex.data,
                nric=form.nric.data,
                dob=form.dob.data,
                age=form.age.data,
                phone_number=form.phone_number.data,
                email = form.email.data,
                home_address=form.home_address.data,
                exp=form.exp.data,
                grade=form.grade.data)
            db.session.add(new_employee)
            db.session.commit()
            flash("Successfully added new employee")
            return redirect(url_for('admin'))
        else:
            return render_template('add_employee.html',form=form)
    else:
        return redirect(url_for('warning'))
    
@app.route('/delete_employee/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    if current_user.is_admin:
        employee_to_delete = Employees.query.filter_by(id=id).first()
        form = DeleteEmployeeForm()
        if form.validate_on_submit():
            db.session.delete(employee_to_delete) 
            db.session.commit()
            flash("Successfully deleted employee")
            return redirect(url_for('admin'))
        else:
            return render_template('delete_employee.html',form=form, employee_to_delete=employee_to_delete)
    else:
        return redirect(url_for('warning'))

#route for displaying warning
@app.route('/warning')
def warning():
    logging.warning('Someones tries to bypass system security')
    return render_template('warning.html')

################################################################

#route for root
@app.route('/root')
@login_required
def root():
    if current_user.is_root:
        userlist = Users.query.all()
        return render_template('root.html',userlist=userlist)
    else:
        return redirect(url_for('warning'))

@app.route('/update_user/<int:id>',methods=['GET','POST'])
@login_required
def update_user(id):
    if current_user.is_root:
        user= Users.query.filter_by(id=id).first()
        form = UpdateUserForm(obj=user)
        if form.validate_on_submit():
            user.username=form.username.data
            user.is_admin=form.is_admin.data
            flash("Successfully updated user")
            db.session.commit()
        return render_template('update_user.html',user=user,form=form)
    else:
        return redirect(url_for('warning'))
    return

@app.route('/delete_user/<int:id>',methods=['GET','POST'])
@login_required
def delete_user(id):
    if current_user.is_root:
        user = Users.query.filter_by(id=id).first()
        form = DeleteUserForm()
        if form.validate_on_submit():
            db.session.delete(user)
            db.session.commit()
            flash("Successfully deleted user")
            return redirect(url_for('root'))
        else:
            return render_template('delete_user.html',form=form,user=user)
    else:
        return redirect(url_for('warning'))

################################################################

#activating debugging mode and run the application
#debug mode is not recommended in actual production environment
if __name__ == '__main__':
    app.run(debug=True)

################################################################