import logging
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import config  


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# command handler functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Welcome to m_cube_bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("""
        The following commands are available:
        /start -> Welcome to the m_cube_bot
        /help -> This message
        /music  -> Suggest Music
        /movie -> Suggest Movie
        /contact -> Contact information
    """)

# suggest music
async def music(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={config.LASTFM_API_KEY}&format=json"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and 'tracks' in data:
        tracks = data['tracks']['track']
        random_track = random.choice(tracks)
        track_name = random_track['name']
        artist_name = random_track['artist']['name']
        await update.message.reply_text(f"How about listening to '{track_name}' by '{artist_name}'?")
    else:
        await update.message.reply_text("Sorry, I couldn't fetch music suggestions right now.")

#movie suggest
async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = f"http://www.omdbapi.com/?s=movie&apikey={config.OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and 'Search' in data:
        movies = data['Search']
        random_movie = random.choice(movies)
        movie_title = random_movie['Title']
        await update.message.reply_text(f"How about watching '{movie_title}'?")
    else:
        await update.message.reply_text("Sorry, I couldn't fetch movie suggestions right now.")


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You can contact us at minphonethitcs001@gmail.com")

#main
def main() -> None:
   
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    # command handlers to application
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("music", music))
    application.add_handler(CommandHandler("movie", movie))
    application.add_handler(CommandHandler("contact", contact))

    # Start bot
    application.run_polling()

if __name__ == '__main__':
    main()
