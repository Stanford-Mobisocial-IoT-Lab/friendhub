from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from bbs.models import Post
from bbs.serializer import BbsSerializer


# Create your views here.
def index(request):
    return HttpResponse("hello")


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def list_posts(request):
    if request.method == 'GET':
        post = Post.objects.all()
        serializer = BbsSerializer(post, many=True)
        return JsonResponse(serializer.data, safe=False)


