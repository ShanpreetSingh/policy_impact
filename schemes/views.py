# schemes/views.py
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Policy Impact Visualizer API",
        "endpoints": {
            "/api/schemes": "List all schemes",
            "/admin": "Admin panel"
        }
    })

def scheme_list(request):
    # Temporary dummy data - we'll connect to DB later
    return JsonResponse({
        "schemes": ["Ujjwala", "PM-KISAN", "MGNREGA"],
        "status": "success"
    })