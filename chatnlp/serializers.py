from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Chats, Chatroom, ChatAdsTags, UserAds 


class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields =('id','user1','user2','timestp','room_name','room_avatar')



    

class ChatAdsTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatAdsTags
        fields =('id','chat_id','cleaned_chat','NERval','TAGS')

class UserAdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAds
        fields =('id','user_id', 'tags')


class ChatsSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField('_get_sender_name')
    tags = serializers.SerializerMethodField('_get_tags_chat')
    def _get_sender_name(self, chatobj):
        return chatobj.sent_by.first_name
    
    def _get_tags_chat(self, chatobj):
        try:
            # print(chatobj.id)
            tmpchattags = ChatAdsTags.objects.filter(chat_id=chatobj.id)
            # print("tags", tmpchattags)
            if(len(tmpchattags)>0):
                return tmpchattags[0].TAGS
            else:
                return ""
        except Exception as e:
            print(e)
            return ""

        
    class Meta:
        model = Chats
        fields=('id','room_id','message','sent_by','chat_type','media_url','timestp','sender_name','tags')


class ChatroomMemberSerializer(serializers.ModelSerializer):
    user1_name = serializers.SerializerMethodField('_get_user_1')
    user2_name = serializers.SerializerMethodField('_get_user_2')
    # room_avatar = serializers.SerializerMethodField('_get_room_image')

    # def _get_room_image(self, roomobj):
    #     return 

    def _get_user_1(self, roomobj):
        # print("get user:",roomobj.user1.first_name)
        return roomobj.user1.first_name
    
    def _get_user_2(self, roomobj):
        return roomobj.user2.first_name



    class Meta:
        model = Chatroom
        fields =('id','user1','user2','timestp','room_name','user1_name','user2_name','room_avatar')


# class ChatroomListSerializer(serializers.ModelSerializer):
#     chatroom
#     class Meta:
#         model = Chatroom
#         fields =('user1','user2','timestp','room_name')