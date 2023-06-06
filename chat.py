import openai
import sys

# Set up your OpenAI API credentials
openai.api_key = ''


def chat_completion(prompt):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': prompt}],
    )
    return response.choices[0].message.content


# Example usage
sys.stdout.write("User: ")
sys.stdout.flush()
user_message = sys.stdin.readline().strip()
chat_history = user_message

while user_message.lower() != 'exit':
    response = chat_completion(chat_history)
   # assistant_reply = response.split() 
    assistant_reply = response
    chat_history += "\nUser: " + user_message + "\nAssistant: " + assistant_reply
    print("Assistant:", assistant_reply)
   # print("Assistant:", " ".join(assistant_reply))
    sys.stdout.write("User: ")
    sys.stdout.flush()
    user_message = sys.stdin.readline().strip()
