# Generated by Django 2.2.4 on 2019-11-03 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20190708_0850'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depth', models.PositiveIntegerField(editable=False)),
                ('queue', models.PositiveIntegerField(editable=False)),
                ('body', models.CharField(default='comment', max_length=128)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='articles.Article')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]