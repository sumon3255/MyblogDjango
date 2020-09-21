from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,get_object_or_404
from blog.models import Post,Comment,Category
from django.contrib import messages
from blog.templatetags import extras
from django.http import JsonResponse
from django.template.loader import render_to_string
from.forms import *
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.contrib.auth.decorators import login_required
# Create your views here.
def blogHome(request):
    Posts = Post.objects.all()
    paginator = Paginator(Posts, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    if page is None:
        start_index = 0
        end_index = 7
    else:
       (start_index , end_index) = proper_pagination(posts, index=4)
    
    page_range = list(paginator.page_range[start_index:end_index])
    context = {'posts':posts,
        'page_range':page_range}
    return render(request,'blog/blogHome.html',context)
  

def blogPost(request,slug):
   post = Post.objects.filter(slug=slug).first()  #filter by slug
   allposts = Post.objects.all()
   post.views = post.views + 1
   post.save()

   comments =Comment.objects.filter(post=post, reply=None).order_by('-id') 
   is_liked = False
   if post.likes.filter(id=request.user.id).exists():
            is_liked = True
   comment_form = CommentForm(request.POST or None)
   if request.method == "POST":
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs =None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            comment_form = CommentForm()
   
   context = {'post':post,   
        'allposts':allposts,
        'is_liked':is_liked,
        'total_likes':post.total_likes(),
        'comments':comments,
        'comment_form':comment_form,}
   if request.is_ajax():
        html = render_to_string('blog/comment_section.html', context, request=request)
        return JsonResponse({'form': html})
   return render(request,'blog/blogPost.html',context)


def likes_post(request):
    # post = get_object_or_404(Post , id=request.POST.get('post_id'))
    post = get_object_or_404(Post, sno=request.POST.get('post_sno'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():#exist thakle option dibe
        post.likes.remove(request.user)
        is_liked = False
    else:

      post.likes.add(request.user)#who like the post
      is_liked = True
    #   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {
        'post':post,
        'is_liked':is_liked,
        'total_likes':post.total_likes(),
    }

    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form2': html})

# def blogNav(request):
#     allPosts = Post.objects.all()
#     context3 = {'allPosts': allPosts}
#     return render(request,'blog/blogPost.html',context3)


# class CatListView(ListView):
#     template_name='category.html'
#     context_object_name='catlist'
#     # paginate_by = 3
#     def get_queryset(self):
      
              
#         content={

#           'cat': self.kwargs['category'],
#            'posts': Post.objects.filter(category__name=self.kwargs['category']),
           
           
#         }
#         return content
        
def CategoryView(request,cats):
    category_posts = Post.objects.filter(category__name=cats)
    paginator = Paginator(category_posts, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    if page is None:
        start_index = 0
        end_index = 7
    else:
       (start_index , end_index) = proper_pagination(posts, index=4)
    
    page_range = list(paginator.page_range[start_index:end_index])

    context ={
        'cats':cats,
        'posts':posts,
        'page_range':page_range
        
    }
    return render(request,'category.html',context)




def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        "category_list": category_list,
    }
    return context


def proper_pagination(posts, index):
    start_index = 0
    end_index = 7
    if posts.number > index:
        start_index = posts.number - index
        end_index = posts.number + end_index
    return (start_index, end_index)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(data= request.POST or None, instance= request.user)
        profile_form = ProfileEditForm(data= request.POST or None, instance= request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect("edit_profile")
    
    else:
        user_form = UserEditForm(instance= request.user)
        profile_form = ProfileEditForm(instance= request.user.profile)
    
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
    }

    return render(request, 'blog/edit_profile.html',context)
