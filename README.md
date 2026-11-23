# Urban Forest sample chatbot demo

A free sample FAQ chatbot (Streamlit + Google Gemini) you can show the cafe.

## Files
- `app.py`: the chatbot
- `faq.md`: everything the bot knows (edit this, not the code)
- `requirements.txt`: libraries Streamlit needs
- `make_qr.py`: turns your demo link into a QR code image

## 1. Get a free Gemini API key
1. Go to https://aistudio.google.com and sign in with a personal Google account.
2. Click **Get API key** > **Create API key**. Copy it.
3. Never paste the key into app.py or upload it to GitHub.

Note: the free tier has rate limits, and Google may use free-tier data to improve its products. That's fine for a sample with public cafe details, but don't put private customer data in it.

## 2. Check your faq.md
- Replace anything you can confirm with the cafe's real details (menu, prices, delivery, payments).
- Delete any line you can't confirm. The bot will then tell customers to call.

## 3. Put it on GitHub (free)
1. Create a free account at https://github.com and make a **new public repository** (e.g. `urban-forest-demo`).
2. Upload `app.py`, `faq.md` and `requirements.txt`.

## 4. Deploy on Streamlit Community Cloud (free)
1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **Create app**, pick your repository, set the main file to `app.py`.
3. Open **Advanced settings > Secrets** and paste:
   ```
   GEMINI_API_KEY = "paste-your-key-here"
   ```
   If the bot errors about the model, add a second line with a current model name from AI Studio:
   ```
   GEMINI_MODEL = "model-name-from-ai-studio"
   ```
4. Click **Deploy**. You'll get a link like `https://your-app-name.streamlit.app`.

## 5. Make the QR code
Option A (free, on your computer):
```
pip install "qrcode[pil]"
python make_qr.py https://your-app-name.streamlit.app
```
Option B: any free QR generator website. Choose a **static** QR code, because "dynamic" ones can expire or ask for payment later.

Test the QR by scanning it with your phone before you show anyone.

## 6. Before you show the cafe
- Open the link on your phone and ask 10 to 15 questions (including Malayalam ones).
- Free Streamlit apps go to sleep when unused. Open the link a few minutes before your visit so it wakes up.
- Say clearly that this is a sample with unconfirmed details.
