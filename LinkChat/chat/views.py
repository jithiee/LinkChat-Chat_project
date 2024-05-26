from django.shortcuts import render , redirect
from django.views import View
from channels.layers import get_channel_layer
from  asgiref.sync import async_to_sync
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Message , UserChannel

# Creating my class based  views here.

class Main( View):
    def get(self , request):
        
        print(dir(request.user))
        username  = request.user.username
        
        
        
        if request.user.is_authenticated:
                return redirect('home')
            
        return render(request=request , template_name="chat/main.html" , )
        
    
    
class Login(View):
    def get(self , request):
        print('lllllllllll')
        print(dir(request.user))
        return render(request=request , template_name="chat/login.html")
    
    def post(self , request ):
        
        context = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request=request , username = username , password= password )
        print(user)
        
        if  user != None:
            login(request=request , user=user)
            return redirect('home')
        
        context.update({'error' : 'Invalid credentials ! Try again   '})
        return render(request=request , template_name="chat/login.html" , context=context )
        
            
class Register(View):
    def get(self , request):
        return render(request=request , template_name="chat/register.html")
    
    def post( self ,  request ):
       
        context = {}
        data  = request.POST.dict()
        # first_name = request.POST.get('first_name') we cna also use like this 
        first_name =data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        
        try:    
            user = User.objects.create_user(
                first_name = first_name , 
                last_name = last_name ,
                username = username ,
                email = email ,
                password =password
            ) 
            
            user.save()
        
        
            user = authenticate(request=request , username=username , password=password)
                
            if user != None:
                # login(request=request , user=user)
                # return redirect('home')
                return redirect('login')
            
        except Exception as e :
            context.update({'error':'the tha data is wrong '+ str(e)})
            return render(request=request , template_name="chat/register.html" , context=context )
        
        return render(request=request, template_name="chat/register.html", context=context)
        

       
    
class Logout(View):
    def get(self , request):
        logout(request=request)
        return redirect('/')
    
    
class Home( View):
    def get(self , request):
        
        users = User.objects.exclude(id = request.user.id)
       
        if request.user.is_authenticated:
            context  = {
                'user':request.user ,
                 'users':users
            }
          
            return render(request=request , template_name="chat/home.html" , context=context )
        
        return redirect('/')
    
        
    
    
class Chat_Person(View):
    def get(self , request , id):
             
        person = User.objects.get(id = id)
       
        me = request.user
        
        messages= Message.objects.filter(Q(from_who = me , to_who = person) | Q(to_who=me , from_who = person  ) ).order_by('date' , 'time')
        
        try :
             user_channel_name   = UserChannel.objects.get(user = person)
        except :
            context = {
                'error': 'This user is cloaked in privacy.'
            }
            
            return render(request=request , template_name="chat/home.html" , context=context )
               
        data = {
                "type" : "receiver_function",
                "type_of_data" :"the_message_have_been_seen_from_the_other",
                       
                }
        
        channel_layer = get_channel_layer()
        
        async_to_sync(channel_layer.send)( user_channel_name.channel_name , data )
        
        
        messagea_have_ot_been_seen = Message.objects.filter(from_who = person , to_who = me)
        messagea_have_ot_been_seen.update(has_been_seen = True)
                    
        
        
        
        
        context = {
            'person':person,
            'me': me,
            'messages':messages
        }
        
        if request.user.is_authenticated:
              return render(request=request , template_name="chat/chat_person.html" , context=context )
        return redirect('/')
            





            
            
            
            
            
            
            
            
            
            
            
            
        
        # try:
        
        #    # print(User , 'ppppp')
        #     new_user = User()
        #     new_user.first_name = first_name
        #     new_user.last_name = last_name
        #     new_user.username = username
        #     new_user.email = email
        #     new_user.set_password(password)
        #     new_user.save()
        # except :
        #     pass
        
        # user = authenticate(request=request , username=username , password=password)
        
        # if user == None:
        #     print("this means tha data is wrong ")
        #     condext.update({"erorr": "the data is wrong "})
        # else:
        #     print("eveything is fine , right data ")
        #     login(request=request , user=user)
        #     redirect('login')
            
         
        # return render(request=request , template_name="chat/register.html" , context=condext )
        
    
    