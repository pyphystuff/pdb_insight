import ollama

def generate_summary(filename, model="llama3.2"):
    with open(filename, "r") as f:
        content = f.read()

    prompt = f"Summarize this protein structure:\n\n{content[:3000]}"
   
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    summary = response['message']['content']
    print(f"\n🧠 Summary:\n{summary}")
