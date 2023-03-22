from app import app
from app.models import user, band
from flask import render_template, redirect, request, session

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    bands = band.Band.get_all()
    for item in bands:
        item.membership = band.Band.get_membership({'id':item.id})
    return render_template("dashboard.html", 
                           user=user.User.get_one({'id':session['user_id']})[0], 
                           bands=bands)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    # see if the login information provided valid
    if not user.User.validate_login(request.form):
        return redirect('/')
    user_in_db = user.User.get_one(request.form, condition='email')
    session['user_id'] = user_in_db[0].id
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/register', methods=['POST'])
def register():
    if user.User.validate_registration(request.form):
        # Call the save @classmethod on User
        user.User.save(request.form)
    return redirect('/')

@app.route('/mybands')
def profile():
    return render_template('profile.html',
                           user=user.User.get_band({'id': session['user_id']}),
                           membership=user.User.get_membership({'id': session['user_id']}))


@app.route('/membership/join/<int:id>')
def join(id):
    user.User.join_band({'user_id':session['user_id'], 'band_id':id})
    return redirect('/dashboard')


@app.route('/membership/quit/<int:id>')
def leave(id):
    user.User.quit_band({'user_id': session['user_id'], 'band_id': id})
    return redirect('/dashboard')


@app.route('/quit/<int:id>')
def leave2(id):
    user.User.quit_band({'user_id': session['user_id'], 'band_id': id})
    return redirect('/mybands')
