from django.urls import path

from thebook.core import views

app_name = "core"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
