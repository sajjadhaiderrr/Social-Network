# Generated by Django 2.1.7 on 2019-04-03 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=500)),
                ('contentType', models.CharField(choices=[('text/plain', 'text/plain'), ('text/markdown', 'text/markdown'), ('application/base64', 'application/base64'), ('image/png;base64', 'image/png;base64'), ('image/jpeg;base64', 'image/jpeg;base64')], default='text/plain', max_length=32)),
                ('published', models.DateTimeField(auto_now=True)),
                ('commentauthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('postid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('source', models.URLField(null=True)),
                ('origin', models.URLField(null=True)),
                ('description', models.CharField(max_length=200)),
                ('contentType', models.CharField(choices=[('text/plain', 'text/plain'), ('text/markdown', 'text/markdown'), ('application/base64', 'application/base64'), ('image/png;base64', 'image/png;base64'), ('image/jpeg;base64', 'image/jpeg;base64')], default='text/plain', max_length=32)),
                ('content', models.TextField(blank=True)),
                ('categories', models.CharField(max_length=250)),
                ('published', models.DateTimeField(auto_now=True)),
                ('visibility', models.CharField(choices=[('PRIVATE', 'private to visibleTo list'), ('FRIENDS', 'private to my friends'), ('FOAF', 'private to friends of friends'), ('SERVERONLY', 'private to only firends on local server'), ('PUBLIC', 'public')], default='PUBLIC', max_length=10)),
                ('visibleTo', models.TextField(blank=True)),
                ('unlisted', models.BooleanField(default=False)),
                ('postauthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postauthor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='posting.Post'),
        ),
    ]
