from django.db import models


class RoomDayAndTime(models.Model):
    day = models.CharField(max_length=1)
    begin = models.TimeField()
    end = models.TimeField()
    room = models.TextField()


class Course(models.Model):
    crn = models.IntegerField(primary_key=True)
    subject_id = models.TextField()
    section = models.TextField()
    title = models.TextField()
    credit = models.FloatField()
    room_day_and_time = models.ManyToManyField(RoomDayAndTime)
    students_max = models.IntegerField()
    students_count = models.IntegerField()
    instructor = models.TextField()
    fees = models.FloatField()
