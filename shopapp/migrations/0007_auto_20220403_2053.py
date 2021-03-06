# Generated by Django 3.1.4 on 2022-04-03 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0006_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date_posted',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(default='123-456-7890', max_length=150),
        ),
    ]
