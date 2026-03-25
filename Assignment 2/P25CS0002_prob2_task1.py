import os

from openai import OpenAI

_API_KEY = os.environ.get("OPENAI_API_KEY")
if not _API_KEY:
    raise SystemExit(
        "Missing OPENAI_API_KEY. Set it in your environment before running this script."
    )

client = OpenAI(api_key=_API_KEY)

# Use a real model id from your account; override with OPENAI_MODEL if needed.
_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


def generate_names(n=1000, batch_size=100):
    names = []

    for _ in range(n // batch_size):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Generate {batch_size} unique Indian full names "
                        f"(first name + last name). Output only names, one per line, "
                        f"no numbering or bullets."
                    ),
                }
            ],
        )

        batch = response.choices[0].message.content.strip().split("\n")
        names.extend(batch)

    return names[:n]


def save_names(filename="TrainingNamesGPT.txt"):
    names = generate_names(1000)

    with open(filename, "w", encoding="utf-8") as f:
        for name in names:
            f.write(name.strip() + "\n")

    print(f"Saved {len(names)} names to {filename}")


if __name__ == "__main__":
    save_names()
