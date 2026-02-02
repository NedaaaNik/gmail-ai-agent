# Gmail AI Agent 🤖📧

This is a Python-based AI agent that connects to your Gmail inbox and uses Google's Gemini 2.5 Flash model to analyze your emails.

**Current Capabilities:**
* Authenticates securely via OAuth 2.0 (no passwords stored).
* Fetches the last 20 emails from your inbox.
* Filters out noise and provides a bulleted "Executive Summary" of the 3 most important items.

## 🛠️ Prerequisites

Before running this agent, you need:
1.  **Python 3.10+** installed.
2.  A **Google Cloud Project** with the Gmail API enabled.
3.  A **Gemini API Key** from Google AI Studio.

## 🚀 Installation

1.  **Clone the repository** (or download the files):
    ```bash
    git clone [https://github.com/NedaaaNik/gmail-ai-agent.git]
    cd gmail-ai-agent
    ```

2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuration (Important)

For security reasons, API keys and credentials are **not** included in this repository. You must create them locally:

1.  **Google Credentials:**
    * Download your OAuth 2.0 Client Desktop file from Google Cloud Console.
    * Rename it to `credentials.json` and place it in this folder.

2.  **Environment Variables:**
    * Create a file named `.env` in this folder.
    * Add your Gemini API Key inside it like this:
        ```env
        GEMINI_API_KEY=AIza...
        ```

## 🏃‍♂️ Usage

Run the agent:
```bash
python agent.py

```bash
python agent.py
