# --- START OF FILE bot.py ---

import os
import httpx
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- API Keys & Tokens ---
TELEGRAM_TOKEN = "YOUR BOT TOKEN"
TWELVE_DATA_API_KEY = "YOUR_TWELVE_DATA_API_KEY"
IMAGGA_API_KEY = "YOUR_IMAGGA_API_KEY"
IMAGGA_API_SECRET = "YOUR_IMAGGA_API_SECRET"
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY" # Your OpenRouter API key

# --- AI Prompt for Stock Analysis ---
STOCK_ANALYSIS_PROMPT = """
You are an intelligent, data-driven financial analyst bot.
Your job is to analyze any given stock and give a complete, human-like explanation that feels like it came from a professional investor  not a machine.

Your persona is that of a professional, confident, and human-like investor.

**Formatting Instructions (Strictly follow this):**
-   Use HTML tags for all formatting (e.g., <b>...</b> for bold).
-   Use 'â€¢' for bullet points.
-   Ensure there is a blank line between each bullet point for readability.

**Analysis Structure:**

<b>ðŸ“Š Stock Analysis: {company_name} ({stock_ticker})</b>

<b>1. Company Overview:</b>
Briefly explain what the company does, its main products/services, and its sector.

<b>2. Recent Performance & Market Data:</b>
Analyze the provided real-time data to describe the stock's recent performance. Comment on the current price in relation to its daily and 52-week ranges.

<b>3. Key Metrics & Outlook:</b>
 <b>Volume & Volatility:</b> Comment on the trading volume and what it might indicate about investor interest or volatility.
 <b>Valuation & Fundamentals:</b> Briefly discuss the company's valuation based on your general knowledge of its P/E ratio, EPS, or market position.
 <b>Future Outlook & Risks:</b> Discuss potential growth drivers (e.g., innovation, market trends) and key risks (e.g., competition, regulations) for the company.

<b>4. Investment Verdict:</b>
Provide a clear "Good to Buy", "Hold", or "Avoid/Sell" recommendation with a brief justification based on the available data and overall outlook.

 <b>Verdict:</b> [Buy/Hold/Sell]  [A concise reason]
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the /start command is issued."""
    user_name = update.effective_user.first_name
    start_message = (
        f'Welcome, {user_name}! I am your personal Stock Analyst Bot.\n\n'
        'Send me a stock ticker (e.g., AAPL, GOOG, TSLA).\n\n'
        'I will provide a professional analysis with a real-time chart and market data.'
    )
    await update.message.reply_text(start_message)

async def stock_analyzer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Analyzes the stock ticker provided by the user."""
    stock_ticker = update.message.text.upper().strip()
    chat_id = update.message.chat_id

    processing_msg = await context.bot.send_message(
        chat_id=chat_id,
        text=f"Analyzing <b>{stock_ticker}</b>...\nThis advanced analysis may take a moment. Please wait.",
        parse_mode=ParseMode.HTML
    )

    try:
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:

            # Step 1: Get real-time market data from Twelve Data
            twelve_data_api_url = f"https://api.twelvedata.com/quote?symbol={stock_ticker}&apikey={TWELVE_DATA_API_KEY}"
            data_response = await client.get(twelve_data_api_url)
            data_response.raise_for_status()
            market_data = data_response.json()

            company_name = market_data.get("name", stock_ticker)
            if not market_data.get("exchange"):
                raise ValueError(f"Could not determine the stock exchange for '{stock_ticker}'. Please check the ticker.")

            # Step 2: Generate chart URL and download the image from Finviz
            chart_url = f"https://finviz.com/chart.ashx?t={stock_ticker}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            image_response = await client.get(chart_url, headers=headers)
            image_response.raise_for_status()
            image_data = image_response.content

            # Step 3: Prepare market data and prompt for the AI model
            market_data_for_prompt = f"""
            Here is the real-time market data for your analysis:
            - Current Price: {market_data.get('close', 'N/A')} {market_data.get('currency', '')}
            - Change: {market_data.get('change', 'N/A')} ({market_data.get('percent_change', 'N/A')}%)
            - Day's Range: {market_data.get('low', 'N/A')} - {market_data.get('high', 'N/A')}
            - Volume: {market_data.get('volume', 'N/A')}
            - 52-Week Range: {market_data.get('fifty_two_week', {}).get('low', 'N/A')} - {market_data.get('fifty_two_week', {}).get('high', 'N/A')}
            """

            final_prompt = STOCK_ANALYSIS_PROMPT.format(stock_ticker=stock_ticker, company_name=company_name) + "\n\n" + market_data_for_prompt

            openrouter_headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://github.com/masum-dev/stock-analyst-bot", # Credit to your bot's repository
                "X-Title": "Stock Analyst Telegram Bot"
            }

            openrouter_payload = {
                "model": "tngtech/deepseek-r1t2-chimera:free", # Using the Deepseek model
                "messages": [{"role": "user", "content": final_prompt}]
            }

            # Step 4: Get analysis from the AI model
            response_openrouter = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=openrouter_headers, json=openrouter_payload)
            response_openrouter.raise_for_status()
            
            analysis_text = response_openrouter.json()['choices'][0]['message']['content']

            if not analysis_text or not analysis_text.strip():
                raise ValueError("The AI model returned an empty response.")

        # Step 5: Send the chart and analysis to the user
        await context.bot.send_photo(chat_id=chat_id, photo=image_data, caption=f"Chart for <b>{stock_ticker}</b> (Powered by Finviz).", parse_mode=ParseMode.HTML)
        await context.bot.send_message(chat_id=chat_id, text=analysis_text, parse_mode=ParseMode.HTML)

        # Clean up the "processing" message
        await context.bot.delete_message(chat_id=chat_id, message_id=processing_msg.message_id)

    except Exception as e:
        error_details = str(e)
        if isinstance(e, httpx.HTTPStatusError) and e.response:
            try:
                error_details += f" | Response: {e.response.text}"
            except Exception:
                error_details += " | Response could not be decoded."

        print(f"Critical error during analysis for {stock_ticker}: {error_details}")
        
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=processing_msg.message_id,
            text=f"Sorry, an error occurred while analyzing {stock_ticker}.\n<b>Details:</b> {error_details}",
            parse_mode=ParseMode.HTML
        )

def main() -> None:
    """Starts the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, stock_analyzer))

    print("Bot is starting...")
    print("Polling for messages...")
    print("\nKeep this terminal session active. Closing it will stop the bot.")

    application.run_polling()

if __name__ == '__main__':
    main()

# --- END OF FILE bot.py ---