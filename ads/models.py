from django.db import models
from django.utils import timezone

# Create your models here.

class AdsDomains(models.Model):
    domain_name = models.CharField(max_length=50)


    def __str__(self):
        return self.domain_name



class Tag(models.Model):

    DOMAINS = (
        ('IT','IT'),
        ('EDUCATION','EDUCATION'),
        ('TECH','TECH'),
        ('MEDICAL','MEDICAL'),
        ('FITNESS','FITNESS'),
        ('INVESTMENT','INVESTMENT'),
        ('NGO','NGO'),
        ('MECHANICS','MECHANICS'),
        ('ELECTRIC','ELECTRIC'),
        ('MOTOR','MOTOR'),
        ('JOB','JOB'),


    )
    tname =  models.CharField(max_length=50)
    domain =  models.ForeignKey(AdsDomains, on_delete=models.RESTRICT, related_name='domain')

    def __str__(self):
        return self.tname



class Ads(models.Model):

    class ActiveAds(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_active ='active')

    OPTION = (
        ('active','active'),
        ('inactive','inactive'),
    )
    orgname = models.CharField(max_length=200)
    weburl = models.CharField(max_length=255)
    adsdec = models.TextField(max_length=400)
    tags = models.ManyToManyField(AdsDomains)
    adimg = models.ImageField(upload_to='images/', default='images/NLP_WATTSAPP.png')
    pubtime = models.DateTimeField(default=timezone.now())
    is_active = models.CharField(max_length=20, choices=OPTION, default='active')
    objects = models.Manager()
    activeobj = ActiveAds()

    class Meta:
        ordering = ('-pubtime',)



    def __str__(self):
        return self.orgname +" : "+ self.adsdec[:40] 


