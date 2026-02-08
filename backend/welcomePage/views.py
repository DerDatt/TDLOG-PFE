from django.http import HttpResponse


def index(request):
    # return HttpResponse("This is the welcome page. It should show up if you enter the website without further information. ")
    return HttpResponse("""
        <h1>Willkommen!</h1>
        <ul>
            <li><a href='/appPFE/login/'>login page</a></li>
            <li><a href='/admin/'>admin</a></li>
        </ul>
    """)
