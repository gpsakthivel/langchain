import json
import os
from pathlib import Path
import urllib.error
import urllib.request


API_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_dotenv() -> None:
    env_file = Path(__file__).with_name(".env")
    if not env_file.exists():
        return

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        name, value = line.split("=", 1)
        name = name.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(name, value)


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key or api_key == "your-api-key-here":
        raise RuntimeError(
            "Replace the OPENROUTER_API_KEY placeholder in .env with a valid API key."
        )

    payload = {
        "model": "openai/gpt-4o",
        "min_tokens": 10,
        "max_tokens": 1000,
        "temperature": 0,
        # "messages": [
        #     {
        #         "role": "user",
        #         "content": "What is the meaning of life?",
        #     }
        # ],
        "messages": [
            {
                "role": "system",
                "content": "you are backend engineer, you only answer to backend only questions",
            },
            {
                "role": "user",
                "content": "What is angular?",
            },
            {
                "role": "assistant",
                "content": "I'm focused on backend technologies, but I can tell you that Angular is a front-end web application framework developed by Google. It's used for building dynamic single-page applications (SPAs) using HTML, CSS, and TypeScript. If you have any questions related to backend technologies or how they might interact with a front-end framework like Angular, feel free to ask!",
            },
            {
                "role": "user",
                "content": "what is my first question?",
            }
        ],
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenRouter returned HTTP {error.code}: {error_body}") from error

    print(result["choices"][0]["message"]["content"])


if __name__ == "__main__":
    main()
