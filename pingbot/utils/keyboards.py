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


START_PRIVATE_KEYBOARD_BUTTONS = InlineKeyboardMarkup(
    create_keyboard_button(buttons=[
        InlineKeyboardButton("ℹ️ Add me to your group", url=f'https://t.me/{settings.BOT_USERNAME}?startgroup=start'),
        InlineKeyboardButton("Setup Token", callback_data="add_token#"),
    ])
)

def _get_redirect_user_to_private_chat(group_id):
    """ apppends the telegram id to inline button """
    #Purpose is to run some background checks on the user using this command
    print(group_id)
    return InlineKeyboardMarkup(
    create_keyboard_button(buttons=[
        InlineKeyboardButton("ℹ️ Click me!", url = f'https://t.me/{settings.BOT_USERNAME}?start={group_id}_public-group-admin-settings'),
        
    ])
)
