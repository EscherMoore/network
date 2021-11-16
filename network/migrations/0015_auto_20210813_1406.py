# Generated by Django 3.2.2 on 2021-08-13 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_alter_user_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.URLField(blank=True, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png', max_length=240),
        ),
    ]
