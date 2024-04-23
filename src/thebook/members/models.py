from django.db import models
from django.utils.functional import classproperty
from django.utils.translation import gettext as _


class Member(models.Model):
    number = models.CharField(
        max_length=100,
        verbose_name=_("Membership Number"),
        db_index=True,
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    email = models.EmailField(max_length=200, verbose_name=_("E-Mail"))

    def __str__(self):
        return self.name

    def current_membership(self):
        return self.memberships.first()


class FeeIntervals:
    MONTHLY = 1
    QUARTERLY = 3
    BIANNUAL = 6
    ANNUALLY = 12

    @classproperty
    def choices(cls):
        return (
            (cls.MONTHLY, _("Monthly")),
            (cls.QUARTERLY, _("Quarterly")),
            (cls.BIANNUAL, _("Biannually")),
            (cls.ANNUALLY, _("Annually")),
        )


class Membership(models.Model):
    member = models.ForeignKey(
        to="members.Member", on_delete=models.CASCADE, related_name="memberships"
    )
    start = models.DateField(verbose_name=_("start"))
    end = models.DateField(verbose_name=_("end"), null=True, blank=True)
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Membership Fee"),
        help_text=_("The amount to be paid in the chosen interval"),
    )
    interval = models.IntegerField(
        choices=FeeIntervals.choices,
        verbose_name=_("Payment Interval"),
        help_text=_("How often does the member pay their fees?"),
    )
