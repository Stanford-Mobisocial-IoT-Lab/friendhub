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


class MatchList(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (BasicAuthentication, )

    @staticmethod
    def get(request):
        activities = Activity.objects.all()
        matches = []
        for a1 in activities:
            for a2 in activities:
                if a1.email != a2.email and a1.activity == a2.activity:
                    max_start_time = max(a1.start_time, a2.start_time)
                    min_end_time = min(a1.end_time, a2.end_time)
                    message = 'A match is found for %s: \n %s (%s) from %s to %s' % (a1.activity, a2.organizer, a2.email, max_start_time, min_end_time)
                    if max_start_time < min_end_time:
                        matches.append({
                            'activity': a1.activity,
                            'email': a1.email,
                            'match_organizer': a2.organizer,
                            'match_email': a2.email,
                            'start_time': max_start_time,
                            'end_time': min_end_time,
                            'message': message
                        })
        return JsonResponse(matches, safe=False)

