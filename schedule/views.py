from django.shortcuts import render
from bs4 import BeautifulSoup as bs
import requests

# Views
def schedule(request):
    # Necessary variables to be displayed
    context = {
        # Get BM Class Schedule JSON
        'schedule': requests.get('https://binusmaya.binus.ac.id/services/ci/index.php/student/class_schedule/classScheduleGetStudentClassSchedule',
                                   header={'Referer': 'https://binusmaya.binus.ac.id/newStudent/'},
                                   cookie=request.session.get('session_cookie')).json(),
        'name': request.session.get('name', 'Name').title(),
        'major': request.session.get('major', 'Major'),
        'student_id': request.session.get('student_id', 'Student ID'),
    }
    return render(request, 'schedule/schedule.html', context)