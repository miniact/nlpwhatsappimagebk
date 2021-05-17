# Generated by Django 3.2 on 2021-05-05 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chatnlp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userads',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='chat_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chats',
            name='room_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='room_id', to='chatnlp.chatroom'),
        ),
        migrations.AddField(
            model_name='chats',
            name='sent_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='user1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='user2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatadstags',
            name='TAGS',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='tags', to='ads.adsdomains'),
        ),
        migrations.AddField(
            model_name='chatadstags',
            name='chat_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='chat_id', to='chatnlp.chats'),
        ),
    ]