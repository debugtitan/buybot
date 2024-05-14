from django.conf import settings
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


# Create Keyboard Buttons
def create_keyboard_button(
    buttons, buttons_per_column=1, button_header=None, button_footer=None
):
    menu = [
        buttons[i : i + buttons_per_column]
        for i in range(0, len(buttons), buttons_per_column)
    ]

    if button_header:
        menu.insert(0, [button_header])
    if button_footer:
        menu.append([_button for _button in button_footer])
    return menu


TOKEN_KEYBOARD_BUTTONS = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Add New Token",callback_data="add_token#")],
        [InlineKeyboardButton("Change Token Settings", callback_data="token_settings#")]
    ]
)

