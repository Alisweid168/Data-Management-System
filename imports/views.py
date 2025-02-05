from django.shortcuts import render
from django.http import JsonResponse
import os
from django.conf import settings
from .tasks import import_customers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        print(file_path)
        import_customers(file_path)  

        return JsonResponse({"message": "File uploaded successfully. Import in progress."})

    return JsonResponse({"error": "No file provided"}, status=400)
