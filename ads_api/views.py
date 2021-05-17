from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from ads.models import Ads ,AdsDomains
from .serializers import AdsSerializer
from rest_framework import status
from rest_framework.response import Response
from chatnlp.models import UserAds

from rest_framework.permissions import IsAdminUser, DjangoModelPermissionsOrAnonReadOnly,IsAuthenticated



# from ads.models import Ads 

# Create your views here.

class AdsList(generics.ListCreateAPIView):
    # permission_classes= [IsAuthenticated]
    queryset = Ads.activeobj.all()
    serializer_class = AdsSerializer

    pass

class AdsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    queryset = Ads.activeobj.all()
    serializer_class = AdsSerializer
    pass 


class MyAdList(generics.ListAPIView):
    serializer_class = AdsSerializer
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # print(user, user.id)
        try:
            userAd = UserAds.objects.get(user_id=user.id)
            # print("userAD:" ,userAd)
            tagsIdMatch = {
                'programming': 1,
                'education':6 ,
                'technology':11 ,
                'heathcare':3 ,
                'medical':10 ,
                'fitness':12 ,
                'investment':2 ,
                'donation':7 ,
                'automobile':13,
                'job':9 ,
                'clothing':14 ,
                'food':8 ,
                'photography':15 ,
                'fintech':16 ,
                'environment':17,
                'sports':4 ,


            }

            tagsCountDict = {
                'programming': userAd.programming,
                'education':userAd.education ,
                'technology':userAd.technology ,
                'heathcare':userAd.heathcare ,
                'medical':userAd.medical ,
                'fitness':userAd.fitness ,
                'investment':userAd.investment ,
                'donation':userAd.donation ,
                'automobile':userAd.automobile,
                'job':userAd.job ,
                'clothing':userAd.clothing ,
                'food':userAd.food ,
                'photography':userAd.photography ,
                'fintech':userAd.fintech ,
                'environment':userAd.environment,
                'sports':userAd.sports ,
            }
            # print("tagsCountDict:",tagsCountDict)
            totalcount = sum(tagsCountDict.values())
            # print("tc:",totalcount )
            if(totalcount==0):
                totalcount=1

            tagsPercentDict = {
                'programming': (userAd.programming*100)//totalcount,
                'education':(userAd.education*100)//totalcount ,
                'technology':(userAd.technology*100)//totalcount ,
                'heathcare':(userAd.heathcare*100)//totalcount ,
                'medical':(userAd.medical*100)//totalcount ,
                'fitness':(userAd.fitness*100)//totalcount ,
                'investment':(userAd.investment*100)//totalcount ,
                'donation':(userAd.donation*100)//totalcount ,
                'automobile':(userAd.automobile*100)//totalcount,
                'job':(userAd.job*100)//totalcount ,
                'clothing':(userAd.clothing*100)//totalcount ,
                'food':(userAd.food*100)//totalcount ,
                'photography':(userAd.photography*100)//totalcount ,
                'fintech':(userAd.fintech*100)//totalcount ,
                'environment':(userAd.environment*100)//totalcount,
                'sports':(userAd.sports*100)//totalcount ,

            }
            print("tagsPercentDict: ",tagsPercentDict)
            sortedtagsCount = list(sorted(tagsCountDict.items(), key=lambda item: item[1],reverse = True))
            print("Sortedtags:", sortedtagsCount)
            #max 6 ads +-2 3
            todisplayTagDict = dict()
            for el in sortedtagsCount:
                taghai = el[0]
                if(el[1] >0):
                    todisplayTagDict[taghai] = int(6*(tagsPercentDict[taghai]/100))+1
            print("todisplayTagDict:      ",todisplayTagDict)

            ##FETCH ADS FROM ADS based on todisplayTagDict
            grandresponse = [] 

            # fetchsportsads = Ads.activeobj.filter(tags=4)
            # print("fetchsportsads:    ",fetchsportsads)
            for tagname, countdisplayads in todisplayTagDict.items():
                fetchads = Ads.activeobj.filter(tags= tagsIdMatch[tagname])
                #if there are less no of ads than required then display all
                if(len(fetchads)>0 and len(fetchads)<=countdisplayads):
                    for el in fetchads:
                        grandresponse.append(el)
                else:
                    count=0
                    for el in fetchads:
                        if(count > countdisplayads):
                            break
                        grandresponse.append(el)
                        count += 1



















            #return all ads
            # return Ads.activeobj.all()
            #return calucaletd ads
            return grandresponse

        except Exception as e:
            print(e)
            return []



# class ChatsList(APIView,ChatsUserReadWritePermission):
#     permission_classes= [IsAuthenticated,ChatsUserReadWritePermission]

#     # queryset = Chats.objects.all()
#     # serializer_class = ChatsSerializer
#     def post(self, request , format=None):
#         print(request.data)
#         serializer = ChatsSerializer(data= request.data)
#         if serializer.is_valid() and request.user.id == int(request.data['sent_by']):
#             serializer.save()
#             print("SData: ", serializer.data)
#             pusher.trigger(request.data['room_id'], 'newmessage', serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






""" Concrete View Classes
#CreateAPIView
Used for create-only endpoints.
#ListAPIView
Used for read-only endpoints to represent a collection of model instances.
#RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
#DestroyAPIView
Used for delete-only endpoints for a single model instance.
#UpdateAPIView
Used for update-only endpoints for a single model instance.
##ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""