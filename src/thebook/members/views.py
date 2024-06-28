import csv

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from thebook.members.forms import NewMemberForm
from thebook.members.models import Member, Membership


def export_members_list(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="members-list.csv"'},
    )

    writer = csv.writer(response)

    writer.writerow(
        [
            "id",
            "name",
            "email",
            "has_key",
            "phone_number",
            "start_membership",
            "fee_amount",
            "fee_interval",
        ]
    )
    for member in Member.objects.all():
        membership = member.current_membership()

        start_membership = membership.start if membership is not None else ""
        fee_amount = membership.amount if membership is not None else ""
        fee_interval = (
            membership.get_interval_display() if membership is not None else ""
        )

        writer.writerow(
            [
                member.id,
                member.name,
                member.email,
                member.has_key,
                member.phone_number,
                start_membership,
                fee_amount,
                fee_interval,
            ]
        )

    return response


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
