import os
from dotenv import load_dotenv
from flask import Flask, request
from hugchat import hugchat
from hugchat.login import Login
from db.orm import (initialize_orm, create_conversation_for_user, get_conversation_id_for_user,
                    update_conversation_id_for_user)

version = "1.0"

# load .env file
load_dotenv()
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')


# flask REST API
app = Flask(__name__)

# load database
initialize_orm()

# Log in to huggingface and grant authorization to huggingchat
sign = Login(email, password)
cookies = sign.login()

# Save cookies to the local directory
cookie_path_dir = "./cookies_snapshot"
sign.saveCookiesToDir(cookie_path_dir)

# Load cookies when you restart your program:
# sign = login(email, None)
# cookies = sign.loadCookiesFromDir(cookie_path_dir)
# This will detect if the JSON file exists, return cookies if it does and raise an Exception if it's not.

# Create a ChatBot
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"

print('Ririko HuggingChat Server, version ' + version + " is now running")


@app.route("/api/v1/ask", methods=["POST"])
def ask():
    print('Received a new request.')
    data = request.json
    if "prompt" in data:
        user_id = data["user_id"]
        conversation_id = get_conversation_id_for_user(user_id)

        if conversation_id:
            print("Existing conversation id " + str(conversation_id) + " found for user " + str(user_id))
            try:
                chatbot.change_conversation(conversation_id)
            except:
                # Create a new conversation
                id = chatbot.new_conversation()
                update_conversation_id_for_user(data["user_id"], id)
                print("Conversation id changed to " + str(id) + " for user " + str(user_id))
        else:
            # Create a new conversation
            id = chatbot.new_conversation()
            create_conversation_for_user(data["user_id"], id)
            print("New conversation id " + str(id) + " created for user " + str(user_id))

        # # Get conversation list
        # conversation_list = chatbot.get_conversation_list()
        #
        # # Switch model (default: meta-llama/Llama-2-70b-chat-hf. )
        # # chatbot.switch_llm(0) # Switch to `OpenAssistant/oasst-sft-6-llama-30b-xor`
        # # chatbot.switch_llm(1) # Switch to `meta-llama/Llama-2-70b-chat-hf`
        #
        answer = chatbot.chat(data["prompt"])

        return {
            "answer": answer
        }
    else:
        return {
            "error": "Prompt not found in the request body."
        }
