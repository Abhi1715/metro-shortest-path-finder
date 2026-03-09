from django.urls import path
from .views import StationListView, ShortestPathView

urlpatterns = [
    path('stations/', StationListView.as_view(), name='station-list'),
    path('shortest-path/', ShortestPathView.as_view(), name='shortest-path'),
]
