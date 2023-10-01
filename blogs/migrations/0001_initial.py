# Generated by Django 4.2.5 on 2023-10-01 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('Tech', 'Tech'), ('News', 'News'), ('ُSpecialized', 'Specialized')], default='unknown', max_length=20)),
                ('published', models.DateField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.users')),
            ],
        ),
    ]
