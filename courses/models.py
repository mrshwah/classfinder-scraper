from django.db import models


class Course(models.Model):
    crn = models.IntegerField(primary_key=True)
    subject_id = models.TextField()
    section = models.TextField()
    title = models.TextField()
    credit = models.FloatField()
    room = models.TextField()
    begin = models.TimeField()
    end = models.TimeField()
    days = models.TextField()
    students_max = models.IntegerField()
    students_count = models.IntegerField()
    instructor = models.TextField()
    fees = models.FloatField()
