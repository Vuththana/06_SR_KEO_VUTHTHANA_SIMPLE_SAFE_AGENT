from agent import StudentAssistantAgent

def main():

    logged_in_user_id = 1

    agent = StudentAssistantAgent(user_id=logged_in_user_id, model="qwen3.5:2b")

    prompt = "What is the schedule for the Spring Boot course?"
    print(f"User Request: {prompt}")

    answer = agent.run(prompt)
    print(f"\nFinal Assistant Response:\n{answer}")

if __name__ == "__main__":
    main()