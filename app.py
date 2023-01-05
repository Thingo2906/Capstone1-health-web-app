import os
import re
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests

from forms import UserRegisterForm, LoginForm, UserEditForm, PostForm, BMIForm, CaloriesRequirement, SearchFoodForm
from models import db, connect_db, User, UserBMI, Post
from config import API_KEY_1, API_KEY_2
CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
uri = os.environ.get('DATABASE_URL', 'postgresql:///footprint_db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
#app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('DATABASE_URL', 'postgresql:///healthy_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
app.config['SQLALCHEMY_ECHO'] =  True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'itisasecret')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)

db.create_all()

##############################################################################
# register
# login
# logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

def get_bmi(age, weight, height):
    """Calculate the BMI"""

    url = "https://fitness-calculator.p.rapidapi.com/bmi"
    
    querystring = {"age":f"{age}","weight":f"{weight}","height":f"{height}"}

    headers = {
	"X-RapidAPI-Key": API_KEY_1,
	"X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
    }

    r = requests.request("GET", url, headers=headers, params=querystring)

    result = r.json()
    bmi = result['data']['bmi']
    health_condition = result['data']['health']
    return {'bmi': bmi, 'health_condition': health_condition}

def get_calories(age, gender, height, weight, activitylevel):
    """Calculate the calories requirement"""
    url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"

    querystring = {"age": f"{age}","gender":f"{gender}","height":f"{height}","weight":f"{weight}","activitylevel":f"{activitylevel}"}

    headers = {
	"X-RapidAPI-Key": API_KEY_1,
	"X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
    }

    res = requests.request("GET", url, headers=headers, params=querystring)
    data = res.json()
    maintain_weight = data['data']['goals']['maintain weight']
    lose_weight = data['data']['goals']['Extreme weight loss']['calory']
    gain_weight = data['data']['goals']['Extreme weight gain']['calory']
    return {'maintain_weight' : maintain_weight, 
            'lose_weight' : lose_weight, 
            'gain_weight' : gain_weight}
"""def search_recipe(food):
    url = "https://edamam-recipe-search.p.rapidapi.com/search"

    querystring = {"q":f"{food}"}

    headers = {
	"X-RapidAPI-Key": "2f848b1f9bmsh46ce8aadc4e6ddep16a7b9jsnbec515e6a2a9",
	"X-RapidAPI-Host": "edamam-recipe-search.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    image = data['hits'][0]['recipe']['image']
    label = data['hits'][0]['recipe']['label']
    ingredients = data['hits'][0]['recipe']['ingredientLines']# a list
    health_labels = data['hits'][0]['recipe']['healthLabels']# a list
    source = data['hits'][0]['recipe']['url']
    recipe = {'image': image, 'label' : label, 
            'ingredients' : ingredients,
            'health_labels' : health_labels,
            'source' : source
            }
    image_1 = data['hits'][1]['recipe']['image']
    label_1 = data['hits'][1]['recipe']['label']
    ingredients_1 = data['hits'][1]['recipe']['ingredientLines']# a list
    health_labels_1 = data['hits'][1]['recipe']['healthLabels']# a list
    source_1 = data['hits'][1]['recipe']['url']
    recipe_2 = {'image': image_1, 'label' : label_1, 
            'ingredients' : ingredients_1,
            'health_labels' : health_labels_1,
            'source' : source_1
            }
    return[recipe, recipe_2]"""

def search_recipe(tag):
    API_URL ="https://api.spoonacular.com/recipes/random?"  

    url = f"{API_URL}number=1&tag={tag}"
    header = {"x-api-key" : API_KEY_2}
    response = requests.request("GET", url, headers=header)
    data = response.json()
    title = data['recipes'][0]['title']
    
    image = data['recipes'][0]['image']
   
    source = data['recipes'][0]['sourceUrl']
    type = data['recipes'][0]['dishTypes']
    ingredients = [x['original'] for x in data['recipes'][0]['extendedIngredients']]  
    instructions =[x['step'] for x in data['recipes'][0]['analyzedInstructions'][0]['steps']]
    return {'title' : title, 'image' : image,
            'source' : source, 'type' : type,
            'ingredients' : ingredients, 'instructions' : instructions}

  
@app.route('/')
def start_page():
    return render_template('initial.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserRegisterForm()
    if form.validate_on_submit():
        try: 
            new_user = User.signup(
                   username = form.username.data,
                   password = form.password.data,
                   email = form.email.data,
                   first_name = form. first_name.data,
                   last_name = form.last_name.data,
                   image_url = form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        do_login(new_user)
        return redirect("/choices")

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("choices")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    # IMPLEMENT THIS
    do_logout()
    flash(f"Goodbye")
    return redirect("/login")

###################################################

@app.route('/choices', methods=['GET'])
def present_choices():
    """Present choices of calculation types to user""" 
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    posts = Post.query.all()
    return render_template("home.html", posts = posts)



@app.route('/bmi', methods=['GET','POST'])
def check_bmi():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    form = BMIForm()
    if form.validate_on_submit():
        age = form.age.data
        weight = form.weight.data
        height = form.height.data
        bmi_results = get_bmi(age, weight, height)
        new_bmi = UserBMI(user_id=g.user.id, age=age, weight=weight, 
                          height=height, bmi=bmi_results['bmi'], 
                          health_condition=bmi_results['health_condition'])
        g.user.user_bmi.append(new_bmi)
        db.session.add(new_bmi)
        db.session.commit()
        
        user = User.query.get_or_404(g.user.id)
       
        return render_template('bmi_result.html', bmi_result=bmi_results, user=user)

    return render_template('bmi_form.html', form =form)  

@app.route('/bmi/<int:bmi_id>/delete', methods=["POST"])
def bmi_destroy(bmi_id):
    """Delete a post."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    bmi = UserBMI.query.get_or_404(bmi_id)
    if bmi.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(bmi)
    db.session.commit()

    return redirect(f"/user/{g.user.id}")



@app.route('/calories', methods=['GET','POST'])
def check_calories():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    form = CaloriesRequirement()
    if form.validate_on_submit():
        age = form.age.data 
        gender = form.gender.data
        height = form.height.data
        weight = form.weight.data
        activitylevel = form.activitylevel.data
        calory_result= get_calories(age, gender, height, weight, activitylevel)
        
        user = User.query.get_or_404(g.user.id)
        
        return render_template('calories_result.html', calory_result=calory_result, user=user)
    return render_template('calories_form.html', form=form)

@app.route('/search-recipe', methods=['GET','POST'])
def search():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    form = SearchFoodForm()
    if form.validate_on_submit():
        tag = form.tag.data
        recipe = search_recipe(tag)
        return render_template('recipe.html', recipe=recipe)
    return render_template('search_food.html', form=form)

#######################################
#User Profile
@app.route('/user/<int:user_id>', methods=['GET'])
def show_user_profile(user_id):
    """show user profile with their Bmi result"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    user_bmi = (UserBMI.query.filter(UserBMI.user_id ==user_id).order_by(UserBMI.result_date.desc()).limit(2).all())

    posts = (Post
                .query
                .filter(Post.user_id == user_id)
                .order_by(Post.timestamp.desc())
                .limit(10)
                .all())
   
    return render_template('profile.html', user_bmi = user_bmi, user=user, posts= posts)

@app.route('/users/update', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/images/default-pic.png"   
            db.session.commit()
            return redirect(f"/user/{user.id}")

        flash("Wrong password, please try again.", 'danger')

    return render_template('user_edit.html', form=form, user_id=user.id)

@app.route('/users/delete', methods = ['POST'])
def delete_user():
    """Delete user"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    do_logout()
   
    db.session.delete(g.user)
    db.session.commit()
    do_logout()

    return redirect("/login")

###########################################################
## 
@app.route('/posts/new', methods=["GET", "POST"])
def add_post():
    """Adding a post"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
   
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        image_url = form.image_url.data
        new_post = Post(title= title, content =content,image_url= image_url, user_id = g.user.id)
        g.user.posts.append(new_post)
        db.session.add(new_post)
        db.session.commit()
       
        return redirect(f"/user/{g.user.id}")
    return render_template('post_form.html', form =form)

@app.route('/posts/<int:post_id>', methods =['GET'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:post_id>/update', methods = ['GET', 'POST'])
def update_feedback(post_id):
    """Update post"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    post = Post.query.get_or_404(post_id)
    
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        return redirect(f"/user/{post.user_id}")

    return render_template("post_edit.html", form=form, post=post)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def post_destroy(post_id):
    """Delete a post."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    post = Post.query.get_or_404(post_id)
    if post.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/user/{g.user.id}")

#################################################################

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req