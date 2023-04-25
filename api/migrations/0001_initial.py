# Generated by Django 4.1.6 on 2023-04-19 09:15

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Demande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typecongee', models.CharField(choices=[('Annuel', 'Annuel'), ('Malade', 'Malade'), ('Maternite', 'Maternite'), ('Exceptionnelle', 'Exceptionnelle')], max_length=100)),
                ('excep', models.CharField(choices=[('m', 'Mariage'), ('mf', "Mariage d'un(e) fils/fille ou d'un(e) frere/soeur"), ('deJE', "deces du conjoint ou d'un enfant"), ('deMP', 'deces de la mere ou  du pere'), ('naisE', "Naissance d'un enfant"), ('batE', "Bateme d'un enfant"), ('auter', 'permission autre')], max_length=100, null=True)),
                ('commentair', models.CharField(blank=True, max_length=300, null=True)),
                ('nbenf', models.PositiveIntegerField(default=0)),
                ('dateCongee', models.DateField()),
                ('dureeCongee', models.IntegerField()),
                ('decision', models.BooleanField(blank=True, null=True)),
                ('approuver', models.BooleanField(blank=True, null=True)),
                ('created_date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('created_time', models.TimeField(blank=True, default=django.utils.timezone.now)),
                ('decisioner_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='decisioner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(choices=[('info', 'Informatique'), ('finance', 'Finance et comptabilité'), ('rh', 'Ressource humain')], max_length=200, null=True)),
                ('responsable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(choices=[('responsable', 'responsable'), ('gaus', 'gaus')], max_length=200, null=True)),
                ('direction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.direction')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateCommance', models.DateField(blank=True, null=True)),
                ('matricule', models.PositiveIntegerField(null=True)),
                ('photo', models.ImageField(null=True, upload_to=api.models.upload_photo)),
                ('gender', models.CharField(choices=[('F', 'Femme'), ('H', 'Homme')], max_length=200, null=True)),
                ('Poste', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.post')),
                ('direction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.direction')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(choices=[('info', 'Informatique'), ('finance', 'Finance et comptabilité'), ('rh', 'Ressource humain')], max_length=128, unique=True)),
                ('notif', models.ManyToManyField(blank=True, to='api.demande')),
                ('responsable', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InfoRH',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solde_jours', models.PositiveIntegerField()),
                ('jours_date', models.PositiveIntegerField()),
                ('visa_rh', models.CharField(max_length=30)),
                ('visa_drh', models.CharField(max_length=30)),
                ('date', models.CharField(max_length=30)),
                ('comentaire', models.CharField(blank=True, max_length=200, null=True)),
                ('demande', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rh', to='api.demande')),
            ],
        ),
        migrations.AddField(
            model_name='demande',
            name='direction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='direction', to='api.direction'),
        ),
        migrations.AddField(
            model_name='demande',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CalendarEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('backgroundColor', models.CharField(blank=True, max_length=100, null=True)),
                ('direction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.direction')),
                ('id_d', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.demande')),
            ],
        ),
    ]
