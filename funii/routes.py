from funii import app,db
from funii.models import User,Post,Comment,Wishlist,Chat,PostSchema
from flask import jsonify , request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user , current_user ,logout_user
import pickle
import sklearn
from flask_cors import CORS
import numpy as np
post_schema=PostSchema()
posts_schema=PostSchema(many=True)
# @app.route('/')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
@app.post("/signup")
def register():
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']
    phone_number=request.json['phone_number']
    if User.query.get(email) or User.query.get(username):
        return jsonify("error")
    with app.app_context():
        db.create_all()
        new_user=User(username=username,email=email,phone_number=phone_number,
                       password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return jsonify("Successfully logined")
@app.route('/signin')
def signin():
    email=request.json['email']
    password=request.json['password']
    loging_user=User.query.filter_by(email=email,password=password).first()
    if  loging_user:
        login_user(loging_user)
        info="user logedin successfully"
        return jsonify(info)
    else:
        info="user doesn't exist"
        return jsonify(info)
@app.route('/logout')
def logout():
    logout_user()
    return jsonify("logout successfully")
@app.post('/delete_user/<id>')
def delete_users(id):
    deleted_user=User.query.get(id)
    if deleted_user:
        db.session.delete(deleted_user)
        db.session.commit()
        return jsonify("user deleted successfully")
    return jsonify("error")
@app.post('/create_post')
def create_p():
    loaded_model=pickle.load(open("trained_model.sav","rb"))
    mark = request.json['mark']
    id = request.json['id']
    pic = request.json['pic']
    category = request.json['category']
    etat = request.json['etat']
    descreption = request.json['descreption']
    fuel = request.json['fuel']
    trensmission = request.json['trensmission']
    owner = request.json['owner']
    max_power = request.json['max_power']
    prix = request.json['prix']
    km_driven =  request.json['km_driven']
    year = request.json['year']
    engine = request.json['engine']
    input_data = (year,prix,km_driven,1.0,1.0,0.0,1248.0,74.00,20.0) #just an example to ensure that it's work 
    input_as_np = np.asarray(input_data)
    reshaped_data = input_as_np.reshape(1,-1)
    prediction=loaded_model.predict(reshaped_data)
    print(prediction)
    if prediction-500<prix or prediction+500>prix:
        post = Post(id = id,mark = mark, prix=prix, km_driven=km_driven , year = year, engine=engine , pic = pic , category =category , etat =etat , descreption = descreption , fuel = fuel , trensmission =trensmission, owner=owner , max_power=max_power)
        db.session.add(post)
        db.session.commit()
        if Post.query.filter_by(id=id).first():
            return jsonify("post succefully created")
        else:
            return jsonify("error ceck the price")
@app.post('/delete_post/<id>')
def delete_pos(id):
    deleted_post=Post.query.get(id)
    if deleted_post:
        db.session.delete(deleted_post)
        db.session.commit()
        return jsonify("post deleted successfully")
    return jsonify("error")
@app.route('/get_posts',methods=['GET'])
def getposts():
    pos=Post.query.all()
    posts=posts_schema.dump(pos)
    return jsonify(posts)
@app.route('/get_post/<id>',methods=['GET'])
def getpost(id):
    post_obj=Post.query.get(id)
    if post_obj:
        post_getting=posts_schema.dump(post_obj)
        return jsonify(post_getting)
    else:
        return jsonify("error")
@app.route('/get_comments/<id>',methods=['GET'])
def getpcomment(id):
    com=Comment.query.filter_by(post=id)
    comments=post_schema.dump(com)
    if comments:
        return jsonify(comments)
    return jsonify("error")
