from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from blog.models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from blog.models import Post
from django.http import JsonResponse
from django.core.mail import send_mail,send_mass_mail


# Create your views here.

#HTML
def home(request):
    allPosts = Post.objects.all().order_by('-views')[:2]
    context = {'allPosts':allPosts}
    return render(request,'home/home.html',context)

def about(request):
     return render(request,'home/about.html')

def contact(request):
     if request.method == 'POST':
         name = request.POST['name']
         email = request.POST['email']
         phone = request.POST['phone']
         content = request.POST['content']
       
         if len(name)<3 or len(email)<5 or len(phone)<3 or len(content)<4:
             messages.error(request, 'Please fill the form correctly')
        
         else:
              contact = Contact(name=name, email=email, phone=phone, content=content)
              contact.save()
              send_mail(
             'Subject - mdsSumon Coding Inbox',
            'Hello I Am' + name + ',\n' +  content,
            'My Email Is' + email,
            ['faahimtf1@gmail.com'],
          
            )
              messages.success(request, 'Your Message has been sent')
           
  

     return render(request,'home/contact.html')



def search(request):
    # allPosts = Post.objects.all()
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none() #for blank list query
    else:
       allPostsTitle = Post.objects.filter(title__icontains = query)
       allPostsContent = Post.objects.filter(content__icontains = query)
       allPosts = allPostsTitle.union(allPostsContent) #union can merge 2 query 
    if allPosts.count() == 0:
          messages.warning(request, 'No Search results Found Please Write Perfectly')

    params = {'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)
    # return HttpResponse("This is search")


#Authentication Part
def handleSignup(request):
    if request.method == "POST":
        #GEt The Post Parameters  
        username = request.POST['username']
        fname= request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1= request.POST['pass1']
        pass2= request.POST['pass2']

        #Check For error input
        if len(username) >10 :
             messages.error(request, 'User Name must Be less than 10 lhars')
             return redirect("home")
        if not username.isalnum():
             messages.error(request, 'User Name must Contain letters and error')
             return redirect("home")
        if pass1 != pass2 :
             messages.error(request, "Password didn't match")
             return redirect("home")
        if len(pass1) < 6: 
             messages.error(request, "Password length should be at least 6")
             return redirect("home")
                    
        if not any(char.isupper()  for char in pass1): 
             messages.error(request, "Password should have at least one Upper  letter")
             return redirect("home")
           
        


 

        #Create The User
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        Profile.objects.create(user=myuser)
        messages.success(request, 'Your account has been successfully created')
        return redirect("home")

    else:
        return HttpResponse("Error 404 - Not Found")



def handleLogin(request):
    if request.method == "POST":
        #GEt The Post Parameters  
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        #check krno
        user = authenticate(username=loginusername,password=loginpass)
        #check krno
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Your havesuccessfully loggedin')
            return redirect("home")
        else:
             messages.error(request, "Invlaid Credentials,Please try Again")
             return redirect("home")
    return HttpResponse("Error 404 - Not Found")


def handleLogout(request):
        logout(request)
        messages.success(request, 'Successfully loggeOut')
        return redirect("home")
        return HttpResponse("Logout")