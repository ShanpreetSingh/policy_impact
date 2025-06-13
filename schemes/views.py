from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.core.exceptions import ValidationError
from django.db.models import Sum
from .models import Scheme, State, SchemeData
import json
from django.db.models import Sum, Count
from django.shortcuts import render

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
    
@require_http_methods(["GET"])
def map_view(request):
    """Render the interactive map template"""
    return render(request, 'map.html')

@require_http_methods(["GET"])
def state_geo_data(request):
    """API endpoint for geographic visualization data"""
    try:
        # Indian state coordinates (approximate)
        state_coords = {
            'AP': (17.6868, 83.2185), 'AR': (27.1004, 93.6167), 'AS': (26.2006, 92.9376),
            'BR': (25.0961, 85.3131), 'CT': (21.2787, 81.8661), 'GA': (15.2993, 74.1240),
            'GJ': (22.2587, 71.1924), 'HR': (29.0588, 76.0856), 'HP': (31.1048, 77.1734),
            'JH': (23.6102, 85.2799), 'KA': (15.3173, 75.7139), 'KL': (10.8505, 76.2711),
            'MP': (22.9734, 78.6569), 'MH': (19.7515, 75.7139), 'MN': (24.6637, 93.9063),
            'ML': (25.4670, 91.3662), 'MZ': (23.1645, 92.9376), 'NL': (25.7999, 93.9511),
            'OR': (20.9517, 85.0985), 'PB': (31.1471, 75.3412), 'RJ': (27.0238, 74.2179),
            'SK': (27.3333, 88.6167), 'TN': (11.1271, 78.6569), 'TG': (18.1124, 79.0193),
            'TR': (23.9408, 91.9882), 'UP': (26.8467, 80.9462), 'UT': (30.0668, 79.0193),
            'WB': (22.9868, 87.8550)
        }

        # Get all states with their data
        states = State.objects.annotate(
           total_beneficiaries=Sum('scheme_data__beneficiaries'),  
           schemes_count=Count('scheme_data__scheme', distinct=True) 
        )

        # Build GeoJSON response
        features = []
        for state in states:
            if state.code in state_coords:
                lat, lon = state_coords[state.code]
                features.append({
                    "type": "Feature",
                    "properties": {
                        "name": state.name,
                        "code": state.code,
                        "beneficiaries": state.total_beneficiaries or 0,
                        "schemes_count": state.schemes_count or 0
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    }
                })

        return JsonResponse({
            "type": "FeatureCollection",
            "features": features
        }, safe=False)
    
    except Exception as e:
        return JsonResponse(
            {'error': 'Failed to generate geographic data', 'details': str(e)},
            status=500
        )

@require_http_methods(["GET"])
def state_boundaries(request):
    """Optional: API for detailed state boundaries (GeoJSON)"""
    try:
        # This would return actual GeoJSON boundaries if you have them
        # For now returning empty - you can add real boundaries later
        return JsonResponse({
            "type": "FeatureCollection",
            "features": []
        }, safe=False)
    
    except Exception as e:
        return JsonResponse(
            {'error': 'Boundary data not available', 'details': str(e)},
            status=501  # Not Implemented
        )