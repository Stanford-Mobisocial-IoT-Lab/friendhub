from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from sticky_notes.models import Post
from sticky_notes.serializer import StickyNotesSerializer


class PostList(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (BasicAuthentication, )

    @staticmethod
    def get(request):
        posts = Post.objects.all()
        serializer = StickyNotesSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    @staticmethod
    def post(request):
        serializer = StickyNotesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
