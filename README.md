# ERINAL Telegram Bot

Foydalanuvchidan ism-familiya so'raydi, ERINAL kanaliga obuna bo'lishni taklif qiladi
va ERINAL saytiga o'tish tugmasini beradi.

## Lokal ishga tushirish
```bash
pip install -r requirements.txt
cp .env.example .env   # va BOT_TOKEN ni yozing
python bot.py
```

## Railway'ga deploy
1. Kodni GitHub'ga push qiling.
2. Railway -> New Project -> Deploy from GitHub repo.
3. Variables bo'limiga `BOT_TOKEN` (majburiy), `CHANNEL_URL`, `WEBSITE_URL` qo'shing.
4. Deploy tugagach bot ishlaydi (Procfile: `worker: python bot.py`).
