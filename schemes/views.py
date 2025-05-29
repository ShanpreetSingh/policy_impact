from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from .models import Scheme, State, SchemeData

def scheme_list(request):
    data = list(SchemeData.objects.select_related('scheme', 'state').values(
        'scheme__name',
        'state__name',
        'state__code',
        'year',
        'beneficiaries'
    ))
    return JsonResponse(data, safe=False)

@never_cache
def state_impact(request, state_code):
    data = list(SchemeData.objects.filter(state__code=state_code)
               .select_related('scheme')
               .values('scheme__name', 'beneficiaries'))
    return JsonResponse(data, safe=False)

def state_list(request):
    states = list(State.objects.all().values('code', 'name').order_by('name'))
    return JsonResponse(states, safe=False)