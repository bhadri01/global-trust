from flask import session,Blueprint, current_app, jsonify,request,render_template,redirect,url_for
from .lib.mailservice import MailSender
from werkzeug.security import generate_password_hash, check_password_hash
import random
from bson import ObjectId

# Create blueprint for authentication routes
auth_routes = Blueprint('admin', __name__, url_prefix='/admin')

#admin home page 
@auth_routes.route('/')
def adminHome():
    db = current_app.config['MONGO']
    if db.user.find_one({'userid':session.get("userid")}):
        return render_template("admin/home.html")
    else:
        return redirect(url_for('admin.admin'))
    
#admin events page 
@auth_routes.route('/event')
def adminEvent():
    db = current_app.config['MONGO']
    if db.user.find_one({'userid':session.get("userid")}):
        return render_template("admin/event.html")
    else:
        return redirect(url_for('admin.admin'))

#admin new events page 
@auth_routes.route('/event/new')
def adminNewEvent():
    db = current_app.config['MONGO']
    if db.user.find_one({'userid':session.get("userid")}):
        return render_template("admin/newevent.html")
    else:
        return redirect(url_for('admin.admin'))

#admin Volunteer page 
@auth_routes.route('/volunteer')
def adminVolunteer():
    db = current_app.config['MONGO']
    if db.user.find_one({'userid':session.get("userid")}):
        return render_template("admin/home.html")
    else:
        return redirect(url_for('admin.admin'))
    
#admin gallery page 
@auth_routes.route('/gallery')
def adminGallery():
    db = current_app.config['MONGO']
    if db.user.find_one({'userid':session.get("userid")}):
        return render_template("admin/home.html")
    else:
        return redirect(url_for('admin.admin'))

#admin banner page 
@auth_routes.route('/banner')
def adminBanner():
    db = current_app.config['MONGO']
    if db.user.find_one({'userid':session.get("userid")}):
        return render_template("admin/home.html")
    else:
        return redirect(url_for('admin.admin'))
    
#login page for the admin
@auth_routes.get('/login')
def admin():
    db = current_app.config['MONGO']
    # Implement signin logic here
    if db.user.find_one({'userid':session.get("userid")}):
        return redirect(url_for('admin.adminHome'))
    else:
        return render_template("admin/login.html",error={'status':False})

#login validation for the admin
@auth_routes.post('/login')
def adminLogin():
    form_data = request.form
    name,password = form_data.get("username"),form_data.get("password")
    
    if name and password:
        db = current_app.config['MONGO']
        if db.user.find_one({'name':name,"password":password}):
            session["userid"] = generate_password_hash(password)
            db.user.update_one({'name':name,"password":password},{'$set':{'userid':session['userid']}})
            return redirect(url_for('admin.adminHome'))
        else:
            return render_template("admin/login.html",error={'message':"Invalied login details",'status':True})
    else:
        return render_template("admin/login.html",error={'message':"login data required",'status':True})


#logout for the amdin
@auth_routes.route('/logout')
def logout():
    # Implement signout logic here
    db = current_app.config['MONGO']
    db.user.update_one({'userid':session.get("userid")},{'$set':{'userid':""}})
    session.clear()
    return redirect(url_for("admin.admin"))



# Create blueprint for main routes
main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return render_template("index.html")

@main_routes.route('/about')
def about():
    data = [
        {"name":"Sara grant","loc":"team1.jpg"},
        {"name":"Sara grant","loc":"team2.jpg"},
        {"name":"Sara grant","loc":"team3.jpg"},
        {"name":"Sara grant","loc":"team4.jpg"},
        {"name":"Sara grant","loc":"team5.jpg"},
        {"name":"Sara grant","loc":"team6.jpg"},
        {"name":"Sara grant","loc":"team7.jpg"},
        {"name":"Sara grant","loc":"team8.jpg"},
    ]
    return render_template("about.html",data=data)

@main_routes.route('/causes')
def causes():
    data = [
        {"title":"Sara grant","loc":"blog1.jpg"},
        {"title":"Sara grant","loc":"blog2.jpg"},
        {"title":"Sara grant","loc":"blog3.jpg"},
        {"title":"Sara grant","loc":"blog4.jpg"},
        {"title":"Sara grant","loc":"blog5.jpg"},
        {"title":"Sara grant","loc":"blog6.jpg"},
    ]
    return render_template("causes.html",data=data)

@main_routes.route('/services')
def services():
    data = [
        {"title":"Sara grant","loc":"si1.png"},
        {"title":"Sara grant","loc":"si2.png"},
        {"title":"Sara grant","loc":"si3.png"},
        {"title":"Sara grant","loc":"si4.png"},
        {"title":"Sara grant","loc":"si5.png"},
        {"title":"Sara grant","loc":"si6.png"},
        {"title":"Sara grant","loc":"si7.png"},
        {"title":"Sara grant","loc":"si10.png"},
        {"title":"Sara grant","loc":"si11.png"},
    ]
    return render_template("services.html",data=data)

@main_routes.route('/contact')
def contact():
    return render_template("contact.html")

@main_routes.route('/send_email')
def send_email(email,otp):
    # Access the Mail instance using the Flask app's context
    mail = current_app.config['MAIL']
    to = f"{email}"
    body = f"{otp}"
    message = "OTP Testing"

    MailSender(mail,to,body,message)
   

    return jsonify({"message":"Email sent"})
