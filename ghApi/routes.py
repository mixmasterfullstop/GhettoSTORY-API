from flask import Flask,request,make_response,jsonify,send_from_directory,abort,url_for
from ghApi import app,db
from flask_bcrypt import Bcrypt 
from ghApi.models import User,Post

import secrets
from PIL import Image
import os
#import jwt


bcrypt = Bcrypt()

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    data = request.get_json()
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    user = User(username=data['username'],email=data['email'],password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'user has been saved'})

@app.route('/delete_user/',methods=['DELETE'])
def delete_user():
    data = request.get_json()
    user = User.query.filter_by().first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'user has been deleted'})

@app.route('/users', methods=['GET','POST'])
def users():
    output = []
    users = User.query.all()
    for user in users:
        user_data = {}
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['password'] = user.password
        output.append(user_data)
    
    return jsonify({'users': output})

def save_picture():
      random_hex = secrets.token_hex(8)
      fname, f_ext = os.splitext()
      picture_fn = random_hex + f_ext
      picture_path = os.path.join(app.root_path, 'static/posts', picture_fn)
      



@app.route('/post', methods=['POST'])
def post():
    data = request.get_json()
    if request.method == "POST":
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        post = Post(title=data['title'],content=data['content'],user_id=user.id)
        db.session.add(post)
        db.session.commit()
        if request.files:
            image = request.files["image"]
            image.save(url_for('static', image.filename))
            user.image_file = image.filename


            #image = url_for('static',filename='posts/'+ )
      
    return jsonify({"message": "posted"})

@app.route('/delete_post')
def delete_post():
    data = request.get_json()
    post = Post.query.filter_by(date_posted = data['date_posted'])
    db.session.delete(post)
    db.session.commit()
    return jsonify({'post': 'deleted'})

@app.route('/posts')
def posts():
    posts = Post.query.all()
    output = []
    for post in posts:
        post_data = {}
        post_data['title'] = post.title
        post_data['content'] = post.content
        output.append(post_data)
    
    return jsonify({'posts': output})



