from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from bbs.models import Post
from bbs.serializer import BbsSerializer


class PostList(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (BasicAuthentication, )

    @staticmethod
    def get(request):
        posts = Post.objects.all()
        serializer = BbsSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    @staticmethod
    def post(request):
        request.data['author'] = request.user.id
        serializer = BbsSerializer(data=request.data)
        if serializer.is_valid():
            Post.objects.create(
                post=request.data['post'],
                author=request.user
            )
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



