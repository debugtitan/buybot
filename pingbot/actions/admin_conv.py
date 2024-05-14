
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
from pingbot.resources.models import PingBot
from pingbot.utils.helpers import PingProcessStarter


process = PingProcessStarter()

MINIMUM_BUY, GROUP_ID, MAINTENANCE, BUY_ALERT_ENABLE, SELL_ALERT_ENABLE, EMOJI = range(
    6
)


back_button = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Continue ⋙", callback_data="token_settings#")],
        [InlineKeyboardButton("Cancel ©", callback_data="close_admin#")],
    ]
)


async def remove_mint_from_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ping = await PingBot.objects.aget(pk=1)
    ping.token_mint = None
    await ping.asave()
    await query.edit_message_text("Token removed!!")
    return ConversationHandler.END


async def close_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await update.callback_query.edit_message_text("Panel Closed!!")
    return ConversationHandler.END


async def _minimum_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Send new minimum amount for alerts, e.g 100")
    return MINIMUM_BUY


async def minimum_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ping = await PingBot.objects.aget(pk=1)
    ping.min_alert_amount = update.message.text
    await ping.asave()
    await update.message.reply_text("Minimum alert set ", reply_markup=back_button)


async def _group_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Send new group id")
    return GROUP_ID


async def group_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ping = await PingBot.objects.aget(pk=1)
    ping.alert_group_id = update.message.text
    await ping.asave()
    await update.message.reply_text("Group Id set", reply_markup=back_button)


async def _maintenace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keys = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Yes", callback_data=f"pause_settings#yes")],
            [InlineKeyboardButton("No ©", callback_data="pause_settings#no")],
        ]
    )
    await query.edit_message_text("Pause token alert?", reply_markup=keys)
    return MAINTENANCE


async def maintenance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    maintenance_enable = query.data.split("#")[1] == "yes"
    ping = await PingBot.objects.aget(pk=1)
    ping.paused = maintenance_enable
    await ping.asave()
    process.stop() if maintenance_enable else process.run()
    await query.edit_message_text("Maintenance set", reply_markup=back_button)


async def _buy_alert_enable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keys = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Yes", callback_data="buy_alert_settings#yes")],
            [InlineKeyboardButton("No ©", callback_data="buy_alert_settings#no")],
        ]
    )
    await query.edit_message_text("Pause buy alert?", reply_markup=keys)
    return BUY_ALERT_ENABLE


async def buy_alert_enable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    alert_enable = query.data.split("#")[1] == "yes"
    ping = await PingBot.objects.aget(pk=1)
    ping.is_buy_alerts_enabled = alert_enable
    await ping.asave()
    await query.edit_message_text("Buy alert  set", reply_markup=back_button)


async def _sell_alert_enable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keys = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Yes", callback_data="sell_alert_settings#yes")],
            [InlineKeyboardButton("No ©", callback_data="sell_alert_settings#no")],
        ]
    )
    await query.edit_message_text("Pause sell alert?", reply_markup=keys)
    return SELL_ALERT_ENABLE


async def sell_alert_enable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ping = await PingBot.objects.aget(pk=1)
    query = update.callback_query
    await query.answer()
    await query.answer()
    alert_enable = query.data.split("#")[1] == "yes"
    ping.is_sell_alerts_enabled = alert_enable
    await ping.asave()
    await query.edit_message_text("Sell alerts set", reply_markup=back_button)


async def _emoji_handlers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Send new emoji")
    return EMOJI


async def emoji_handlers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ping = await PingBot.objects.aget(pk=1)
    ping.emoji = update.message.text
    await ping.asave()
    await update.message.reply_text("Emoji set", reply_markup=back_button)


admin_conv_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(_minimum_buy, pattern="set_minimum_buy#"),
        CallbackQueryHandler(_group_id, pattern="set_group#"),
        CallbackQueryHandler(_maintenace, pattern="set_maintenace#"),
        CallbackQueryHandler(_buy_alert_enable, pattern="enable_buy_alert#"),
        CallbackQueryHandler(_sell_alert_enable, pattern="enable_sell_alert#"),
        CallbackQueryHandler(_emoji_handlers, pattern="set_emoji"),
    ],
    states={
        MINIMUM_BUY: [MessageHandler(filters.TEXT, minimum_buy)],
        GROUP_ID: [MessageHandler(filters.TEXT, group_id)],
        MAINTENANCE: [CallbackQueryHandler(maintenance, pattern="pause_settings#")],
        BUY_ALERT_ENABLE: [
            CallbackQueryHandler(buy_alert_enable, pattern="buy_alert_settings#")
        ],
        SELL_ALERT_ENABLE: [
            CallbackQueryHandler(sell_alert_enable, pattern="sell_alert_settings#")
        ],
        EMOJI: [MessageHandler(filters.TEXT, emoji_handlers)],
    },
    fallbacks=[
        CallbackQueryHandler(close_admin_panel, pattern="close_admin#")
    ],
)
