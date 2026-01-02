# AI Voice Assistant 🤖🎙️

A modular, Python-based AI voice assistant featuring speech recognition, interruptible text-to-speech, task automation, and real-time intelligence — designed with a clean backend architecture and GUI integration.

---

## ✨ Features

- 🎙️ **Speech-to-Text** (always listening)
- 🔊 **Text-to-Speech** (interruptible with voice command like “stop”)
- 🧠 **Decision-Making Model** to classify queries
- ⚙️ **Task Automation**
  - Open / close applications
  - Play media
  - System controls (volume, mute, etc.)
- 🌐 **Realtime Search Engine** for up-to-date queries
- 💬 **Conversational Chatbot**
- 🛑 **CPU-style Interrupt Handling**
- 🖥️ **GUI Interface**
- 🧩 **Modular Backend Design**

---

## 🏗️ Project Structure

AI Assistant/
│
├── Backend/
│ ├── Automation.py
│ ├── Chatbot.py
│ ├── Model.py
│ ├── RealtimeSearchEngine.py
│ ├── SpeechToText.py
│ ├── TextToSpeech.py
│ └── init.py
│
├── Frontend/
│ ├── GUI.py
│ └── Files/ # Runtime files (ignored in git)
│
├── RVC/
│ ├── inference.py
│ └── requirements.txt
│
├── Main.py
├── Requirements.txt
├── .gitignore
└── README.md

---

## 🚀 How It Works

1. User speaks into the microphone
2. Speech is converted to text
3. Decision model classifies the query
4. Appropriate module is triggered:
   - Chatbot
   - Realtime search
   - Automation
5. Assistant responds via voice and GUI
6. User can interrupt at any time by saying **“stop”**

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/AI-Assistant.git
cd AI-Assistant
2️⃣ Create a Virtual Environment
python -m venv .venv
.venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r Requirements.txt

🔐 Environment Variables

Create a .env file in the project root:

Username=YourName
Assistantname=YourAssistant
GroqAPIKey=YOUR_GROQ_API_KEY
AssistantVoice=en-US-JennyNeural
InputLanguage=en


⚠️ .env is ignored by Git for security reasons.

▶️ Run the Assistant
python Main.py


Make sure:

Microphone access is enabled

Chrome + matching ChromeDriver are installed (for speech recognition)

🧠 Supported Commands Examples

“Open WhatsApp”

“Play music”

“What is Python?”

“What’s today’s news?”

“Mute volume”

“Stop” (interrupts speech and tasks)

🖼️ Image Generation

Image generation is currently disabled.
Planned future support:

Local Stable Diffusion

Cloud-based image APIs

🧩 Future Enhancements

🔥 Local image generation (Stable Diffusion)

🎭 Emotion-based voice modulation

🧠 Memory & personalization

⏰ Reminders & scheduling

🌍 Multi-language support

⚠️ Security Notes

API keys are never committed

Runtime/generated files are ignored

GitHub secret scanning is enabled

👤 Author

Shahid Mushtaq
Built with passion and persistence 💪

📜 License

This project is for educational and personal use.
License can be added later if open-sourced publicly.


---

## ✅ What you should do next

1. Create `README.md`
2. Paste the content above
3. Run:
```bash
git add README.md
git commit -m "Add README documentation"
git push
