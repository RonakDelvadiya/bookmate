# Generated by Django 5.1.2 on 2024-10-13 15:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(blank=True, help_text='The author of the book. Can be left blank.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='The user who created this book record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, help_text='The user who last modified this book record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='number_of_pages',
            field=models.PositiveIntegerField(blank=True, help_text='The number of pages in the book. Can be left blank.', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(help_text='The title of the book. Must be unique.', max_length=255, unique=True),
        ),
    ]
