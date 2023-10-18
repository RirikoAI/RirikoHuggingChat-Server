import os
from dotenv import load_dotenv
from flask import Flask, request
from hugchat import hugchat
from hugchat.login import Login
from db.orm import (initialize_orm, create_conversation_for_user, get_conversation_id_for_user,
                    update_conversation_id_for_user)

version = "2.0"

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

models = chatbot.get_available_llm_models()

print('Ririko HuggingChat Server, version ' + version + " is now running. Available models: ")
i = 1

for obj in models:
    print(obj)


def find_conversation(conversation_id):
    found_object = None  # Initialize a variable to store the found object (if any)
    remote_conversations = chatbot.get_remote_conversations(replace_conversation_list=True)

    for obj in remote_conversations:
        if obj.id == conversation_id:
            found_object = obj
            break  # If found, exit the loop

    if found_object is not None:
        return found_object
    else:
        return False


@app.route("/api/v1/ask", methods=["POST"])
def ask():
    print('Received a new request.')

    data = request.json
    if "prompt" in data:
        user_id = data["user_id"]
        conversation_id = get_conversation_id_for_user(user_id)
        existing_conversation = find_conversation(conversation_id)

        if existing_conversation:
            conversation_id = existing_conversation.id

        key = "system_prompt"

        if key not in data:
            data["system_prompt"] = "Your name is Ririko and you are chatting with the user named " + data["user_id"]

        if conversation_id:
            try:
                print("Existing conversation id " + str(conversation_id) + " found for user " + str(user_id))
                chatbot.change_conversation(existing_conversation)
            except:
                # Create a new conversation
                id = chatbot.new_conversation(2, data["system_prompt"])
                update_conversation_id_for_user(data["user_id"], id)
                chatbot.change_conversation(id)
                print("Conversation id changed to " + str(id) + " for user " + str(user_id))
        else:
            # Create a new conversation
            id = chatbot.new_conversation(2, data["system_prompt"])
            create_conversation_for_user(data["user_id"], id)
            print("New conversation id " + str(id) + " created for user " + str(user_id))

        # # Get conversation list
        # conversation_list = chatbot.get_conversation_list()
        #
        # # Switch model (default: meta-llama/Llama-2-70b-chat-hf. )
        # # chatbot.switch_llm(0) # Switch to `OpenAssistant/oasst-sft-6-llama-30b-xor`
        # # chatbot.switch_llm(1) # Switch to `meta-llama/Llama-2-70b-chat-hf`
        #
        answer = ""

        # stream response into the answer variable and send it to the user
        key = "token"
        for resp in chatbot.query(
                data["prompt"],
                stream=True
        ):
            try:
                if key in resp:
                    answer += resp["token"]
            except:
                answer += ""

        print("Submitted answer for user " + str(user_id))

        return {
            "answer": answer
        }
    else:
        return {
            "error": "Prompt not found in the request body."
        }
