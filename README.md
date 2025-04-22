# News Aggregator Bot

A Telegram bot that fetches news articles from NewsAPI, summarizes them using LlamaIndex’s `SummaryIndex`, and delivers summaries to a Telegram group chat or channel. Users can tag the bot with keywords (e.g., `@NewsBot tech startups`) to request custom news summaries, and the bot automatically posts hourly breaking business news updates to a specified Telegram channel. The program operates entirely in-memory, with no disk storage.

## Features
- **User-Triggered Queries**: Tag the bot in any Telegram chat (group or private) with keywords (e.g., `@NewsBot tech startups`) to receive a summarized newsletter.
- **In-Memory Processing**: Processes articles and indexes without saving to disk, ensuring lightweight operation.
- **Modular Design**: Organized into `main`, `collector`, `aggregator`, and `bot` modules for maintainability.

## Prerequisites
- **Python 3.8+**: Ensure Python is installed.
- **NewsAPI Account**: Obtain an API key from [newsapi.org](https://newsapi.org/) (free tier available).
- **OpenAI Account**: Get an API key for LlamaIndex’s summarization (uses `gpt-3.5-turbo`).
- **Telegram Bot**: Create a bot via [BotFather](https://t.me/BotFather) to get a bot token.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd news-aggregator
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root:
   ```
   NEWSAPI_KEY=your_newsapi_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHANNEL_ID=@YourChannelName
   ```

## Usage
1. **Run the Program**:
   ```bash
   python src/main.py
   ```

2. **Interact with the Bot**:
   - In a Telegram group or private chat, send:
     ```
     @NewsBot tech startups
     ```
     The bot replies with a summary, e.g.:
     ```
     Recent news about tech startups: Anthropic raised $500M for AI development (TechCrunch, 2025-04-15). New startup incubators launched in Silicon Valley (Forbes, 2025-04-14).
     ```
   - Use `/start` to see instructions.

## Repository Structure
```
news-aggregator/
├── src/
│   ├── __init__.py            # Marks src as a package
│   ├── main.py                # Entry point, orchestrates modules
│   ├── collector.py           # Fetches news from NewsAPI
│   ├── aggregator.py          # Summarizes news using LlamaIndex
│   ├── bot.py                 # Handles Telegram interactions
├── .env                       # Environment variables (not committed)
├── requirements.txt           # Python dependencies
├── .gitignore                 # Excludes sensitive files
├── README.md                  # This file
```

## Modules
- **main.py**: Entry point that initializes the Telegram bot, schedules hourly updates, and coordinates `collector`, `aggregator`, and `bot` modules.
- **collector.py**: Fetches news articles from NewsAPI based on user keywords or default business headlines.
- **aggregator.py**: Prepares LlamaIndex `Document` objects and generates summaries using `SummaryIndex`.
- **bot.py**: Handles Telegram interactions:
  - `query_handler`: Detects `@BotName <keywords>` in chats.
  - `post_to_channel`: Sends summaries to Telegram chats or channels.

## Future Enhancements
- **LlamaHub Reader**: Implement LLM-powered web scrapers
- **Event-Driven**: Set-up a `webhook` web app for resource optimization instead of `long-pulling` 