from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from partner_finder.models import Activity
from partner_finder.serializer import ActivitySerializer


class ActivityList(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (BasicAuthentication, )

    @staticmethod
    def get(request):
        if hasattr(request, 'activity'):
            activities = Activity.objects.filter(activity=request.activity)
            serializer = ActivitySerializer(activities, many=True)
            return JsonResponse(serializer.data, safe=False)
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return JsonResponse(serializer.data, safe=False)

    @staticmethod
    def post(request):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
