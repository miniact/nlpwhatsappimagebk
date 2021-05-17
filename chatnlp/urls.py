from django.urls import path
from .views import ChatRoomDetail , ChatRoomList, ChatsDetail,ChatsList,ChatSync,ChatRoomMembersDetail,ChatsListUpload,ChatNLPprocessing,CleanDataForNLP


app_name = 'chat_api'

urlpatterns = [
    path('chatroom/<int:pk>', ChatRoomDetail.as_view(), name='detailroom'),
    path('chatroom/<int:room_id>/members', ChatRoomMembersDetail.as_view(), name='detailroom'),
    path('chatroom/', ChatRoomList.as_view(), name='listrooms'),
    path('chat/<int:pk>', ChatsDetail.as_view(), name='detailcreate'),
    path('chat/', ChatsList.as_view(), name='listcreate'),
    path('chat/upload', ChatsListUpload.as_view(), name='listcreate'),
    path('chatsync/<int:room_id>', ChatSync.as_view(), name='chatsync'),
    path('startnlpprocessing/',ChatNLPprocessing,name='nlp_process'),
    path('cleandatafornlp/',CleanDataForNLP, name="clean_data" ),
    
]
