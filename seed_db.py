import datetime
import json

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

from courses.models import Course, RoomDayAndTime

with open('fall18.json') as json_data:
    courses = json.load(json_data)

room_days_and_times = []

for course in courses['courses']:
    if '*' in course['crn']:
        continue

    # Divide into multiple rooms if necessary
    rooms = course['room']
    rooms = rooms.split()

    # Divide into multiple times if necessary
    # and format time string
    begin_times = course['begin']
    begin_times = begin_times.split()
    begin_times = [begin_times[i] + ' ' + begin_times[i + 1] for i in range(0, len(begin_times) - 1, 2)]

    end_times = course['end']
    end_times = end_times.split()
    end_times = [end_times[i] + ' ' + end_times[i + 1] for i in range(0, len(end_times) - 1, 2)]

    # Divide into multiple days if necessary
    # and match with time
    days = course['days']
    days = days.split()
    days = [list(days[i]) for i in range(len(days))]

    # Put everything together in a RoomDayTime object
    for i in range(len(begin_times)):
        # begin time formatting
        if 'PM' in begin_times[i] and '12' not in begin_times[i]:
            begin = datetime.time(int(begin_times[i][0:2]) + 12, int(begin_times[i][2:4]))
        elif 'TBA' in course['begin']:
            begin = datetime.time(0, 0)
        else:
            begin = datetime.time(int(begin_times[i][0:2]), int(begin_times[i][2:4]))

        # end time formatting
        if 'PM' in end_times[i] and '12' not in end_times[i]:
            end = datetime.time(int(end_times[i][0:2]) + 12, int(end_times[i][2:4]))
        elif 'TBA' in end_times[i]:
            end = datetime.time(0, 0)
        else:
            end = datetime.time(int(end_times[i][0:2]), int(end_times[i][2:4]))
        if len(days[i]) > 0:
            for day in days[i]:
                new_rdt = RoomDayAndTime(begin=begin, end=end, day=day, room=rooms[i])
                room_days_and_times.append(new_rdt)

    if '$' in course['fees']:
        fees = float(course['fees'].replace('$ ', ''))
    else:
        fees = 0

    match = Course.objects.filter(crn=course['crn']).first()

    if match is not None:
        continue

    course_to_add = Course(crn=int(course['crn']),
                           subject_id=course['subject'],
                           section=course['section'],
                           title=course['title'],
                           credit=course['credit'],
                           students_max=course['max'],
                           students_count=course['count'],
                           instructor=course['instructor'],
                           fees=fees)

    course_to_add.save()

    for rdt in room_days_and_times:
        rdt.save()
        course_to_add.room_day_and_time.add(rdt)
