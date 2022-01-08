# Generated by Django 3.2.9 on 2022-01-08 02:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qux_newsfeed', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsitem',
            options={'ordering': ['-id'], 'verbose_name': 'News Item', 'verbose_name_plural': 'News Items'},
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('voter', 'item')},
        ),
    ]
