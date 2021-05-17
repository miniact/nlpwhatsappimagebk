from django.contrib import admin
from . import models 
# Register your models here.




admin.site.register(models.UserAds)



class ChatAdsTagsAdmin(admin.ModelAdmin):
    fields = ['chat_id','troom_id','NERval','TAGS']
    list_display = ('id','chat_id','troom_id','NERval','TAGS')
    list_filter = ('TAGS',)
    search_fields = ('TAGS',)
    ordering = ('chat_id',)

class ChatsAdmin(admin.ModelAdmin):
    
    list_display = ('id','message', 'chat_type','sent_by','media_url','timestp','nlp_processed')
    search_fields = ('message','sent_by')
    list_filter = ('chat_type', 'nlp_processed',)
    ordering = ('timestp',)

admin.site.register(models.ChatAdsTags, ChatAdsTagsAdmin)

admin.site.register(models.Chatroom)
admin.site.register(models.Chats,ChatsAdmin)