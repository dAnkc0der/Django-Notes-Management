from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, NotesSerializer, ShareNoteSerializer, NotesCreateSerializer, NotesUpdateSerializer, NoteVersionHistorySerializer
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Note
from django.db import models


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NoteCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Note.objects.all()
    serializer_class = NotesCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NoteList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotesSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(user=user)


class NoteDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotesSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

class ShareNoteView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShareNoteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shared_with_users = serializer.validated_data.get('shared_with_users', [])
        note_id = serializer.validated_data['note_id']

        try:
            note = Note.objects.get(id=note_id, user=request.user)
        except Note.DoesNotExist:
            return Response({'detail': 'Note not found'}, status=404)

        note.shared_with.add(*shared_with_users)
        return Response({'detail': 'Note shared successfully'}, status=201)
    

class NoteUpdate(generics.UpdateAPIView):
    serializer_class = NotesUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(models.Q(user=user) | models.Q(shared_with=user)).distinct()

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

class NoteVersionHistoryAPIView(generics.RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteVersionHistorySerializer

    def get(self, request, *args, **kwargs):
        note_id = self.kwargs.get('id')
        note = self.get_object()
        
        # Retrieve the historical versions of the note
        historical_versions = note.history.all()

        version_history = [{
            'timestamp': version.history_date,
            'user': version.history_user.username if version.history_user else 'Anonymous',
            'changes': {
                'title': version.title,
                'content': version.content
            }
        } for version in historical_versions]

        return Response(version_history)


    
