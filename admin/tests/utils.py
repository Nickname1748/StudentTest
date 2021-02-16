'''
This module contains functions for testing
'''

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from study_base.models import StudentGroup

test_credentials = {
    'username':'testuser',
    'password':'testpassword'
}

admin_credentials = {
    'username':'admin',
    'password':'rootpassword'
}

teacher_credentials = {
    'username':'teacher',
    'password':'teacherpassword'
}

students_credentials = [
    {'username':'student1', 'password':'studentpassword'},
    {'username':'student2', 'password':'studentpassword'}
]

def create_test_user():
    '''
    Creates test user
    '''
    user = get_user_model().objects.create_user(
        **test_credentials,
        email = 'test@example.com',
        first_name = 'Name',
        last_name = 'Surname'
    )
    return user

def create_admin_user():
    '''
    Creates admin user
    '''
    admin = get_user_model().objects.create_user(
        **admin_credentials,
        email = 'adminemail@example.com',
        first_name = 'AdminName',
        last_name = 'AdminSurname'
    )
    admin.is_staff = True
    admin.save()
    return admin

def create_teacher_user():
    '''
    Creates teacher user
    '''
    teacher = get_user_model().objects.create_user(
        **teacher_credentials,
        email = 'teacheremail@example.com',
        first_name = 'TeacherName',
        last_name = 'TeacherSurname'
    )

    teacher_group = Group.objects.get_or_create(name = "Teacher")[0]
    teacher.groups.add(teacher_group)
    return teacher

def create_student_users():
    '''
    Creates 2 students users
    '''
    students = []
    for index, credential in enumerate(students_credentials):
        students.append(
            get_user_model().objects.create_user(
                **credential,
                email = f'student{index+1}email@example.com',
                first_name = f'Student{index + 1}Name',
                last_name = f'Student{index + 1}Surname'
            )
        )
    group = Group.objects.get_or_create(name = 'Student')[0]
    for student in students:
        student.groups.add(group)
    return students

def create_student_group():
    '''
    Creates student group
    '''
    teacher = create_teacher_user()
    students = create_student_users()
    student_group = StudentGroup.objects.create(
        name = 'Test Group',
        teacher = teacher
    )
    student_group.students.set(students)
    student_group.save()
    return student_group
