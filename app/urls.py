from django.urls import path
from .views import RegisterUserAPIView, UserLoginAPIView, NoteList, NoteCreate, NoteDetail, ShareNoteView, NoteUpdate, NoteVersionHistoryAPIView

urlpatterns = [
  path('signup/',RegisterUserAPIView.as_view(), name='signup'),
  path('login/', UserLoginAPIView.as_view(), name='login'),
  path('notes/create/', NoteCreate.as_view(), name='note-create'),
  path('notes/', NoteList.as_view(), name='note-list'),
  path('notes/<int:id>/', NoteDetail.as_view(), name='note-detail'),
  path('notes/share', ShareNoteView.as_view(), name='share-notes'),
  path('notes/<int:pk>/update/', NoteUpdate.as_view(), name='note-update'),
  path('notes/version-history/<int:pk>/', NoteVersionHistoryAPIView.as_view()),
]