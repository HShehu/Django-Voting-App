from django.urls import path
from . import views

app_name = 'VotingApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:poll_id>/add/', views.contestant_view, name='add'),
    path('<int:poll_id>/', views.detail, name='detail'),
    path('<int:poll_id>/results/', views.results, name='results'),
    path('<int:poll_id>/vote/', views.vote, name='vote'),
    path('<str:obj>/resultsdata/', views.resultsData, name='resultsData'),
]
