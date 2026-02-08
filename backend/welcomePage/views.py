from django.http import HttpResponse


def index(request):
    return HttpResponse("""
        <h1>Welcome!</h1>
        <ul>
            <li><a href='/appPFE/login/'>login page</a></li>
            <li><a href='/admin/'>admin</a></li>
        </ul>
    """)
