# 🎙️ Multimodal Voice Assistant

An AI-powered multimodal voice assistant designed to support voice-based interaction, intelligent responses, conversational memory, and image understanding. The project integrates speech recognition, Large Language Models (LLMs), and vector database storage to provide an interactive conversational experience.

## ✨ Features

* 🎤 **Speech-to-Text:** Converts spoken input into text using Whisper.
* 🧠 **AI-Powered Responses:** Generates intelligent responses using Large Language Models.
* 🔊 **Text-to-Speech:** Supports spoken responses for interactive conversations.
* 💬 **Conversational Memory:** Uses ChromaDB for context-aware conversation memory.
* 🖼️ **Image Understanding:** Supports image-related interactions.
* 🌐 **Web-Based Interface:** Provides a browser-based interface for user interaction.
* ⚡ **API Integration:** Connects with AI services through APIs.
* 🧹 **Memory Management:** Includes utilities for managing vector database data.

## 🛠️ Technologies Used

* **Programming Language:** Python
* **Backend Framework:** Django
* **Frontend:** HTML, CSS, JavaScript
* **Speech Recognition:** Whisper
* **AI Model Integration:** Groq API
* **Vector Database:** ChromaDB
* **AI Application Framework:** LangChain

## 📂 Project Structure

```text
multimodal-voice-assistant/
├── api/
├── chat/
├── templates/
├── voicAsst/
├── manage.py
├── requirements.txt
├── clear_vd.py
├── run_with_ngrok.py
├── view_chromadb.py
└── README.md
```

## 🚀 Installation and Setup

### Prerequisites

* Python 3.x
* Git
* Required API credentials

### 1. Clone the Repository

```bash
git clone https://github.com/brunda-7/multimodal-voice-assistant.git
```

### 2. Navigate to the Project Directory

```bash
cd multimodal-voice-assistant
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project directory and add the API credentials required by the application.

**Important:** Never upload API keys, passwords, or other sensitive credentials to GitHub.

### 5. Run the Application

```bash
python manage.py runserver
```

Open the local development URL displayed in the terminal to access the application.

> **Note:** Additional configuration may be necessary depending on the project's Django settings, API requirements, and database configuration.

## 🔮 Future Enhancements

* Face recognition
* Emotion detection
* Multiple LLM integration
* Mobile application support
* Cloud deployment
* Offline functionality

## 👩‍💻 Author

Brunda T S
(https://github.com/brunda-7)

## 📌 Project Information

This project explores the integration of speech recognition, conversational AI, and vector database memory to create an interactive multimodal voice assistant.

