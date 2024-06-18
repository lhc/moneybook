from django.contrib import admin

from thebook.members.models import Member, Membership


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "has_key",
    )


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "start",
        "amount",
        "interval",
    )
