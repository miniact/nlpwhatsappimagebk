from django.db import models
# from django.contrib.auth.models import User 

from ads.models import AdsDomains
# Create your models here.
from django.utils import timezone 

from django.conf import settings



def upload_to(instanse,filename):
    return 'images/{filename}'.format(filename=filename)

class Chatroom(models.Model):
    user1= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='user2')
    timestp = models.DateTimeField(default=timezone.now())
    room_name=models.CharField(max_length=50)
    room_avatar = models.ImageField(upload_to=upload_to, default='images/NLP_WATTSAPP.png',null=True)

    def __str__(self) :
        return self.room_name

    # class Meta:
    #     unique_together = ('user1', 'user2',)

# class MediaUrls(models.Model):
#     media_img = models.ImageField(null=True)
#     media_link = models.CharField(max_length=200,null=True)
#     mtype = models.CharField(choices=(('img','img'),('doc','doc')), default='img')


class Chats(models.Model):
    CTYPE = (
        ('msg','msg'),
        ('media','media'),
    )
    room_id = models.ForeignKey(Chatroom, on_delete=models.RESTRICT, related_name='room_id')
    message = models.TextField(max_length=600,default="BLANKNLPHAI")
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='sender')
    chat_type = models.CharField(choices=CTYPE, default='msg',max_length=10)
    media_url = models.ImageField(upload_to=upload_to, default='images/NLP_WATTSAPP.png',null=True)
    timestp = models.DateTimeField(default=timezone.now())
    nlp_processed = models.BooleanField(default=False)

    def __str__(self):
        if(self.chat_type == "media"):
            return str(self.media_url)
        else:
            return self.message

    


class ChatAdsTags(models.Model):
    chat_id = models.ForeignKey(Chats ,on_delete=models.RESTRICT, related_name='tag_chat_id')
    troom_id = models.ForeignKey(Chatroom ,on_delete=models.RESTRICT, related_name='tag_room_id')
    cleaned_chat = models.TextField(max_length=600,null=True)
    NERval = models.CharField(max_length=600)
    # TAGS = models.ForeignKey(AdsDomains,on_delete=models.RESTRICT, related_name='tags')
    TAGS = models.TextField(max_length = 300)

    def __str__(self):
        return  str(self.chat_id) 

class UserAds(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='user_id')
    # tags = models.ManyToManyField(AdsDomains)
    programming = models.DecimalField( max_digits=5,default=0, decimal_places=2)
    education = models.DecimalField( max_digits=5,default=0, decimal_places=2)
    technology = models.DecimalField( max_digits=5,default=0, decimal_places=2)
    heathcare = models.DecimalField( max_digits=5,default=0, decimal_places=2)
    medical = models.DecimalField( max_digits=5,default=0, decimal_places=2)
    fitness = models.DecimalField( max_digits=5,default=0, decimal_places=2)
    investment = models.DecimalField( max_digits=5,default=0, decimal_places=2)
    donation = models.DecimalField( max_digits=5,default=0, decimal_places=2)
    automobile = models.DecimalField( max_digits=5,default=0, decimal_places=2)
    job = models.DecimalField( max_digits=5,default=0, decimal_places=2)
    clothing = models.DecimalField( max_digits=5,default=0, decimal_places=2)
    food = models.DecimalField( max_digits=5,default=0, decimal_places=2)     
    photography = models.DecimalField( max_digits=5,default=0, decimal_places=2)     
    fintech = models.DecimalField( max_digits=5,default=0, decimal_places=2)     
    environment = models.DecimalField( max_digits=5,default=0, decimal_places=2)     
    sports = models.DecimalField( max_digits=5,default=0, decimal_places=2) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  


    def __str__(self):
       # return f"prog :{self.programming} | edu: {self.education} | tech:{self.technology} | med : {self.medical} | invest: {self.investment} | sport: {self.sports} | job:{self.job}"
       return str(self.user_id)
    # class Meta:
    #     unique_together = ['user_id']





