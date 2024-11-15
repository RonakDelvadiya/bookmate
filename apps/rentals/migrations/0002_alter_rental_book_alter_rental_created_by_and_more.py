# Generated by Django 5.1.2 on 2024-10-13 15:03

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('rentals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='book',
            field=models.ForeignKey(help_text='The book that was rented.', on_delete=django.db.models.deletion.CASCADE, to='books.book'),
        ),
        migrations.AlterField(
            model_name='rental',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='The user who created this rental record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rental_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rental',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, help_text='The user who last modified this rental record.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rental_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rental',
            name='rental_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='The date and time when the book was rented.'),
        ),
        migrations.AlterField(
            model_name='rental',
            name='return_date',
            field=models.DateTimeField(blank=True, help_text='The date and time when the book was returned. Leave blank if not yet returned.', null=True),
        ),
        migrations.AlterField(
            model_name='rental',
            name='returned',
            field=models.BooleanField(default=False, help_text='Indicates whether the book has been returned. If returned date is provided, it will be set to True automatically.'),
        ),
        migrations.AlterField(
            model_name='rental',
            name='student',
            field=models.ForeignKey(help_text='The student who rented the book.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
