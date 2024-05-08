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
    mint_pair = models.CharField(
        _("Token Mint Pair Address"), blank=True, null=True, max_length=65
    )

    # Alert Config
    alert_group_id = models.CharField(
        _("Telegram Group Id"), max_length=56, null=True, blank=True
    )
    send_alerts = models.BooleanField(default=False)
    is_buy_alerts_enabled = models.BooleanField(default=True)
    is_sell_alerts_enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Ping Bot")

    def __str__(self):
        return "Ping Bot Configuration"
