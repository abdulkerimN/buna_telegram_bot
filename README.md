# Buna Mini Bot 📚🌟

A simple Telegram study companion built with Python. Buna Mini Bot helps students stay motivated and improve their study habits through random study tips and motivational messages.

**Try the bot:** [@bunaet_bot](https://t.me/bunaet_bot)

![Buna Mini Bot](avatar.jpg)

## Features

- `/start` — Start the bot and display the main menu.
- `/help` — Show available commands and instructions.
- `/tip` — Receive a random study tip.
- `/motivate` — Receive a random motivational message.
- **Reply keyboard** — Easily access bot features using buttons.
- **Another button** — Get a different random tip or motivational message without sending a new command.

## Technologies Used

- Python
- python-telegram-bot
- python-dotenv

## Project Structure

```text
Telegram-Bot/
│
├── bot.py                  # Main bot application
├── messages.py             # Study tips and motivational messages
├── buna_bot_profile.jpg    # Bot profile picture
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── .gitignore              # Git ignored files
├── Procfile                # Process configuration
└── README.md               # Project documentation
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Telegram-Bot.git
cd Telegram-Bot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

For Git Bash on Windows:

```bash
source .venv/Scripts/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root directory:

```env
TOKEN=your_telegram_bot_token
BOT_USERNAME=@your_bot_username
```

Replace the placeholder values with your own bot credentials.

**Important:** Never share your bot token or commit your `.env` file to GitHub.

### 6. Run the bot

```bash
python bot.py
```

## Available Commands

| Command | Description |
|---|---|
| `/start` | Start the bot |
| `/help` | Display help information |
| `/tip` | Get a random study tip |
| `/motivate` | Get a motivational message |

## How It Works

Buna Mini Bot uses predefined lists of study tips and motivational messages stored in `messages.py`. Whenever a user requests a tip or motivation, Python randomly selects a message from the corresponding list.

The project does not require a database or AI API.

---

**Made with Python ❤️**