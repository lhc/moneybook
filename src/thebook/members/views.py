from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from thebook.members.forms import NewMemberForm
from thebook.members.models import Member, Membership


def members(request):
    members = Member.objects.order_by("name")

    return render(request, "members/members.html", context={"members": members})


def new_member(request):
    if request.method == "POST":
        form = NewMemberForm(request.POST)
        if form.is_valid():
            member = Member(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                has_key=form.cleaned_data["has_key"],
                phone_number=form.cleaned_data["phone_number"],
            )
            member.save()

            membership = Membership(
                member=member,
                start=form.cleaned_data["start"],
                amount=form.cleaned_data["amount"],
                interval=form.cleaned_data["interval"],
            )
            membership.save()

            return HttpResponseRedirect(reverse("members:all-members"))
    else:
        form = NewMemberForm()

    return render(request, "members/new_member.html", {"form": form})
