from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import MoodEntry
from .serializers import MoodEntrySerializer, UserSerializer
from django.contrib.auth.models import User

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MoodEntryList(APIView):
    def get(self, request):
        moods = MoodEntry.objects.all()
        serializer = MoodEntrySerializer(moods, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MoodEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MoodEntryDetail(APIView):
    def get(self, request, pk):
        mood = get_object_or_404(MoodEntry, pk=pk)
        serializer = MoodEntrySerializer(mood)
        return Response(serializer.data)

    def put(self, request, pk):
        mood = get_object_or_404(MoodEntry, pk=pk)
        serializer = MoodEntrySerializer(mood, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        mood = get_object_or_404(MoodEntry, pk=pk)
        mood.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
