'''
from django.conf import settings
import dj_database_url

settings.configure(
    DATABASES={
        'default': dj_database_url.config(conn_max_age=600)
    },
    INSTALLED_APPS={
        'courses'
    }
)

import django
django.setup()
'''

from courses.models import Course, RoomDayAndTime


class RequestedCourse:
    def __init__(self, rank, title):
        self.rank = rank
        self.title = title

    def __str__(self):
        return 'Title = {}, Rank = {}'.format(self.title, self.rank)


def create_schedule(requested_courses):
    possibilities = [list(Course.objects.filter(title=course.title)) for course in requested_courses]
    return possibilities


courses = [RequestedCourse(1, "Biochemistry I Full Term"),
           RequestedCourse(2, "Circut Training Full Term"),
           RequestedCourse(3, "Copyright Law Full Term")]

schedule = create_schedule(courses)
for courses in schedule:
    for course in courses:
        print(course.title)
