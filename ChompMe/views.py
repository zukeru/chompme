#views.py
from ChompMe.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from ChompMe.models import UserProfile, FriendToken, Friends, Post, ProfilePic,FriendRequest,PostComment, PostLikes, DisLikes
from django.http import JsonResponse
from datetime import *
import base64
import simplejson
from __builtin__ import file, str
import os 
from gdata.youtube import FirstName

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required  
@csrf_protect       
def upload_profilepic(request):
    if request.method == 'POST':
        f = request.FILES.get('file')
        username = request.user
        
        filename = str(f).lower()
        try:
            ext = filename.split('.')[1]
            
            if ext != 'jpg' and  ext != 'jpeg' and  ext !='gif' and  ext !='png':
                ext = filename.split('.')[2]
        except:
            pass
        print filename, ext
        
        if ext:                                
            time_stamp = str(datetime.now()).replace('-','').replace(' ','').replace(':','').split('.')[0]
            current_directory = os.path.dirname(os.path.abspath(__file__))
            directory = current_directory + "/static/images/user_images/%s/" % username
            file_name = base64.urlsafe_b64encode(time_stamp + str(username))
            
            file_name = file_name + '.' + ext
            
            user_data = UserProfile.objects.get(username=str(request.user))   
            
            user_id = user_data.id
            
            pic_location = "user_images/%s/%s" % (username, file_name)
            
            pic_location = pic_location.replace(' ', '')
            
                  
            profile_pic_update = ProfilePic.objects.filter(user_id=user_id)
            if profile_pic_update:
                profile_pic_update = profile_pic_update[0]
                profile_pic_update.profile_pic=pic_location
                profile_pic_update.save()
            else:
                profile_pic_update = ProfilePic(user_id=user_id,profile_pic=pic_location)
                profile_pic_update.save()
            
            print pic_location
            
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except:
                    pass
                path = directory + file_name  
            else:     
                path = directory +  file_name 
                 
            destination = open(path, 'wb')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            context = {'user': request.user,
                       'file_message':'Your profile picture has been updated.',
                        }
                
            return render_to_response('profile_pic.html',context ,  RequestContext(request)) 
        else:
                context = {'user': request.user,}
                return render_to_response('profile_pic.html',context ,  RequestContext(request))

    context = {'user': request.user,} 
    
    return render_to_response('profile_pic.html',context ,  RequestContext(request))

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            save_userdata = UserProfile(username = form.cleaned_data['username'] , 
                                        title=form.cleaned_data['profile_title'], 
                                        first_name = form.cleaned_data['first_name'], 
                                        last_name = form.cleaned_data['last_name'],
                                        about = form.cleaned_data['about'],
                                        user_score = 0,
                                        dob = form.cleaned_data['dob'],
                                        occupation = form.cleaned_data['occupation'],
                                        pub_date = datetime.now())
            save_userdata.save()

            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'register.html',
    variables,
    )
 
def register_success(request):
    return render_to_response(
    'success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
@csrf_protect
def deletePost(request):
    post_data = request.POST.copy()
    context = {}   
    posts=[]
    if request.POST.has_key('id'):
            id = post_data['id']
            user_data = UserProfile.objects.get(username=str(request.user))   
            user_id = user_data.id
            instance = Post.objects.get(id=id, user_id=user_id)
            instance.delete()
            context.update({'message': 'Your post has been deleted'})
            return HttpResponse(simplejson.dumps(context), content_type='application/json')  
    else:
        context.update({'message': 'Your post has been deleted'})
        return HttpResponse(simplejson.dumps(context), content_type='application/json')   



@login_required
@csrf_protect
def searchFriends(request):
    def remove_duplicates(values):
        output = []
        seen = set()
        for value in values:
            # If value has not been encountered yet,
            # ... add it to both list and set.
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output
    def getuser(user_data):
        try:
            for user in user_data:
                profile_pic_search = ProfilePic.objects.get(user_id=user.id)
                profile_pic_search = profile_pic_search.profile_pic
                users.append((user.id, user.username, user.first_name, user.last_name, profile_pic_search, user.user_score))
            return users
        except Exception as e:
            print e
            
    post_data = request.POST.copy()
    context = {}   
    users=[]
    if request.POST.has_key('searchstring'):
            string_search = post_data['searchstring']
            if ' ' in string_search:
                string_search = string_search.split(' ')
                firstname = string_search[0]
                lastname = string_search[1]
                          
            else:
                username = string_search 

            try:  
                user_data = UserProfile.objects.filter(username__icontains=username)  
                print getuser(user_data)
            except Exception as e:
                print e
   
            try: 
                user_data = UserProfile.objects.filter(first_name__icontains=username)  
                print getuser(user_data)
            except Exception as e:
                print e
                    
            try:
                user_data = UserProfile.objects.filter(last_name__icontains=username)  
                getuser(user_data)
            except Exception as e:
                print e
                
            try:
                user_data = UserProfile.objects.filter(first_name__icontains=firstname,last_name__icontains=lastname)  
                getuser(user_data)
            except Exception as e:
                print e
            
            users = remove_duplicates(users)   
            
            context.update({'message': 'Hello', 'users':users})
            return HttpResponse(simplejson.dumps(context), content_type='application/json')                



@login_required
@csrf_protect
def update_profile_pic(request):
    user_data = UserProfile.objects.get(username=str(request.user))   
    user_id = user_data.id
    context={}
    try:
        profile_pic_db = ProfilePic.objects.get(user_id=user_id)
        profile_pic = profile_pic_db.profile_pic
    except Exception as e:
        profile_pic = None   
    context.update({'profile_pic': profile_pic})    
    return HttpResponse(simplejson.dumps(context), content_type='application/json')

@login_required
@csrf_protect
def get_posts(request):
    profile_name = request.POST.copy()
    profile_name  = str(profile_name['profile_name']).split('/')
    username = str(request.user)
    context = {}
    posts = []
    comments = []
    html_output = ''
    if 'home' not in profile_name[3]: 
        try:
            user_data = UserProfile.objects.get(username=str(profile_name[3]))   
            user_id = user_data.id
            username = request.user
            user_posts =  Post.objects.filter(user_id = user_id).order_by('-pub_date').values()
            
            for post in user_posts:
                
                comments = getComments(post['id'])
                for comment in comments:
                    #(3, 1L, u'Comment\n', u'user_images/Gandalf/MjAxNTAyMTEyMjMyMzVHYW5kYWxm.jpg', u'Gandalf', 6)
                    html_output = html_output + "<br><span class='glyphicon glyphicon-fire' aria-hidden='true' style='color:#9bba9c;'></span><i><font size='4'> <a href='/" + comment[4] + "'>" + comment[4] +"</a></font>" + ": " + comment[2] + "</i><br>"  
                
                
                dislikes = getDisLikes(post['id'])            
                likes = getLikes(post['id'])      
                print html_output, likes, dislikes    
                posts.append((str(profile_name[3]), post['title'], post['body'], post['id'], str(post['pub_date']), html_output, likes, dislikes))

            context.update({'message': '', 'user_posts':posts })    
            return HttpResponse(simplejson.dumps(context), content_type='application/json') 
    
        except:
            context.update({'message': 'No post for this user'})    
            return HttpResponse(simplejson.dumps(context), content_type='application/json')   
    else:
       
        try:
            user_data = UserProfile.objects.get(username=str(request.user))   
            user_id = user_data.id
            username = request.user
            user_posts =  Post.objects.filter(user_id = user_id).order_by('-pub_date').values()
            
            for post in user_posts:
                comments = getComments(post['id'])
                for comment in comments:
                    #(3, 1L, u'Comment\n', u'user_images/Gandalf/MjAxNTAyMTEyMjMyMzVHYW5kYWxm.jpg', u'Gandalf', 6)
                    html_output = html_output + "<br><span class='glyphicon glyphicon-fire' aria-hidden='true' style='color:#9bba9c;'></span><i><font size='4'> <a href='/" + comment[4] + "'>" + comment[4] +"</a></font>" + ": " + comment[2] + "</i><br>"  
                
                dislikes = getDisLikes(post['id'])      
                likes = getLikes(post['id'])      
                posts.append((str(username), post['title'], post['body'], post['id'], str(post['pub_date']), html_output, likes, dislikes)) 

            context.update({'message': '', 'user_posts':posts })    
            return HttpResponse(simplejson.dumps(context), content_type='application/json') 
    
        except Exception as e:
            print e
            context.update({'message': 'No post for this user'})    
            return HttpResponse(simplejson.dumps(context), content_type='application/json')


def getDisLikes(post_id):
    context = {}   
    posts=[]
    likes = 0
    try:
        comments = DisLikes.objects.filter(post_id=post_id)
        for com in comments:
            likes += 1
    except Exception as e:
        likes = 0
        print e
    
    return likes

def getLikes(post_id):
    context = {}   
    posts=[]
    likes = 0
    try:
        comments = PostLikes.objects.filter(post_id=post_id)
        for com in comments:
            likes += 1
    except Exception as e:
        likes = 0
        print e
    
    return likes

def getComments(post_id):
    context = {}   
    posts=[]
    comments_list = []
    try:
        comments = PostComment.objects.filter(post_id=post_id)
        for com in comments:
            get_friend_data = UserProfile.objects.get(id=com.friend_id)
            find_pic_id = get_friend_data.id
            friend_username = get_friend_data.username
            ppic = ProfilePic.objects.get(user_id=find_pic_id)
            pic = ppic.profile_pic
            comments_list.append((com.id,com.friend_id,com.comment,pic,friend_username, post_id))
        return comments_list   
    except Exception as e:
        print e

@login_required
@csrf_protect
def addLike(request):
    post_data = request.POST.copy()
    context = {}   
    posts=[]
    context.update({'message':'not added'})
    if request.POST.has_key('id'):
        user_data = UserProfile.objects.get(username=str(request.user))   
        user_id = user_data.id
        post_id = post_data['id']
        
        try:
            user_liked = DisLikes.objects.get(friend_id = user_id)
            user_liked.delete()
        except:
            pass
        
        try:
            user_liked = PostLikes.objects.get(friend_id = user_id, post_id = post_id)
        except:
            save_like= PostLikes(friend_id = user_id, post_id=post_id)
            save_like.save() 
        context.update({'message':'added liked'})
               
    return HttpResponse(simplejson.dumps(context), content_type='application/json') 


@login_required
@csrf_protect
def removeLike(request):
    post_data = request.POST.copy()
    context = {}   
    posts=[]
    if request.POST.has_key('id'):
        user_data = UserProfile.objects.get(username=str(request.user))   
        user_id = user_data.id
        post_id = post_data['id']
 
        try:
            user_liked = PostLikes.objects.get(friend_id = user_id, post_id = post_id)
            user_liked.delete()
        except:
            pass
        
        try:
            user_liked = DisLikes.objects.get(friend_id = user_id, post_id = post_id)
        except:
            save_like= DisLikes(friend_id = user_id, post_id=post_id)
            save_like.save() 
    
    context.update({'message':'removed liked'})
    return HttpResponse(simplejson.dumps(context), content_type='application/json')  

@login_required
@csrf_protect
def makepost(request):
    post_data = request.POST.copy()
    context = {}   
    posts=[]
    if request.POST.has_key('post_text'):
            post_title = post_data['post_title']
            post_text = post_data['post_text']
            username = post_data['username']
            user_data = UserProfile.objects.get(username=str(request.user))   
            user_id = user_data.id
            post_time = datetime.now() 
            save_post= Post(user_id = user_id, title = post_title, body = post_text, pub_date = post_time)
            save_post.save()
            user_posts =  Post.objects.filter(user_id = user_id).order_by('-pub_date').values()
            for post in user_posts:
                posts.append((username, post['title'], post['body'], post['id']))
            context.update({'message': 'Your post has been posted', 'user_posts':posts })
            return HttpResponse(simplejson.dumps(context), content_type='application/json')  
    else:
        context.update({'token':'Your message failed to post'})
        return HttpResponse(simplejson.dumps(context), content_type='application/json')   


@login_required
@csrf_protect
def getNot(request):
    post_data = request.POST.copy()
    context = {}   
    user_data = UserProfile.objects.get(username=str(request.user))   
    friend_id = Friends.objects.filter(user_id = user_data.id) 
    friend_data = []
    context = {}   
    for id in friend_id:
        profile_pic_db_friend = ProfilePic.objects.get(user_id=id.friend_id)
        profile_pic_friend = profile_pic_db_friend.profile_pic
        friend_info = UserProfile.objects.get(id = id.friend_id)
        user_posts =  Post.objects.filter(user_id = id.friend_id).order_by('-pub_date').values()  
        for post in user_posts:
            friend_data.append((profile_pic_friend,friend_info.username, post['title'], post['body'], post['id']))
    context.update({'notifications':friend_data})
    return HttpResponse(simplejson.dumps(context), content_type='application/json')   



@login_required
@csrf_protect
def getToken(request):
    post_data = request.POST.copy()
    context = {}   
    
    profile_name = post_data['username']

    viewing_profile_data = UserProfile.objects.get(username=str(profile_name))
    user_data = UserProfile.objects.get(username=str(request.user))   
    
    if viewing_profile_data.id == user_data.id: 
   
        if request.POST.has_key('create_token'):
            datetimes = datetime.now()
            enc_token = base64.urlsafe_b64encode(str(request.user) + str(datetimes))     
            save_token= FriendToken(user_id = user_data.id, token = enc_token )
            save_token.save()
            context.update({'token': enc_token})
            return HttpResponse(simplejson.dumps(context), content_type='application/json')  
    else:
        context.update({'token':'You can only generate tokens for your self'})
        return HttpResponse(simplejson.dumps(context), content_type='application/json')   

@login_required
@csrf_protect
def getFriends(request):   
    profile_name = request.POST.copy()
    profile_name  = str(profile_name['profile_name']).split('/')
    username = str(request.user)
    context = {}
    posts = []

    if 'home' not in profile_name[3]:    
        user_data = UserProfile.objects.get(username=str(profile_name[3])) 
        friend_id = Friends.objects.filter(user_id = user_data.id) 
        friend_data = []
        context = {}   
        for id in friend_id:
            profile_pic_db_friend = ProfilePic.objects.get(user_id=id.friend_id)
            profile_pic_friend = profile_pic_db_friend.profile_pic
            friend_info = UserProfile.objects.get(id = id.friend_id)
            friend_data.append((profile_pic_friend,friend_info.username))
            
        context.update({'friend_data': friend_data})
        return HttpResponse(simplejson.dumps(context), content_type='application/json')        
    else: 
        user_data = UserProfile.objects.get(username=str(username)) 
        friend_id = Friends.objects.filter(user_id = user_data.id) 
        friend_data = []
        context = {}   
        for id in friend_id:
            profile_pic_db_friend = ProfilePic.objects.get(user_id=id.friend_id)
            profile_pic_friend = profile_pic_db_friend.profile_pic
            friend_info = UserProfile.objects.get(id = id.friend_id)
            friend_data.append((profile_pic_friend,friend_info.username))
            
        context.update({'friend_data': friend_data})
        return HttpResponse(simplejson.dumps(context), content_type='application/json')

@login_required
@csrf_protect
def friendRequest(request):
    post_data = request.POST.copy()
    username = request.user
    context = {}
    friend_data = []
    user_data = UserProfile.objects.get(username=str(username)) 
    user_id = user_data.id
    id = post_data['username']
    user_name = str(user_data.username)
    
    request_exists = FriendRequest.objects.filter(user_id=id, friend_id=user_id)
    
    if request_exists:
        context.update({'message':'Already Sent.',})
        return HttpResponse(simplejson.dumps(context), content_type='application/json') 
    else:
        save_friend= FriendRequest(user_id=id, friend_id=user_id)  
        save_friend.save()
        context.update({'message':'Request Sent'})
        return HttpResponse(simplejson.dumps(context), content_type='application/json')  

@login_required
@csrf_protect
def ar(request):
    post_data = request.POST.copy()
    username = request.user
    context = {}
    friend_id = post_data['id']
    
    user_data = UserProfile.objects.get(username=str(username)) 
    user_id = user_data.id
    friend_request = []
    
    request_exists = FriendRequest.objects.get(user_id=user_id, friend_id=friend_id)
    request_exists.delete()
    
    friends = Friends(user_id = user_id, friend_id=friend_id)
    friends.save()
    
    friends2 = Friends(user_id = friend_id, friend_id=user_id)
    friends2.save()
        
    context.update({'requests':'You are now friends..',})
    return HttpResponse(simplejson.dumps(context), content_type='application/json')


@login_required
@csrf_protect
def friendCount(request):
    post_data = request.POST.copy()
    username = request.user
    context = {}
    friend_id = post_data['profile_name']
    fusername = friend_id.split('/')[3]
    count = 0
    if fusername == 'home':
        user_data = UserProfile.objects.get(username=str(username)) 
        user_id = user_data.id
        friends = Friends.objects.filter(user_id=user_id)
        count = friends.count()
    
        context.update({'count':count,})
        return HttpResponse(simplejson.dumps(context), content_type='application/json')
    else:
        friend_data = UserProfile.objects.get(username=str(fusername)) 
        context.update({'count':count,})
        return HttpResponse(simplejson.dumps(context), content_type='application/json')
  
@login_required
@csrf_protect
def commentPost(request):

    post_data = request.POST.copy()
    username = request.user
    user_data = UserProfile.objects.get(username=str(username))
    user_id = user_data.id
    
    context = {}
    
    comment = post_data['comment']
    post_id = post_data['id']

    profile_name = post_data['profile_name']
    profile_url = profile_name.split('/')[3]

    comment_data = PostComment(post_id = post_id, friend_id=user_id,comment=comment)
    comment_data.save()

    context.update({'message':'Comment Saved!',})
    return HttpResponse(simplejson.dumps(context), content_type='application/json')

@login_required
@csrf_protect
def editProfile(request):

    post_data = request.POST.copy()
    username = request.user
    context = {}
    user_data = UserProfile.objects.get(username=str(username)) 
    user_id = user_data.id
    title = post_data['title']
    first_name = post_data['first_name']
    last_name = post_data['last_name']
    about = post_data['about']
    dob = post_data['dob']
    occupation = post_data['occupation'] 

    user_data.title = title
    user_data.first_name = first_name
    user_data.last_name = last_name
    user_data.about = about
    user_data.dob = dob
    user_data.occupation = occupation
    user_data.save()
    
    context.update({'message':'Saved!',})
    return HttpResponse(simplejson.dumps(context), content_type='application/json')


@login_required
@csrf_protect
def requestCount(request):
    post_data = request.POST.copy()
    username = request.user
    context = {}
    friend_id = post_data['profile_name']
    fusername = friend_id.split('/')[3]

    if fusername == 'home':
        user_data = UserProfile.objects.get(username=str(username)) 
        user_id = user_data.id
        friends = FriendRequest.objects.filter(user_id=user_id)
        count = friends.count()
    
        context.update({'count':count,})
        return HttpResponse(simplejson.dumps(context), content_type='application/json')
    else:
        context.update({'count':'',})
        return HttpResponse(simplejson.dumps(context), content_type='application/json')


 
@login_required
@csrf_protect
def getRequest(request):
    post_data = request.POST.copy()
    username = request.user
    context = {}
    
    user_data = UserProfile.objects.get(username=str(username)) 
    user_id = user_data.id
    friend_request = []
    
    request_exists = FriendRequest.objects.filter(user_id=user_id)
    for request in request_exists:
        user_data = UserProfile.objects.get(id=str(request.friend_id))
        profile_pic = ProfilePic.objects.get(user_id=user_data.id)
        profile_pic = profile_pic.profile_pic
        friend_request.append((user_data.id, user_data.username,profile_pic ))
        
    context.update({'requests':friend_request,})
    return HttpResponse(simplejson.dumps(context), content_type='application/json') 

        
@login_required
@csrf_protect
def addFriend(request):
    post_data = request.POST.copy()
    username = request.user
    context = {}
    friend_data = []
              
    if request.POST.has_key('add_friend'):
        datetimes = datetime.now()
        passed_token = post_data['add_friend']
        
        user_data = UserProfile.objects.get(username=str(request.user))
        try:
            token_exists = FriendToken.objects.get(token=str(passed_token))
            token_friend_id = token_exists.user_id
            token_id = token_exists.id
        except:
            context.update({'message':'Token does not exist.'})
            return HttpResponse(simplejson.dumps(context), content_type='application/json') 
        
        if token_exists:
            if user_data.id == token_exists.id:
                context.update({'message':'You can not add yourself.'})
                return HttpResponse(simplejson.dumps(context), content_type='application/json')   
            else:    
                     
                try:
                    friend_exists = Friends.objects.get(friend_id=token_friend_id, user_id=user_data.id)
                except Exception as e:
                    friend_exists = None
                
                if not friend_exists:        
                    save_friends= Friends(user_id = user_data.id, friend_id = token_friend_id)
                    save_friends.save()
                    
                    save_friends= Friends(user_id = token_friend_id, friend_id = user_data.id)
                    save_friends.save()
                    
                    FriendToken.objects.filter(id = token_id).delete()
                               
                    context.update({'message':'You have succesfully added your friend'})
                    return HttpResponse(simplejson.dumps(context), content_type='application/json')     
                else: 
                    context.update({'message':'You are already friends with that person.'})  
                    return HttpResponse(simplejson.dumps(context), content_type='application/json')   
        else:
            context.update({'message':'No token matching that requests.'})
            return HttpResponse(simplejson.dumps(context), content_type='application/json')     
     
@login_required
@csrf_protect
def home(request):
    friend_data = []
    post_data = request.POST.copy()
    username = request.user
    user_data = UserProfile.objects.filter(username=str(request.user))
    user_id = UserProfile.objects.get(username=str(request.user))
    friend_id = Friends.objects.filter(user_id = user_id.id)
    try:
        profile_pic_db = ProfilePic.objects.get(user_id=user_id.id)
        profile_pic = profile_pic_db.profile_pic
    except Exception as e:
        profile_pic = None   

    is_user_profile = 'Yes'

    context = {'user': request.user,
                   'user_data':user_data,
                   'is_user_profile':is_user_profile,
                   'profile_pic':profile_pic,
                }
        
    return render_to_response('home.html',context ,  RequestContext(request))

     
@login_required
def friends(request):
    friend_data = []
    
    try:
        is_friend = 'no'    
        profile_name = request.get_full_path()
        profile_name = profile_name.replace('/','')
        user_data = UserProfile.objects.filter(username=str(profile_name))
        user_info = UserProfile.objects.get(username=str(profile_name))
        user_id = user_info.id
        view_data = UserProfile.objects.get(username=str(request.user))
        view_id = view_data.id
    
    except Exception as e:
        print e

    request_sent = 'no'
        
    try:
        request_sent = FriendRequest.objects.get(user_id=user_id, friend_id=view_id)
        if request_sent.user_id == view_id:
            request_sent = 'yes'
    except Exception as e:
        print e
        pass
    
    try:
        friends = Friends.objects.get(user_id=user_id, friend_id=view_id)
        try:
            profile_pic_db = ProfilePic.objects.get(user_id=user_id)
            profile_pic = profile_pic_db.profile_pic
        except Exception as e:
            print e
            profile_pic = None  
        
        is_friend = 'True'
         
        if profile_name == str(request.user):
            return HttpResponseRedirect("/home")
        else:
            context = {'user_data':user_data,
                       'profile_pic':profile_pic,
                       'friend_data':friend_data,
                       'is_friend':is_friend,
                       'request_sent':request_sent,
                   }
        #user_data = UserProfile.objects.filter(username=str(request.user))
        return render_to_response('friend.html',context,  RequestContext(request))    
            
    except:
    
        try:
            profile_pic_db = ProfilePic.objects.get(user_id=user_id)
            profile_pic = profile_pic_db.profile_pic
        except Exception as e:
            profile_pic = None  
         
        if profile_name == str(request.user):
            return HttpResponseRedirect("/home")
        else:
            context = {'user_data':user_data,
                       'profile_pic':profile_pic,
                       'friend_data':friend_data,
                       'request_sent':request_sent,
                   }
        #user_data = UserProfile.objects.filter(username=str(request.user))
        return render_to_response('friend.html',context,  RequestContext(request))    