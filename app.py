import gradio as gr

import os
from datetime import datetime
from ModelMerge.utils import prompt
from ModelMerge.models import chatgpt
LANGUAGE = os.environ.get('LANGUAGE', 'Simplified Chinese')
GPT_ENGINE = os.environ.get('GPT_ENGINE', 'gpt-4-turbo-2024-04-09')
API = os.environ.get('API', None)
Current_Date = datetime.now().strftime("%Y-%m-%d")
systemprompt = os.environ.get('SYSTEMPROMPT', prompt.system_prompt.format(LANGUAGE, Current_Date))
chatgptbot = chatgpt(api_key=f"{API}", engine=GPT_ENGINE, system_prompt=systemprompt)


with gr.Blocks(fill_height=True) as demo:
    with gr.Column():
        chatbot = gr.Chatbot(show_label=False, elem_id="chatbox", scale=10, height=900)  # 设置聊天框高度
        with gr.Row():
            msg = gr.Textbox(placeholder="输入你的问题...", elem_id="inputbox", scale=10)
            clear = gr.Button("清除", elem_id="clearbutton")

    # 用户输入处理函数，记录用户的问题
    def user(user_message, history):
        return "", history + [[user_message, None]]

    # 机器人回答函数，根据用户的问题生成回答
    def bot(history):
        print(history)
        user_message = history[-1][0]
        history[-1][1] = ""
        answer = ""
        for text in chatgptbot.ask_stream(user_message):
            print(text, end="")
            if "🌐" in text:
                history[-1][1] = text
            else:
                answer += text
                history[-1][1] = answer
            yield history

    # 提交用户消息和处理回答
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    # 清除聊天记录
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()