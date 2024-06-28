from django.urls import path

from thebook.members import views

app_name = "members"

urlpatterns = [
    path("all", views.members, name="all-members"),
    path("new", views.new_member, name="new-member"),
    path("export", views.export_members_list, name="export-members-list"),
]
