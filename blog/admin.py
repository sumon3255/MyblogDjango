from django.contrib import admin
from .models import Post,BlogComment

# Register your models here.
admin.site.register(BlogComment)

#add tinyMCE in Admin post
@admin.register(Post) #register krar sathe sathe admin o change krlam
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyinject.js',)
