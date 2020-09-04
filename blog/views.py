from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request,'blog/blogHome.html',context)

def blogPost(request,slug):
   post = Post.objects.filter(slug=slug).first()  #filter by slug
   post.views = post.views + 1
   post.save()
  


   comments = BlogComment.objects.filter(post=post,parents=None )#Post Corresponding comment nia asbe
   replies = BlogComment.objects.filter(post=post).exclude(parents=None) #Post Corresponding reply nia asbe expect none reply (not equal to)
   repDict = {}
   for reply in replies:
       if reply.parents.sno not in  repDict.keys():
           repDict[reply.parents.sno] = [reply]
       else:
           repDict[reply.parents.sno].append(reply)
   
   context = {'post':post,'comments':comments,'user': request.user,'repDict':repDict}
   return render(request,'blog/blogPost.html',context)

def postComment(request):
     if request.method == "POST":
            
            comment = request.POST.get("comment")
            user =  request.user
            postSno =  request.POST.get("postSno")
            post = Post.objects.get(sno=postSno)       
            parentSno= request.POST.get("ParentSno")
            if parentSno == "":      
                  comment = BlogComment(comment=comment, user=user, post=post)
                  comment.save()
                  messages.success(request, 'Your Comment has been posted Successfully')

                  #for reply logic
            else:
                parent = BlogComment.objects.get(sno=parentSno)                
                comment = BlogComment(comment=comment, user=user, post=post, parents=parent)
                comment.save()
                messages.success(request, 'Your Reply has been posted Successfully')
          
            
            
     return redirect(f"/blog/{post.slug}")


# def blogNav(request):
#     allPosts = Post.objects.all()
#     context3 = {'allPosts': allPosts}
#     return render(request,'blog/blogPost.html',context3)
