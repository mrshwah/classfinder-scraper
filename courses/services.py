from courses.models import Course


class RequestedCourse:
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return 'Title = {}, Rank = {}'.format(self.title, self.rank)


class CourseTree:
    def __init__(self, course):
        self.course = course
        self.children = []

    def add(self, courses):
        self.children.append(courses)


# # just compare two sections
# def sections_conflict(section1, section2):
#     for time1 in section1.room_day_and_time.all():     # iterate through all meeting times for this section.
#         for time2 in section2.room_day_and_time.all():
#             if time1.begin >= time2.begin and time1.begin <= time2.end:   # starts during another course
#                 #print("conflict: section1 (",section1,") starts during section2 (",section2,")")
#                 return True
#             if time1.end >= time2.begin and time1.end <= time2.end:   # ends during another course
#                 #print("conflict: section1 (",section1,") ends during section2 (",section2,")")
#                 return True
#             if time1.begin <= time2.begin and time1.end >= time2.end:   # spans across another course
#                 #print("conflict: section1 (",section1,") spans section2 (",section2,")")
#                 return True
#     return False
#
#
# # this checks one complete schedule for any conflicts -- this is a LOT of comparisons
# # for N courses, this is ~O(N^2) i.e. slow.   Gotta be a better way!
# def any_conflicts(schedule):
#     for i in range(len(schedule)-1):
#         for j in range(i+1,len(schedule)):
#             if sections_conflict(schedule[i], schedule[j]):
#                 return True
#     return False
#
# # this is the counter for keeping track of all the various course combinations for schedules
# #     Here we pay no attention to conflicts
# #   Note: course_indices is passed by reference so it gets modified IN PLACE.
# def increment_indices(course_indices, courses_desired):
#     # arbitrary choice: we're going to follow "big-endian" notation, so the first course gets incremented the most
#     course_indices[0] += 1
#     for j in range(len(course_indices)-1):
#         if (course_indices[j] > len(courses_desired[j])-1):  # if we exceed max index for that course
#             course_indices[j] = 0
#             course_indices[j+1] +=1
#     return
#
# def create_schedule(requested_courses):
#     #print("requested courses = ",requested_courses)
#     n_courses = len(requested_courses)
#     courses_desired = [list(Course.objects.filter(title=course.title)) for course in requested_courses]
#     #print("courses_desired = ", courses_desired," len(courses_desired) = ",len(courses_desired))
#
#     course_indices = [0]*n_courses     # we are literally going to make an integer counter for each course to keep track of all combos
#
#     # also, let's see exactly how big of a job we're going to be doing...
#     n_combos = 1
#     for i in range(n_courses):
#         n_combos *=  len(courses_desired[i])
#     #print(" n_combos = ",n_combos)
#
#     for i_combo in range(n_combos):    # generate all possible schedules
#         schedule = []
#         #print("course_indices = ",course_indices)
#         for j in range(n_courses):     # go along list of courses
#             schedule.append( courses_desired[j][ course_indices[j] ] )
#         # previous loop just generated one complete schedule
#         #print("i_combo = ",i_combo,", schedule = ",schedule)
#
#         if not any_conflicts(schedule):       # check for any conflicts in this schedule
#             #print("     WE HAVE A WINNER!")
#             return schedule          # TODO: for now, we just return the first complete schedule
#         increment_indices(course_indices, courses_desired)  # end of loop. advance to next course combination
#
#     return schedule      # return whatever's left.  (worst case)


def create_tree(tree, possible_courses):
    if 0 == len(possible_courses):
        return tree

    for section in possible_courses[0]:
        section_tree = CourseTree(section)
        section_tree = create_tree(section_tree, possible_courses[1:])
        tree.add(section_tree)
    return tree


def build_schedules(node):
    if len(node.children) == 0:
        return [node.course]
    all_schedules = []
    for child in node.children:
        sub_schedules = build_schedules(child)
        if node.course == 'Top':
            return sub_schedules
        if not sub_schedules:
            continue
        if type(sub_schedules[0]) == Course:
            if check_conflicts(sub_schedules[0], node.course):
                sub_schedules.append(node.course)
            else:
                continue
            all_schedules.append(sub_schedules)
        else:
            for schedule in sub_schedules:
                fits = False
                for course in schedule:
                    if not check_conflicts(course, node.course):
                        break
                    fits = True
                if fits:
                    schedule.append(node.course)
                else:
                    continue
            all_schedules += sub_schedules
    return all_schedules


def check_conflicts(course_1, course_2):
    '''
    Checks for course conflicts. If there are none, returns True.
    :param course_1:
    :param course_2:
    :return:
    '''
    section_fits = True
    for time_1 in course_1.room_day_and_time.all():
        # check if course begins during existing course
        for time_2 in course_2.room_day_and_time.all():
            if time_1.day != time_2.day:
                break
            if time_1.begin <= time_2.begin and time_1.end >= time_2.end:
                section_fits = False
                break
            if time_1.begin <= time_2.end and time_1.end >= time_2.end:
                section_fits = False
                break
    return section_fits

def create_schedule(requested_courses):
    for course in requested_courses:
        print(course.title)
        print(len(Course.objects.filter(title=course.title)))
    possible_courses = [list(Course.objects.filter(title=course.title)) for course in requested_courses]

    course_tree = CourseTree('Top')
    course_tree = create_tree(course_tree, possible_courses)

    schedules = build_schedules(course_tree)
    schedules = list(filter(lambda x: len(x) == len(requested_courses), schedules))
    return schedules[0]
    '''
    for course in possible_courses:  # Iterate through different courses
        for section in course:  # Iterate through individual sections of each course
            section_fits = True
            for existing in course_schedule:  # Iterate through the current schedule, what we have so far
                for time in existing.room_day_and_time.all():
                    # check if course begins during existing course
                    for section_time in section.room_day_and_time.all():
                        if time.day != section_time.day:
                            break
                        if time.begin <= section_time.begin and time.end >= section_time.end:
                            section_fits = False
                            break
                        if time.begin <= section_time.end and time.end >= section_time.end:
                            section_fits = False
                            break

            if section_fits:
                course_schedule.append(section)  # if we make it through every course in our schedule
                break  # with no conflicts, add it to schedule and move to next

    return course_schedule
    '''
