from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from pingbot.utils.decorators import check_owner
from pingbot.resources.models import PingBot


@check_owner
async def check_token_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ping = await PingBot.objects.aget(pk=1)
    token_exist = ping.token_mint == None
    query = update.callback_query
    if token_exist:
        return await query.edit_message_text(
            "No token found, add new token using '/start'"
        )

    keyboard_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"Minimum Buy: {ping.min_alert_amount}",
                    callback_data="set_minimum_buy#",
                )
            ],
            [
                InlineKeyboardButton(
                    f"Group Id: {'Not Set' if ping.alert_group_id == None else ping.alert_group_id }", callback_data="set_group#"
                )
            ],
            [
                InlineKeyboardButton(
                    f"Paused: {"✅" if ping.paused else "🚫"}", callback_data="set_maintenace#"
                )
            ],
            [
                InlineKeyboardButton(
                    f"Buy Alert Enabled: {"✅" if ping.is_buy_alerts_enabled else "🚫"}",
                    callback_data="enable_buy_alert#",
                )
            ],
            [
                InlineKeyboardButton(
                    f"Sell Alert Enabled: {"✅" if ping.is_sell_alerts_enabled else "🚫"}",
                    callback_data="enable_sell_alert#",
                )
            ],
           
            [
                InlineKeyboardButton(
                    f"Sell Emoji: {ping.emoji}",
                    callback_data="set_emoji",
                )
            ],
            [InlineKeyboardButton("❌ Delete Mint", callback_data="delete_mint#")],
            [InlineKeyboardButton("Close", callback_data="close_admin#")],
        ]
    )
    msg = (
        f"Current\n"
        f"↱ {ping.mint_name} ({ping.mint_symbol})\n\n"
        f"∴ <code>{ping.token_mint} </code>\n\n"
        f"↳ AMM ID: <code>{ping.mint_pair}</code>"
    )
    return await query.edit_message_text(
        msg, reply_markup=keyboard_buttons, parse_mode=ParseMode.HTML
    )
