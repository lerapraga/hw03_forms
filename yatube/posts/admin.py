from django.contrib import admin

from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    # можно вынести эту строку в константу в settings.py
    # - при доработке я это учту


admin.site.register(Post, PostAdmin)
admin.site.register(Group)

# @admin.register использую в дальнейшем спасибо :)
