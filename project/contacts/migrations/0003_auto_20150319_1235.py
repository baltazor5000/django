# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_contact_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='pic',
            field=models.ImageField(default=b'', upload_to=b'images/', verbose_name=b'Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='upload_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 19, 12, 35, 15, 97637, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
