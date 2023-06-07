from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class Classroom(models.Model):
    # 默认定义的自增长id作为键
    id = models.AutoField(primary_key=True)
    classroom_name = models.CharField(max_length = 128)
    building = models.CharField(max_length = 128)
#    recommand= models.IntegerField()
    classroom_covered = models.BooleanField()

class Occupytable(models.Model):
    classroom_id = models.IntegerField()
    date = models.CharField(max_length = 10)
    time = models.CharField(max_length = 10)
    available = models.BooleanField()
    covered = models.BooleanField()

class Labeltable(models.Model):
    id = models.AutoField(primary_key=True)
    label_name = models.CharField(max_length = 128)

class LabelClassroom(models.Model):
    id = models.AutoField(primary_key=True)
    classroom_id = models.IntegerField()
    label_id = models.IntegerField()
'''
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
'''