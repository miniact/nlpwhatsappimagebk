# Generated by Django 3.2 on 2021-05-14 00:45

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chatnlp', '0009_auto_20210514_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatadstags',
            name='troom_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='tag_room_id', to='chatnlp.chatroom'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chatadstags',
            name='chat_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='tag_chat_id', to='chatnlp.chats'),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='timestp',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 14, 0, 44, 13, 668948, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='chats',
            name='timestp',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 14, 0, 44, 13, 669942, tzinfo=utc)),
        ),
    ]
