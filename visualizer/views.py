# visualizer/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import State, Scheme, PolicyData
import json

@csrf_exempt
@require_http_methods(["GET"])
def get_schemes(request):
    schemes = list(Scheme.objects.filter(is_active=True).values('id', 'name'))
    return JsonResponse({'schemes': schemes})

@csrf_exempt
@require_http_methods(["GET"])
def get_states(request):
    states = list(State.objects.values('code', 'name'))
    return JsonResponse({'states': states})

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def submit_data(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['state', 'scheme', 'year', 'beneficiaries']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Get related objects
        state = State.objects.get(code=data['state'])
        scheme = Scheme.objects.get(id=data['scheme'])
        
        # Create or update record
        record, created = PolicyData.objects.update_or_create(
            state=state,
            scheme=scheme,
            year=data['year'],
            defaults={
                'beneficiaries': data['beneficiaries'],
                'submitted_by': request.user
            }
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Data added successfully' if created else 'Data updated'
        })
        
    except State.DoesNotExist:
        return JsonResponse({'error': 'Invalid state code'}, status=400)
    except Scheme.DoesNotExist:
        return JsonResponse({'error': 'Invalid scheme ID'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def dashboard(request):
    return render(request, 'index.html')