from django.shortcuts import render

from thebook.members.models import Member


def members(request):
    members = Member.objects.order_by("name")

    return render(request, "members/members.html", context={"members": members})
