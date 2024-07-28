from django.http import JsonResponse
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def healthView(request):
    return JsonResponse({'success': True})
    

@api_view(['GET'])
def ReadinessView(request):
    return JsonResponse({'success': True})