import openai
from openai import OpenAI
import base64
import playsound
from dashscope import MultiModalConversation
import dashscope
from dashscope.audio.tts_v2 import *

def init(src):
    global O_src
    global client
    O_src = src
    if src == "OpenAI":
        url = "https://api.openai.com/v1"
        key = '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'
    elif src == "Nuwa":
        url = "https://api.nuwaapi.com/v1"
        key = 'sk-oxirYGNoyv0otJJZiIS6iB9zdmyjVr3KbKdd5WTQMQfsYjr8'
    elif src == "aliyuncs":
        url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        key = 'sk-33d5aa12eea3461c922d3342b16dd7b3'
        dashscope.api_key = "sk-33d5aa12eea3461c922d3342b16dd7b3"
    else:
        raise ValueError(f"Unknown O_source: {src}")
    client = OpenAI(
        api_key=key,
        base_url=url,
    )


def L0_OpenAI_chat(prompt, model = "gpt-4o"):
    if O_src == "aliyuncs":
        model = "deepseek-r1-distill-qwen-32b"
    # print(f"[L0]: OpenAI chat with {model}...")
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


def L0_OpenAI_VL(prompt, pic, model = "gpt-4o-mini"):
    base64_image = encode_image(pic)
    if O_src == "aliyuncs":
        model = "qwen-vl-max-latest"
    # print(f"[L0]: OpenAI VL with {model}...")
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


def L0_OpenAI_TTS(text, path="./media/output.mp3", model="tts-1"):
    if O_src in ["OpenAI", "Nuwa"]:
        with client.audio.speech.with_streaming_chat.create(
            model=model,
            voice="alloy",
            input=text,
            speed=1.3,
        ) as chat:
            chat.stream_to_file(path)
    elif O_src == "aliyuncs":
        model = "cosyvoice-v1"
        voice = "longxiaoxia" 
        synthesizer = SpeechSynthesizer(model=model, voice=voice, speech_rate=1.2)
        audio = synthesizer.call(text)
        with open(path, 'wb') as f:
            f.write(audio)


def L0_OpenAI_STT(path, model="whisper-1"):
    audio_file= open(path, "rb")
    if O_src in ["OpenAI", "Nuwa"]:
        print(f"[L0]: OpenAI STT with {model}...")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return transcription.text
    elif O_src == "aliyuncs":
        print(f"[L0]: OpenAI STT with aliyuncs...")
        messages = [
            {
                "role": "user",
                "content": [{"audio": path}],
            }
        ]
        response = MultiModalConversation.call(
            model="qwen-audio-asr",
            messages=messages
        )
        return response["output"]["choices"][0]["message"]["content"][0]["text"]
    return None


init("aliyuncs")


if __name__ == '__main__':
    init("aliyuncs")
    # response = L0_OpenAI_chat(
    #     "What is the meaning of life? short in 30 words", 
    #     model='deepseek-r1-distill-qwen-32b'
    # )
    # print(f"AI response: {response}")

    # response = L0_OpenAI_VL(
    #     '这张图是什么内容',
    #     "./media/snapshot.png", 
    #     model='qwen-vl-max-latest'
    # )
    # print(f"AI response: {response}")

    # L0_OpenAI_TTS(
    #     '晚上好，我的朋友',
    #     path='./media/output.mp3',
    #     model='tts-1'
    # )
    # playsound.playsound("./media/output.mp3")

    asr = L0_OpenAI_STT(
        path='./media/output.mp3',
        model='whisper-1'
    )
    print(asr)
