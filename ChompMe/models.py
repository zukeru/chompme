from django.db import models

class UserProfile(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=100)
    first_name = models.CharField(max_length=20)
    username = models.CharField(max_length=100)
    last_name = models.CharField(max_length=20)
    user_score = models.BigIntegerField()
    about = models.TextField()
    dob = models.CharField(max_length=11)
    occupation = models.CharField(max_length=40)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return ' '.join([
            self.first_name,
            self.last_name,
        ])    

class ProfilePic(models.Model):
    id = models.AutoField(primary_key = True)   
    user_id = models.BigIntegerField()
    profile_pic = models.CharField(max_length=500)

class Friends(models.Model):
    id = models.AutoField(primary_key = True)
    friend_id = models.BigIntegerField()    
    user_id = models.BigIntegerField()

class FriendToken(models.Model):
    id = models.AutoField(primary_key = True)
    user_id = models.BigIntegerField()
    token = models.CharField(max_length=200)

class FriendRequest(models.Model):
    id = models.AutoField(primary_key = True)
    user_id = models.BigIntegerField()
    friend_id = models.BigIntegerField()
    accepted = models.CharField(max_length=3)
    token = models.CharField(max_length=200)

class GlobalImages(models.Model):
    id = models.AutoField(primary_key = True)
    user_id = models.BigIntegerField()
    score = models.BigIntegerField()
    hash_tags= models.CharField(max_length=4000)
    global_pic = models.CharField(max_length=500)

class UserImages(models.Model):
    id = models.AutoField(primary_key = True)
    user_id = models.BigIntegerField()
    album = models.BigIntegerField()
    user_pic = models.CharField(max_length=500)

class UserAlbum(models.Model):
    id = models.AutoField(primary_key = True)
    user_id = models.BigIntegerField()
    album_name = models.CharField(max_length=500)    
    
class Post(models.Model):
    id = models.AutoField(primary_key = True)
    user_id = models.BigIntegerField()
    title = models.CharField(max_length=100)
    body = models.TextField()
    pub_date = models.DateTimeField('date published')
    
class PostLikes(models.Model):
    id = models.AutoField(primary_key = True)
    friend_id = models.BigIntegerField()    
    post_id = models.BigIntegerField() 
    
class DisLikes(models.Model):
    id = models.AutoField(primary_key = True)
    friend_id = models.BigIntegerField()    
    post_id = models.BigIntegerField()    
    
class PostComment(models.Model):
    id = models.AutoField(primary_key = True)
    friend_id = models.BigIntegerField()    
    post_id = models.BigIntegerField()  
    comment = models.CharField(max_length=1000)  
    
class ImageLikes(models.Model):
    id = models.AutoField(primary_key = True)
    friend_id = models.BigIntegerField()    
    post_id = models.BigIntegerField() 
    
class ImageComment(models.Model):
    id = models.AutoField(primary_key = True)
    friend_id = models.BigIntegerField()    
    post_id = models.BigIntegerField()  
    comment = models.CharField(max_length=1000)      

# Create your models here.
"""
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=4000)
    password = models.CharField(max_length=4000)
    email = models.CharField(max_length=4000)
    phone = models.CharField(max_length=4000)
    profile_image = models.FileField()
    about  = models.CharField(max_length=4000)
    hometown  = models.CharField(max_length=4000)
    mood = models.CharField(max_length=4000)
    job  = models.CharField(max_length=4000)
    score  = models.CharField(max_length=4000)
    hobbies  = models.CharField(max_length=4000)
    datetime  = models.DateField()
    class Meta:
        managed=True

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    friendid = models.ForeignKey(User)
    msg  = models.CharField(max_length=4000)
    subject = models.CharField(max_length=4000)
    datetime  = models.DateField()
    class Meta:
        managed=True

class MsgQueue(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    friend = models.CharField(max_length=4000)
    msg  = models.CharField(max_length=4000)
    type  = models.CharField(max_length=4000)
    dest  = models.CharField(max_length=4000)
    datetime  = models.DateField()
    class Meta:
        managed=True

class UserCode(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    code  = models.CharField(max_length=4000)
    datetime  = models.DateField()
    class Meta:
        managed=True

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    image = models.FileField()
    imgdesc  = models.CharField(max_length=4000)
    datetime  = models.DateField()
    class Meta:
        managed=True
           
class Album(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    name  = models.CharField(max_length=4000)
    imageid = models.ForeignKey(Image)
    datetime  = models.DateField()
    class Meta:
        managed=True

class ImageComment(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    imageid = models.ForeignKey(Image)
    comment = models.CharField(max_length=4000)
    datetime = models.DateField()
    class Meta:
        managed=True

class ImageLike(models.Model):
    id = models.AutoField(primary_key=True)
    imageid = models.ForeignKey(Image)
    userid = models.ForeignKey(User)
    datetime = models.DateField()
    class Meta:
        managed=True

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    message = models.CharField(max_length=4000)
    image = models.FileField()
    embed_link  = models.CharField(max_length=4000)
    liked_count  = models.CharField(max_length=4000)
    datetime = models.DateField()
    class Meta:
        managed=True

class PostComment(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    postid = models.ForeignKey(Post)
    comment = models.CharField(max_length=4000)
    datetime = models.DateField()
    class Meta:
        managed=True

class PostLike(models.Model):
    id = models.AutoField(primary_key=True)
    postid = models.ForeignKey(Post)
    userid = models.ForeignKey(User)
    datetime = models.DateField()
    class Meta:
        managed=True

class UserFriend(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    friendid = models.ForeignKey(User)
    datetime = models.DateField()
    class Meta:
        managed=True


class UserEnviroment(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    elementid = models.ForeignKey(User)
    datetime = models.DateField()
    class Meta:
        managed=True

class EnvElement(models.Model):
    id = models.AutoField(primary_key=True)
    elementname = models.CharField(max_length=4000)
    elementfile = models.FileField()
    elementcost =  models.CharField(max_length=4000)
    elementmaturetime = models.CharField(max_length=4000)
    elementposition = models.CharField(max_length=4000)
    animatedtype = models.CharField(max_length=4000)
    datetime = models.DateField()
    class Meta:
        managed=True
"""