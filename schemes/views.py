from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, 'index.html')

def scheme_list(request):
    return JsonResponse({
        "schemes": ["Ujjwala", "PM-KISAN", "MGNREGA"],
        "status": "success"
    })