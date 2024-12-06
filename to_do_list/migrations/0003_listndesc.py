# Generated by Django 5.1.2 on 2024-10-27 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('to_do_list', '0002_customuser_groups_customuser_user_permissions_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListNDesc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
            ],
        ),
    ]
