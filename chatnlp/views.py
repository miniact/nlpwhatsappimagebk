from django.shortcuts import render
from rest_framework import generics, serializers,status
from rest_framework.views import APIView
from .models import ChatAdsTags, Chats,Chatroom,UserAds
from .serializers import ChatAdsTagsSerializer, ChatroomSerializer,ChatsSerializer,UserAdsSerializer,ChatroomMemberSerializer
from django.db.models import Q
from rest_framework.response import Response 
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from pusher import Pusher
from django.conf import settings
#F exp for real update  race condition
from django.db.models import F
from django.contrib.admin.views.decorators import staff_member_required

# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


from rest_framework.permissions import IsAdminUser, DjangoModelPermissionsOrAnonReadOnly,IsAuthenticated,BasePermission


#pusher
pusher = Pusher(app_id=settings.PUSHER_APP_ID, key=settings.PUSHER_APP_KEY, secret=settings.PUSHER_APP_SECRET, cluster=settings.PUSHER_APP_CLUSTER)
# print(pusher)



class ChatsUserReadWritePermission(BasePermission):
    message = 'only user within this room able to read and write!'

    def has_object_permission(self, request, view, obj):
        
        if request.method in ('OPTIONS','HEAD'):
            return True 
        
        room_id  = obj.room_id
        # print(room_id.id)

        try:
            chatroom = Chatroom.objects.get(pk=room_id.id)
            print(chatroom,chatroom.user1.id, chatroom.user2.id,request.user.id)
            return chatroom.user1.id == request.user.id or chatroom.user2.id == request.user.id 
        except:
            return False

        

class ChatsSyncPermission(BasePermission):
    message = 'only user within this room able to read and write!'

    def has_object_permission(self, request, view, obj):
        
        if request.method in ('OPTIONS','HEAD'):
            return True 
        print(obj)
        room_id  = obj.room_id
        print(room_id.id)


        try:
            chatroom = Chatroom.objects.get(pk=room_id.id)
            print(chatroom,chatroom.user1.id, chatroom.user2.id,request.user.id)
            return chatroom.user1.id == request.user.id or chatroom.user2.id == request.user.id 
        except:
            return False
        
        
        





# from ads.models import Ads 

# Create your views here.

class ChatRoomList(generics.ListCreateAPIView):
    permission_classes= [IsAuthenticated]
    # queryset = Chatroom.objects.all()
    serializer_class = ChatroomSerializer
    def get_queryset(self):
        return Chatroom.objects.all().filter(Q(user1=self.request.user.id) | Q(user2 = self.request.user.id))

    

class ChatRoomDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes= [IsAuthenticated]
    queryset = Chatroom.objects.all()
    serializer_class = ChatroomSerializer
    

class ChatsList(APIView,ChatsUserReadWritePermission):
    permission_classes= [IsAuthenticated,ChatsUserReadWritePermission]

    # queryset = Chats.objects.all()
    # serializer_class = ChatsSerializer
    def post(self, request , format=None):
        print(request.data)
        serializer = ChatsSerializer(data= request.data)
        if serializer.is_valid() and request.user.id == int(request.data['sent_by']):
            serializer.save()
            print("SData: ", serializer.data)
            pusher.trigger(request.data['room_id'], 'newmessage', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            




class ChatsListUpload(APIView,ChatsUserReadWritePermission):
    permission_classes= [IsAuthenticated,ChatsUserReadWritePermission]
    parser_classes = [MultiPartParser, FormParser]

    # queryset = Chats.objects.all()
    # serializer_class = ChatsSerializer

    def post(self,request, format=None):
        print(request.data)
        print("uid",request.user.id)
        print("sent:" , int(request.data['sent_by']))
        serializer = ChatsSerializer(data=request.data)
        if serializer.is_valid() and request.user.id == int(request.data['sent_by']):
            serializer.save()
            pusher.trigger(request.data['room_id'], 'newmessage', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    

class ChatsDetail(generics.RetrieveUpdateDestroyAPIView,ChatsUserReadWritePermission):
    permission_classes= [ChatsUserReadWritePermission]
    queryset = Chats.objects.all()
    serializer_class = ChatsSerializer 


class ChatSync(generics.ListAPIView):
    permission_classes= [ChatsSyncPermission]
    serializer_class = ChatsSerializer 
    def get_queryset(self):
        room_id = self.kwargs['room_id']
        # print(room_id)
        # room = Chatroom.objects.get(pk=room_id)
        # print(room.user1.id == self.request.user.id or  room.user1.id == self.request.user.id)
        try:
            room = Chatroom.objects.get(pk=room_id)
            if(room.user1.id == self.request.user.id or  room.user2.id == self.request.user.id):
                return Chats.objects.all().filter(room_id= room_id)
        except:
            return 
        



class ChatRoomMembersDetail(generics.ListAPIView):
    # permission_classes =[ChatsUserReadWritePermission]
    permission_classes=[IsAuthenticated]
    serializer_class = ChatroomMemberSerializer
    def get_queryset(self):
        room_id = self.kwargs['room_id']
        # print(room_id)
        # room = Chatroom.objects.get(pk=room_id)
        # print(room.user1.id == self.request.user.id or  room.user1.id == self.request.user.id)
        try:
            room = Chatroom.objects.get(pk=room_id)
            if(room.user1.id == self.request.user.id or  room.user2.id == self.request.user.id):
                return [Chatroom.objects.get(pk=room_id)]
        except:
            
            content = {'fmsg': 'Only user within this room able to read and write!'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)


    
        # return Response(datah)

@staff_member_required
def CleanDataForNLP(request):
    Chats.objects.all().update(nlp_processed=False)
    UserAds.objects.all().update(
        programming=0 ,#F('programming') +tags.count('programming'),
        education=0 ,#F('education')+tags.count('education'),
        technology=0 ,#F('technology')+tags.count('technology'),
        heathcare=0 ,#F('heathcare')+tags.count('heathcare'),
        medical=0 ,#F('medical')+tags.count('medical'),
        fitness=0 ,#F('fitness')+tags.count('fitness'),
        investment=0 ,#F('investment')+tags.count('investment'),
        donation=0 ,#F('donation')+tags.count('donation'),
        automobile=0 ,#F('automobile')+tags.count('automobile'),
        job=0 ,#F('job')+tags.count('job'),
        clothing=0 ,#F('clothing')+tags.count('clothing'),
        food=0 ,#F('food')+tags.count('food'),
        photography=0 ,#F('photography')+tags.count('photography'),
        fintech=0 ,#F('fintech')+tags.count('fintech'),
        environment=0 ,#F('environment')+tags.count('environment'),
        sports=0 ,#F('sports')+tags.count('sports')
    )
    ChatAdsTags.objects.all().delete()
    print("DATA CLEANED !")
    return render(request, 'startnlp.html')





####NLP STARTED MANGYA  


import spacy
nlp = spacy.load('en_core_web_lg')
# nlp.add_pipe(nlp.create_pipe('merge_noun_chunks'))
nlp.add_pipe("merge_noun_chunks")

domains = ['programming', 'education', 'technology','heathcare','medical', 'fitness', 'investment', 'donation','automobile','job','clothing','food','photography','travel','fintech','environment','sports']



domainsnlparr = list(nlp.pipe(domains))







def get_most_related_domain_3diff(docobj):
  scores = dict()
  for d in domainsnlparr:
    scores[d.text] = round(d.similarity(docobj),2)
  temp = list(sorted(scores.items(), key=lambda item: item[1],reverse = True))
  # print(temp)
  res=[]
  res.append(temp[0])
  maxscore = temp[0][1]
  # print(maxscore)
  minallowedscore = round(abs(maxscore-0.03),2)
  # print(minallowedscore)
  for i in range(1,len(temp)):
    if(temp[i][1]>minallowedscore):
      res.append(temp[i])
  return res


#############################################################################IMAGE CAPTIONING######################################



from pickle import load
from numpy import argmax
from keras.preprocessing.sequence import pad_sequences
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from keras.models import load_model
 
# extract features from each photo in the directory
def extract_features(filename):
    # load the model
    model = VGG16()
    # re-structure the model
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
    # load the photo
    image = load_img(filename, target_size=(224, 224))
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)
    # get features
    feature = model.predict(image, verbose=0)
    return feature
 
# map an integer to a word
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None
 
# generate a description for an image
def generate_desc(model, tokenizer, photo, max_length):
    # seed the generation process
    in_text = 'startseq'
    # iterate over the whole length of the sequence
    for i in range(max_length):
        # integer encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad input
        sequence = pad_sequences([sequence], maxlen=max_length)
        # predict next word
        yhat = model.predict([photo,sequence], verbose=0)
        # convert probability to integer
        yhat = argmax(yhat)
        # map integer to word
        word = word_for_id(yhat, tokenizer)
        # stop if we cannot map the word
        if word is None:
            break
        # append as input for generating the next word
        in_text += ' ' + word
        # stop if we predict the end of the sequence
        if word == 'endseq':
            break
    return in_text

import os
from django.conf import settings
# load the tokenizer
# tokenpath = str(os.path.join(settings.BASE_DIR, 'tokenizer.pkl'))
tokenizer = load(open('tokenizer.pkl', 'rb'))
# pre-define the max sequence length (from training)
max_length = 34
# load the model
# model = load_model('model-ep002-loss3.245-val_loss3.612.h5')
# # load and prepare the photograph
# photo = extract_features('example.jpg')
# # generate description
# description = generate_desc(model, tokenizer, photo, max_length)
# print(description)
# modelpath = str(os.path.join(settings.BASE_DIR, 'model_p-4.h5'))
#Load Models
ImROA_update_model = load_model('model_p-4.h5')


def oneimagedesc(imgpath):
#   imgobj = Image(filename=imgpath ,width = 500, height = 500)
#   display(imgobj)
  photo = extract_features(imgpath)
#   print("")
#   print("******************ImROA_update_model***************************")
  description_ImROA = generate_desc(ImROA_update_model, tokenizer, photo, max_length)
  return description_ImROA[8:-7]
 


def image_to_caption(patharr):
    print(patharr)
    all_captions_arr = []
    for el in patharr:
        tmppath = os.path.join(settings.MEDIA_ROOT, str(el))
        tmpdesc = oneimagedesc(tmppath)
        print(tmpdesc)
        all_captions_arr.append(tmpdesc)
    return all_captions_arr


        






def get_tags_by_chat_nlpobj_arr(nlpobjarr):

  CHATTAGS =[]
  NERCHAT=[]
  for chat in nlpobjarr:
    # print(chat.text)
    processed = []
    
    TAGS = []
    # print("*****************|ENTITY EXTRACT|************************")
    for entity in chat.ents:
      if(entity.label_ !='DATE' and entity.label_ !='GPE'):
        # print(entity.text,entity.label_)
        # print(get_most_related_domain_3diff(entity))
        tmpent =get_most_related_domain_3diff(entity)
        for el in tmpent:
          TAGS.append(el[0])
        processed.append(entity.text)
        
        

      
    # print("*****************|CHATS EXTRACT|************************")
    
    for token in chat:
      if token.pos_ == 'NOUN' or token.pos_ == 'PROPN' and token.is_stop==False: #or token.pos_ == 'VERB':
        if token.text not in processed:
          tmp =get_most_related_domain_3diff(token)
          for el in tmp:
            TAGS.append(el[0])
          # print(token.text,"-->", token.pos_,"sim: ",," || ", end="  ")
    CHATTAGS.append(TAGS)
    NERCHAT.append(processed)
  return [CHATTAGS,NERCHAT]

@staff_member_required
def ChatNLPprocessing(request):
    #only for chat msg nlp processing
    all_chat_media = Chats.objects.filter(chat_type='media',nlp_processed=False)
    all_media_urls =[]
    for el in all_chat_media:
        all_media_urls.append(el.media_url)
    all_captions_arr = image_to_caption(all_media_urls)

    #image to caption save in dataabse as a message
    for chat,caption in zip(all_chat_media,all_captions_arr):
        chat.message = caption 
        chat.save()



    # all_chats_db = Chats.objects.filter(chat_type='msg',nlp_processed=False)
    all_chats_db = Chats.objects.filter(nlp_processed=False)
    # print(type(all_chats),list(all_chats))
    all_chats_id =[]
    all_chats_room_id =[]
    all_chats_msg=[]
    for el in all_chats_db:
        all_chats_id.append(el.id)
        all_chats_room_id.append(el.room_id.id)
        all_chats_msg.append(el.message)
    
    all_chat_nlparr = list(nlp.pipe(all_chats_msg))
    # print(all_chat_nlparr)
    temphai = get_tags_by_chat_nlpobj_arr(all_chat_nlparr)
    all_chat_tags = temphai[0]
    NERval = temphai[1]
    try:
        for cid,rid,msg,ner,tags in zip(all_chats_id,all_chats_room_id,all_chat_nlparr,NERval,all_chat_tags):
            print(cid,rid,msg, "-->", tags,"ner: ", ner)
            tmpchat = Chats.objects.get(pk=cid)
            tmproom = Chatroom.objects.get(pk=rid)
            tmp = ChatAdsTags(chat_id=tmpchat,troom_id=tmproom,NERval=' '.join(ner),TAGS=' '.join(tags) )
            print(tmp)
            tmp.save()
            
            # person, created = Person.objects.get_or_create(identifier=id)

            # if created:
            # # means you have created a new person
            # else:
            # # person just refers to the existing one


           #####STEP2###################### #check if alredy an user  entry is present in UserAds table if not then create else update the tags counts
            userad = UserAds.objects.filter(user_id=tmproom.user1)
            if(len(userad)==0):

                #create new one 
                #tmpUserAD = UserAds(user_id=tmproom.user1, programming=,education=,technology=,heathcare=,medical=,fitness=,investment=,donation=,automobile=,job=,clothing=,food=,photography=,fintech=,environment=,sports=)
                tmpUser1AD = UserAds(user_id=tmproom.user1, programming=tags.count('programming'),education=tags.count('education'),technology=tags.count('technology'),heathcare=tags.count('heathcare'),medical=tags.count('medical'),fitness=tags.count('fitness'),investment=tags.count('investment'),donation=tags.count('donation'),automobile=tags.count('automobile'),job=tags.count('job'),clothing=tags.count('clothing'),food=tags.count('food'),photography=tags.count('photography'),fintech=tags.count('fintech'),environment=tags.count('environment'),sports=tags.count('sports'))
                print(tmpUser1AD, "user 1 saved")
                tmpUser1AD.save()
                tmpUser2AD = UserAds(user_id=tmproom.user2, programming=tags.count('programming'),education=tags.count('education'),technology=tags.count('technology'),heathcare=tags.count('heathcare'),medical=tags.count('medical'),fitness=tags.count('fitness'),investment=tags.count('investment'),donation=tags.count('donation'),automobile=tags.count('automobile'),job=tags.count('job'),clothing=tags.count('clothing'),food=tags.count('food'),photography=tags.count('photography'),fintech=tags.count('fintech'),environment=tags.count('environment'),sports=tags.count('sports'))
                print(tmpUser2AD ,"user2 saved")
                tmpUser2AD.save()
            elif (len(userad)==1):
                #update the values
                userad.update( 
                programming=F('programming') +tags.count('programming'),
                education=F('education')+tags.count('education'),
                technology=F('technology')+tags.count('technology'),
                heathcare=F('heathcare')+tags.count('heathcare'),
                medical=F('medical')+tags.count('medical'),
                fitness=F('fitness')+tags.count('fitness'),
                investment=F('investment')+tags.count('investment'),
                donation=F('donation')+tags.count('donation'),
                automobile=F('automobile')+tags.count('automobile'),
                job=F('job')+tags.count('job'),
                clothing=F('clothing')+tags.count('clothing'),
                food=F('food')+tags.count('food'),
                photography=F('photography')+tags.count('photography'),
                fintech=F('fintech')+tags.count('fintech'),
                environment=F('environment')+tags.count('environment'),
                sports=F('sports')+tags.count('sports')
                )

                print("Pahele se hai user1:", userad)
                # userad.save()

                userad2 = UserAds.objects.filter(user_id=tmproom.user2)
                userad2.update( 
                programming=F('programming') +tags.count('programming'),
                education=F('education')+tags.count('education'),
                technology=F('technology')+tags.count('technology'),
                heathcare=F('heathcare')+tags.count('heathcare'),
                medical=F('medical')+tags.count('medical'),
                fitness=F('fitness')+tags.count('fitness'),
                investment=F('investment')+tags.count('investment'),
                donation=F('donation')+tags.count('donation'),
                automobile=F('automobile')+tags.count('automobile'),
                job=F('job')+tags.count('job'),
                clothing=F('clothing')+tags.count('clothing'),
                food=F('food')+tags.count('food'),
                photography=F('photography')+tags.count('photography'),
                fintech=F('fintech')+tags.count('fintech'),
                environment=F('environment')+tags.count('environment'),
                sports=F('sports')+tags.count('sports')
                )
                print("Pahele se hai user2:", userad2)
                # userad2.save()

            else:
                print("DUP USER ADS FOUND")
        
            ######STEP 3##### )UPDATE THE status of Chats table nlp_processed = True

            tmpchat.nlp_processed=True
            tmpchat.save()



            


    except Exception as e:
            print (e)
        



    
    # for id,rid,msg in zip(all_chats_id,all_chats_room_id,all_chats_msg):
    #     print(id,rid,msg)





    return render(request, 'startnlp.html')

    


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