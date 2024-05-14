from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel
from pingbot.utils.base import BaseModelMixin


class PingBot(BaseModelMixin, SingletonModel):
    """default configuration for pingbot model"""

    owner = models.CharField(
        _("Bot Owner"),
        editable=False,
        max_length=255,
        default=settings.SUPER_ADMIN,
    )

    token_mint = models.CharField(
        _("Token Mint Address"), blank=True, null=True, max_length=65
    )
    mint_name = models.CharField(_("Mint Name"), null=True, blank=True, max_length=65)
    mint_symbol = models.CharField(
        _("Mint Symbol"), null=True, blank=True, max_length=65
    )
    mint_supply = models.IntegerField(
        _("Mint Supply"),
        null=True,
        blank=True,
    )
    mint_pair = models.CharField(
        _("Token Mint Pair Address"), blank=True, null=True, max_length=65
    )

    # Alert Config
    alert_group_id = models.CharField(
        _("Telegram Group Id"), max_length=56, null=True, blank=True
    )
    paused = models.BooleanField(default=True)
    is_buy_alerts_enabled = models.BooleanField(default=True)
    is_sell_alerts_enabled = models.BooleanField(default=True)
    min_alert_amount = models.PositiveIntegerField(
        _("Minimum Alert Amount"),
        help_text=_(
            "Minimum threshold amount before bot send notication, default is $10"
        ),
        default=10,
    )
    emoji = models.CharField(
        _("Emoji"),
        help_text="emoji to display on alerts",
        default="🔮",
        max_length=1,
    )
    pid = models.IntegerField(_("Process Id"), default=0)

    class Meta:
        verbose_name = _("Ping Bot")

    def __str__(self):
        return "Ping Bot Configuration"
