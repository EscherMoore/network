# Generated by Django 3.2.2 on 2021-07-31 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_like_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='like_value',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='network.like'),
        ),
    ]
