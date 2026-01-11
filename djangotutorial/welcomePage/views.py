from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # return HttpResponse("This is the welcome page. It should show up if you enter the website without further information. ")
    return HttpResponse("""
        <h1>Willkommen!</h1>
        <ul>
            <li><a href='/welcome/'>WelcomeApp</a></li>
            <li><a href='/polls/'>Polls</a></li>
            <li><a href='/appPFE/'>AppPFE (You shouldn't be able to access this directly withoud login)</a></li>
            <li><a href='/accounts/'>To the login page. </a></li>
            <li><a href='/admin/'>admin</a></li>
        </ul>
    """)