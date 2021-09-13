from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from . import models

# Register your models here.


@admin.register(models.Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title','slug', 'author','status')
    prepopulated_fields = {
        "slug" : ("title",),
    }

admin.site.register(models.Category)

admin.site.register(models.Comment, MPTTModelAdmin)