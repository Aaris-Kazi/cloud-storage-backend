from django.urls import path

from health_app import views

urlpatterns = [
    path('health/', view=views.healthView),
    path('readiness/', view=views.ReadinessView),
]
