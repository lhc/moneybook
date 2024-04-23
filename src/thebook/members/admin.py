from django.contrib import admin

from thebook.members.models import Member, Membership


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin): ...


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin): ...
