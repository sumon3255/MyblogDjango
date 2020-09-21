from django.contrib import admin
from .models import Post,Comment,Category,Profile

# Register your models here.
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Profile)

#add tinyMCE in Admin post
@admin.register(Post) #register krar sathe sathe admin o change krlam
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyinject.js',)
    list_display = ('title','slug','authur','category')
    # list_filter = ()
    search_fields = ('authur__username', 'title')
   
class ProfileAdmin(admin.ModelAdmin):
      list_display = ('user','dob','photo')