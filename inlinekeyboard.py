import logging

from telegram import __version__ as TG_VER, ReplyKeyboardRemove

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Stages
# START_ROUTES, END_ROUTES = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)
PHOTO, LOCATION, BIO = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User first_name %s started the conversation.", user)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Yes, I have", callback_data=str(ONE)),
            InlineKeyboardButton("No, I`m baying", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("Do you have somthing to sell? ", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return PHOTO


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)
    return PHOTO


def photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_foto.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_foto.jpg')
    update.message.reply_text("perfect . almost complete, Now please send me your "
                              "location, '' or send /skip if you dom`t")
    return LOCATION


def skip_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s: did not send a photo", user.first_name)
    update.message.reply_text("Ok, no problem! Now send me your location please, ' ' or send /skip.")
    return LOCATION


def location(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f ", user.first_name, user_location.latitude, user_location.longitude)
    update.message.reply_text("Okm we will take it in consideration a notify ")
    return BIO


def bio(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("review by %s: %s ", user.first_name, update.message.text)
    update.message.reply_text("Thank you! We will call you soon!")
    return ConversationHandler.END


def cansel(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User %s: cansel the conversation", user.first_name)
    update.message.reply_text("reach as back you ", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END



