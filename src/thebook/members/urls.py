from django.urls import path

from thebook.members import views

app_name = "members"

urlpatterns = [
    path("all", views.members, name="all-members"),
]
