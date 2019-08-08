from django.contrib import admin

# Register your models here.

from .models import Reader,Group,User,Pin,Tag,Action,Status,Condition,Trigger

admin.site.register(Reader)
admin.site.register(Group)
admin.site.register(User)
admin.site.register(Pin)
admin.site.register(Tag)
admin.site.register(Action)
admin.site.register(Status)
admin.site.register(Condition)
admin.site.register(Trigger)