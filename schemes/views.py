from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.core.exceptions import ValidationError
from django.db.models import Sum
from .models import Scheme, State, SchemeData
import json

@require_http_methods(["GET"])
def scheme_list(request):
    """Get aggregated scheme data across all states"""
    try:
        # Get aggregated data by scheme and state
        data = list(SchemeData.objects.values(
            'scheme__name',
            'state__name',
            'state__code'
        ).annotate(
            beneficiaries=Sum('beneficiaries')
        ).order_by('scheme__name', 'state__name'))
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return JsonResponse(
            {'error': 'Failed to fetch scheme data', 'details': str(e)},
            status=500
        )

@require_http_methods(["GET"])
@never_cache
def state_impact(request, state_code):
    """Get scheme data for a specific state"""
    try:
        # Get aggregated data for the state
        data = list(SchemeData.objects.filter(state__code=state_code)
                   .values('scheme__name')
                   .annotate(beneficiaries=Sum('beneficiaries'))
                   .order_by('scheme__name'))
        
        if not data:
            return JsonResponse(
                {'error': f'No data found for state {state_code}'},
                status=404
            )
            
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return JsonResponse(
            {'error': 'Failed to fetch state data', 'details': str(e)},
            status=500
        )

@require_http_methods(["GET"])
def state_list(request):
    """Get list of all available states"""
    try:
        states = list(State.objects.all()
                     .values('code', 'name')
                     .order_by('name'))
        return JsonResponse(states, safe=False)
    except Exception as e:
        return JsonResponse(
            {'error': 'Failed to fetch states', 'details': str(e)},
            status=500
        )

@require_http_methods(["GET"])
def state_history(request, state_code):
    """Get historical data for a specific state"""
    try:
        # Get yearly data grouped by scheme and year
        data = list(SchemeData.objects.filter(state__code=state_code)
                   .values('scheme__name', 'year')
                   .annotate(beneficiaries=Sum('beneficiaries'))
                   .order_by('scheme__name', 'year'))
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return JsonResponse(
            {'error': 'Failed to fetch historical data', 'details': str(e)},
            status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def add_data(request):
    """Handle form submission for new data"""
    try:
        # Parse and validate request data
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['state', 'scheme', 'year', 'beneficiaries']
        if not all(field in data for field in required_fields):
            return JsonResponse(
                {'error': 'Missing required fields'},
                status=400
            )
        
        # Get related objects
        try:
            state = State.objects.get(code=data['state'])
            scheme = Scheme.objects.get(name=data['scheme'])
        except (State.DoesNotExist, Scheme.DoesNotExist) as e:
            return JsonResponse(
                {'error': 'Invalid state or scheme'},
                status=400
            )
        
        # Create new record
        record = SchemeData(
            state=state,
            scheme=scheme,
            year=data['year'],
            beneficiaries=data['beneficiaries']
        )
        
        # Full clean validation
        record.full_clean()
        record.save()
        
        return JsonResponse(
            {'success': 'Data added successfully'},
            status=201
        )
        
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON data'},
            status=400
        )
    except ValidationError as e:
        return JsonResponse(
            {'error': 'Validation failed', 'details': dict(e)},
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {'error': 'Failed to add data', 'details': str(e)},
            status=500
        )