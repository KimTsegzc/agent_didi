import openai
from openai import OpenAI
import base64

def init(src):
    global client
    global O_source, key, url
    O_source = src
    if O_source == "OpenAI":
        url = "https://api.openai.com/v1"
        key = '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'
    elif O_source == "Nuwa":
        url = "https://api.nuwaapi.com/v1"
        key = 'sk-oxirYGNoyv0otJJZiIS6iB9zdmyjVr3KbKdd5WTQMQfsYjr8'
    else:
        raise ValueError(f"Unknown O_source: {O_source}")
    client = OpenAI(
        api_key=key,
        base_url=url,
    )


def L0_OpenAI_chat(prompt):
    model = "gpt-4o"
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def L0_OpenAI_VL(prompt, url):
    model = "gpt-4o-mini"
    base64_image = encode_image(url)
    chat = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return chat.choices[0].message.content


def L0_OpenAI_TTS(text, speech_file_path="./media/output.mp3"):
    with client.audio.speech.with_streaming_chat.create(
        model="tts-1",
        voice="alloy",
        input=text,
        speed=1.3,
    ) as chat:
        chat.stream_to_file(speech_file_path)

init("Nuwa")

if __name__ == '__main__':
    init("Nuwa")
    prompt = "What is the meaning of life? short in 30 words"
    response = L0_OpenAI_chat(prompt)
    print(f"AI response: {response}")
    response = L0_OpenAI_VL('what this pic?', "./media/snapshot.png")
    print(f"AI response: {response}")
