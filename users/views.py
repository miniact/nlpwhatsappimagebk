from django.views import generic
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer,NewUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from users.models import NewUser


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeUserDetails(generics.ListAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = NewUserSerializer 
    def get_queryset(self):
        # room_id = self.kwargs['room_id']
        # print(room_id)
        # room = Chatroom.objects.get(pk=room_id)
        # print(room.user1.id == self.request.user.id or  room.user1.id == self.request.user.id)
        print(self.request.user.id)
        try:
            
            return [NewUser.objects.get(pk=self.request.user.id)]
        except:
            return []

        
