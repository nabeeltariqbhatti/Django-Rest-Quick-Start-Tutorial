from rest_framework.response import Response

from .models import Category, Post
from django.contrib.auth.models import User
from blog.serializers import CategorySerializer, PostSerializer, UserSerializer

from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly



# class POSTList(APIView):
#     """
#     List all code Posts, or create a new Post.
#     """
#     def get(self,request,form=None):

#         posts = Post.objects.all()

#         serializer = PostSerializer(posts, many=True)

#         return Response(serializer.data)

#     def post(self,request,form=None):

#         serializer = PostSerializer(data=request.data,many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HHT_400_BAD_REQUEST)


# class PostDetail(APIView):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     def get_object(self,request,pk):
#         try:
#            post = Post.objects.get(pk=pk)

#         except Post.DoesNotExist:

#            return Response(status=status.HTTP_404_NOT_FOUND)

#     def get(self,request,pk,form=None):
#         post=self.get_object(pk=pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     def put(self,request,pk,form=None):
#         post=self.get_object(pk=pk)
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self,request,pk,form=None):
#         post=self.get_object(pk=pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT,)


class POSTList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)




class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
