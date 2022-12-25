from funii import db ,ma
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer() , primary_key=True)
    username = db.Column(db.String(length=255), nullable=False )
    email = db.Column(db.String(length=255), nullable=False , unique=True) 
    password = db.Column(db.String(length = 255) , unique = True)
    phone_number=db.Column(db.String(length=11))
    is_active=db.Column(db.String(length=11))
class Post(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    pic=db.Column(db.String(length=200)) #pic field : url 
    category=db.Column(db.String(length=100))
    mark=db.Column(db.String(length=100))
    prix=db.Column(db.Integer())
    etat=db.Column(db.String(length=100)) # choice field
    descreption=db.Column(db.String(length=2000))
    year=db.Column(db.Integer())
    km_driven=db.Column(db.Float())
    fuel= db.Column(db.String(length=2000)) #choices
    trensmission= db.Column(db.String(length=2000)) #choices
    owner=db.Column('user_id',db.Integer(),db.ForeignKey('user.id'))
    engine=db.Column(db.Float())
    max_power=db.Column(db.Float())
class PostSchema(ma.Schema):
    class Meta:
        fileds=('id','pic','name','prix','category','mark','etat','description','year','km_driven',
                'fuel','trensmission','owner','engine','max_power')
class Comment(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    rating=db.Column(db.Integer()) 
    text=db.Column(db.Text())
    user=db.Column('User_id',db.Integer(),db.ForeignKey('user.id'))
    post=db.Column('Post_id',db.Integer(),db.ForeignKey('post.id'))
class Wishlist(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    user_id=db.Column(db.Integer(),db.ForeignKey('user.id'))
    username=db.Column(db.String(length=50))
    post_id=db.Column(db.Integer(),db.ForeignKey('post.id'),)
class Chat(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    sender=db.Column(db.Integer(),db.ForeignKey('user.id'))
    receiver=db.Column(db.Integer(),db.ForeignKey('user.id'))
    text=db.Column(db.Text())
    date=db.Column(db.DateTime,default=datetime.utcnow)

