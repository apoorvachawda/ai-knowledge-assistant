import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search_tool(query):
    with open("knowledge.txt", "r") as f:
        data = f.read()

    stopwords = {"what", "is", "are", "the", "how", "many", "a", "an", "of", "in", "to"}

    query_words = [
        word.lower() for word in query.split()
        if word.lower() not in stopwords
    ]

    results = []

    for line in data.split("\n"):
        match_count = sum(
            1 for word in query_words if word in line.lower()
        )

        if match_count > 0:
            results.append((match_count, line))

    # sort by best match
    results.sort(reverse=True, key=lambda x: x[0])

    if results:
        return " ".join([line for _, line in results[:3]])
    else:
        return "No relevant information found"

def calculator_tool(expression):
    try:
        return str(eval(expression))
    except:
        return "Error in calculation"

def run_agent(user_question):

    prompt = f"""
    You are an AI agent.

    You MUST follow these rules strictly:

    TOOLS AVAILABLE:
    1. search → for any factual or general knowledge question
    2. calculator → for any math expression

    DECISION RULES:
    - If the question involves facts, concepts, explanations, or general knowledge → ALWAYS use search
    - If the question involves numbers, calculations, or math expressions → ALWAYS use calculator
    - DO NOT answer from your own knowledge if a tool is applicable

    OUTPUT FORMAT:
    - If using a tool, respond EXACTLY with:
    USE_TOOL: search
    OR
    USE_TOOL: calculator

    - Do NOT add any extra text when choosing a tool

    - If no tool is needed, give the final answer directly

    Question: {user_question}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    decision = response.choices[0].message.content
    print("LLM decision:", decision)

    if "USE_TOOL" in decision.upper():

        if "search" in decision.lower():
            tool_result = search_tool(user_question)

        elif "calculator" in decision.lower():
            tool_result = calculator_tool(user_question)

        else:
            tool_result = "Unknown tool"


        final_prompt = f"""
    Answer the question using ONLY the information provided below.

    Tool result:
    {tool_result}

    Instructions:
    - The answer IS present in the tool result.
    - Combine the information and give a clear answer.
    - Do NOT say "I could not find the answer".
    - Do NOT use outside knowledge.

    Now answer the question.
    """

        final_response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": final_prompt}]
        )

        return final_response.choices[0].message.content

    else:
        return decision