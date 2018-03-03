def makeSchedule(courses):
    courseSchedule = []
    i = 0  # Tracks which course you are looking at

    for course in courses:  # Iterate through different courses
        j = 0  # Tracks which section you are looking at
        for section in courses[i]:  # Iterate through individual sections of each course
            fits = True
            for finalCourse in courseSchedule:  # Iterate through the current schedule, what we have so far
                dayNumber = 0
                for day in finalCourse.days:
                    for timeSlot in section.days[dayNumber]:
                        for timeSlotFinal in finalCourse.days[dayNumber]:
                            if (timeSlot <= finalCourse.days[dayNumber][timeSlotFinal]
                                    and section.days[dayNumber][timeSlot] >= finalCourse.days[dayNumber][
                                        timeSlotFinal]):
                                fits = False
                                break  # Keep looking; there is an overlap
                            elif (section.days[dayNumber][timeSlot] >= timeSlotFinal
                                  and section.days[dayNumber][timeSlot] <= finalCourse.days[dayNumber][timeSlotFinal]):
                                fits = False
                                break  # Keep looking; there is an overlap
                            elif timeSlot == timeSlotFinal:
                                fits = False
                                break
                            elif section.days[dayNumber][timeSlot] == finalCourse.days[dayNumber][timeSlotFinal]:
                                fits = False
                                break

            if fits:
                courseSchedule.append(courses[i][j])  # if we make it through every course in our schedule
                break  # with no conflicts, add it to schedule and move to next
            j += 1
        i += 1

    return courseSchedule


class Course():
    def __init__(self, days, name):
        self.days = days  # In each course object, I'm assuming days is a list of dictionaries;
        # each dictionary corresponds to a day of the week, M through F in order,
        # and each dictionary entry has a key start time and value end time.
        # Ex. days = [ {1100 : 1215, 930 : 1045} , {1530 : 16:45} ] -> M and T times.
        self.name = name


def testMakeSchedule():
    days1 = [{1200: 1250}, {}, {1200: 1250}, {}, {1200: 1250}]
    englishSection1 = Course(days1, "eng1")
    days2 = [{1300: 1350}, {}, {1300: 1350}, {}, {1300: 1350}]
    englishSection2 = Course(days2, "eng2")
    days3 = [{}, {1230: 1345, 1100: 1215}, {}, {1230: 1345}, {}]
    mathSection1 = Course(days3, "mth1")
    days4 = [{1300: 1350}, {}, {1300: 1350}, {}, {1300: 1350}]
    chemistrySection1 = Course(days4, "cem1")
    days5 = [{1200: 1250}, {}, {1200: 1250}, {}, {1200: 1250}]
    compsciSection1 = Course(days5, "csc1")
    days6 = [{1140: 1250}, {}, {}, {}, {}]
    physicsSection1 = Course(days6, "phy1")
    days7 = [{900: 950}, {}, {900: 950}, {}, {900: 950}]
    englishSection3 = Course(days7, "eng3")

    courses = [[compsciSection1], [mathSection1], [chemistrySection1],
               [englishSection1, englishSection2, englishSection3],
               [physicsSection1]]
    schedule = makeSchedule(courses)
    for course in schedule:
        print(course.name)


testMakeSchedule()
