from django.contrib import admin
from .models import Message , UserChannel

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id' , 'from_who' , 'to_who' , 'message' , 'date' , 'time' , 'has_been_seen' ]

admin.site.register(Message , MessageAdmin)

class UserChannelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'channel_name' ]

admin.site.register(UserChannel , UserChannelAdmin)


