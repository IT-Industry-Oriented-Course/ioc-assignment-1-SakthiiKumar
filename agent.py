from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
import os

from tools import (
    search_patient,
    check_insurance,
    find_slots,
    book_appointment
)

load_dotenv()

# =========================
# 🔹 NEW: reusable agent
# =========================
_agent = None

def get_agent():
    global _agent

    if _agent is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY not found in .env")

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            api_key=api_key
        )

        _agent = initialize_agent(
            tools=[
                search_patient,
                check_insurance,
                find_slots,
                book_appointment
            ],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    return _agent


# =========================
# 🔹 NEW: callable function
# =========================
def run_agent(user_input: str) -> str:
    agent = get_agent()
    result = agent.invoke({"input": user_input})
    return result["output"]


# =========================
# 🔹 YOUR EXISTING CLI
# =========================
def main():
    print("Clinical Workflow Agent started")
    print("Type 'q' to quit safely")

    while True:
        try:
            user_input = input("\nClinician : ").strip()

            if user_input.lower() == "q":
                print("Clinical Workflow Agent stopped safely")
                break

            if not user_input:
                print("Empty input ignored.")
                continue

            output = run_agent(user_input)
            print("\nSystem Output:", output)

        except KeyboardInterrupt:
            print("\nSession interrupted by user")
            break
        except Exception as e:
            print("Unable to process request:", e)
            print("Agent is still running.")

    print("Shutdown complete")


if __name__ == "__main__":
    main()
