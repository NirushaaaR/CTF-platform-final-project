from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings

import sqlite3

@require_POST
def get_sql_response(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    conn = sqlite3.connect(str(settings.BASE_DIR / 'sqli.db'))
    result = None
    try:
        cursor = conn.execute(f"SELECT username, password, quote, 1, 2, 3 FROM Users WHERE username='{username}' and password='{password}'")
        result = [{"username": row[0], "password": row[1], "quote": row[2]} for row in cursor]
    except Exception as e:
        result = "Error: "+str(e)
    finally:
        conn.close()

    return JsonResponse({"data": result})
