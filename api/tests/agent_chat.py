
from core.prompt import MUSIC_PROMPT, CHAT_PROMPT
from core.llm import OpenAILLM
import time

qwen_agent = OpenAILLM(model= "qwen2.5-7b-instruct")
messages = [{"role": "system", "content": CHAT_PROMPT}]

def main():
    while True:
        question = input("Question: ")
        if question.lower() in ['q', 'exit']:
            print("Exiting...")
            break

        current_timestamp = int(time.time() * 1000)

        messages.append({"role": "user", "content": question})

        answer = qwen_agent.generate_response(messages)

        messages.append({"role": "assistant", "content": answer})

        current_timestamp1 = int(time.time() * 1000) - current_timestamp
        print(f"Answer {current_timestamp1}ms: {answer}")
    
    for msg in messages:
        print(f"{msg['role']}: {msg['content']}")

if __name__ == "__main__":
    main()
