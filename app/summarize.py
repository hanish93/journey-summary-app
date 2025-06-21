import subprocess

def generate_summary(captions):
    prompt = "Summarize this trip in a travel journal style:\n" + "\n".join([f"- {cap}" for _, cap in captions])
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120
        )
        return result.stdout.decode("utf-8").strip()
    except Exception as e:
        return f"Error generating summary: {e}"
