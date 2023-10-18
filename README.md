## RirikoHuggingChat-Server

This is the HuggingChat API server for RirikoAI.

### What's the difference with RirikoAI/RirikoLLaMA-Server?

| RirikoHuggingChat-Server                  | RirikoLLaMA-Server                                          |
|-------------------------------------------|-------------------------------------------------------------|
| Uses the HuggingChat API                  | Runs the OpenLLaMA model in your PC (No internet API calls) |
| Does not host the model in your RAM / GPU | Hosts the model in your RAM / GPU                           |
| Censored                                  | Uncensored                                        |

### Requirements
Sign up for HuggingFace Account: https://huggingface.co/join

### About API usage

HuggingFace is kind enough to let us use the API for free. Please be kind and mindful not to abuse it.

## Installing The Server

### 1. Install Python 3.11 in your PC:

https://www.python.org/downloads/release/python-3110/ (Install it to C:\Python311)

### 2. Install pip

- Download this file https://bootstrap.pypa.io/get-pip.py (Download this to C:\Python311 or the
  same directory where your Python installation is)
- Open your terminal (Command Prompt / PowerShell)
- Change dir to the Python installation folder: `cd C:\Python311`
- Install pip: `python get-pip.py`
- Check if pip is successfully installed: `pip --version`

### 3. Activate virtual environment

```python3 -m venv venv```

### 4. Install requirements

```pip install -r requirements.txt```

### 5. Copy .env.example into .env

Copy and enter your email and password

### 6. Run the LLaMA server

```flask run --host=0.0.0.0 -p 5000```

The server will now run locally at:  http://127.0.0.1:5000. You can send a POST request to `http://localhost:5000/api/v1/ask` API endpoint for your chatbot.

## Using the API:

Example API request: POST `/api/v1/ask` with JSON in the body

```json5
{
  "prompt": "Hello! I'm Angel!",
  "user_id": "angel",
  "system_prompt": "Your name is Ririko, and you are now talking to Angel"
}
```
Use the same `user_id` in the json body so conversations persists.

### Example Response from the server:

```json5
{
  "answer": "Hello Angel! It's nice to meet you. Is there anything you need help with or would you like to chat for a bit?"
}
```

## Credits
1. HuggingFace (https://huggingface.co/)
2. Soulter/hugging-chat-api (https://github.com/Soulter/hugging-chat-api)
