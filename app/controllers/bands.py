from sys import implementation
from app import app
from app.models import band, user
from flask import render_template, redirect, request, session

@app.route('/new/sighting')
def newBand():
    return render_template('new_band.html', user=user.User.get_one({'id': session['user_id']})[0])

@app.route('/addBand', methods=['POST'])
def addBand():
    if not band.Band.is_valid(request.form):
        return redirect('/new/sighting')
    band.Band.save({**request.form, 'user_id': session['user_id']})
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def editBand(id):
    return render_template('edit_band.html', user=user.User.get_one({'id': session['user_id']})[0], band=band.Band.get_one({'id': id})[0])

@app.route('/modify/<int:id>', methods=['POST'])
def modBand(id):
    if not band.Band.is_valid(request.form):
        return redirect(f'/edit/{id}')
    band.Band.update({**request.form,'id':id})
    return redirect('/dashboard')


@app.route('/mybands/delete/<int:id>')
def remove_band(id):
    band.Band.remove({'id':id})
    return redirect('/mybands')


@app.route('/dashboard/delete/<int:id>')
def remove_band2(id):
    band.Band.remove({'id': id})
    return redirect('/dashboard')
