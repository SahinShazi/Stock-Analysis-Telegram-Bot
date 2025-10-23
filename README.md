# Stock Analyst AI 🤖

Stock Analyst AI is a powerful Telegram bot that provides professional-grade, AI-driven analysis for any stock ticker. It combines real-time market data, high-quality charts, and advanced AI models to deliver comprehensive and easy-to-understand financial insights directly to your chat.

This bot is designed for retail investors, students, and financial enthusiasts who want quick, data-driven analysis without the complexity of traditional financial tools.

---

## ✨ Features

- **📈 Real-Time Market Data:** Fetches the latest stock prices, daily change, volume, and 52-week range.
- **📊 High-Quality Charts:** Generates a clean and informative stock chart for visual technical analysis, powered by Finviz.
- **🧠 AI-Powered Analysis:** Utilizes powerful language models via OpenRouter (like DeepSeek) to provide a human-like analysis of the company, its performance, and future outlook.
- **📝 Structured Reports:** Delivers a well-formatted report covering a company overview, market performance, key metrics, and a final investment verdict.
- **💬 Easy to Use:** A simple and intuitive interface—just send a stock ticker to get started.

---

## ⚙️ How It Works

The bot follows a simple yet powerful workflow:

1. A user sends a stock ticker (e.g., `AAPL`) to the bot on Telegram.
2. The bot fetches real-time financial data from the **Twelve Data API**.
3. It generates a stock chart image by making a request to **Finviz**.
4. It prepares a detailed prompt, combining its instructions with the real-time data.
5. This prompt is sent to a powerful AI model via the **OpenRouter API**.
6. The AI analyzes the information and generates a structured report.
7. Finally, the bot formats the response and sends the chart and the AI-generated analysis back to the user.

---

## 🚀 Setup and Installation

To run this bot on your own server or machine, follow these steps:

### Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token
- API keys for Twelve Data and OpenRouter

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/stock-analyst-ai.git
cd stock-analyst-ai
```

### 2. Install Dependencies

It is highly recommended to use a virtual environment.

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the required libraries
pip install -r requirements.txt
```

### 3. Configure API Keys

Open the `bot.py` file and replace the placeholder values with your actual API keys:

```python
# --- API Keys & Tokens ---
TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"
TWELVE_DATA_API_KEY = "YOUR_TWELVE_DATA_API_KEY"
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"
```

- **TELEGRAM_TOKEN:** Get this from [@BotFather](https://t.me/botfather) on Telegram.
- **TWELVE_DATA_API_KEY:** Sign up on the [Twelve Data website](https://twelvedata.com/) for a free API key.
- **OPENROUTER_API_KEY:** Sign up on the [OpenRouter.ai website](https://openrouter.ai/) to get your API key.

⚠️ **Security Warning:** Never share your API keys publicly or commit them to a public repository.

### 4. Run the Bot

Once the dependencies are installed and the keys are configured, you can start the bot:

```bash
python bot.py
```

The bot will start polling for messages. Keep the terminal session active to keep the bot running.

---

## 💬 How to Use

1. Find your bot on Telegram using the username you set up with BotFather.
2. Send the `/start` command to see the welcome message.
3. Send any valid stock ticker (e.g., `TSLA`, `MSFT`, `KO`) to receive a full analysis.

---

## 🛠️ Technologies Used

- **Language:** Python
- **Telegram Bot Framework:** python-telegram-bot
- **HTTP Requests:** httpx
- **Financial Data:** Twelve Data API
- **Stock Charts:** Finviz
- **AI Model Provider:** OpenRouter.ai

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve this project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes and commit (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 📧 Contact

For questions, suggestions, or feedback, feel free to reach out:

- **GitHub:** [@your-username](https://github.com/your-username)
- **Email:** your.email@example.com

---

## ⭐ Show Your Support

If you find this project helpful, please consider giving it a star on GitHub! ⭐

---

**Happy Investing! 📈💰**