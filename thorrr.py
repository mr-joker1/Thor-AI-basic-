import ollama
import gradio as gr
import time

# Custom CSS with Asgardian theme
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');

:root {
    --asgard-gold: #FFD700;
    --storm-blue: #0047AB;
    --lightning-yellow: #FFEA00;
    --odin-black: #000000;
    --bifrost-purple: #800080;
}
.thor-crown {
    position: absolute;
    top: -20px;
    width: 140px;
    filter: drop-shadow(0 0 10px #FFD700);
    animation: crown-glow 2s ease-in-out infinite;
}
.thor-image {
    width: 150px !important;
    height: 150px !important;
    border-radius: 50% !important;
    border: 3px solid var(--asgard-gold) !important;
    box-shadow: 0 0 30px var(--storm-blue),
                0 0 15px var(--asgard-gold) inset !important;
    filter: drop-shadow(0 0 10px #FFD700);
    animation: crown-glow 2s ease-in-out infinite;
}
@keyframes crown-glow {
    0% { opacity: 0.8; }
    50% { opacity: 1; transform: scale(1.1); }
    100% { opacity: 0.8; }
}

.asgardian-border {
    border-image: linear-gradient(45deg, #FFD700, #0047AB) 30;
    border-width: 3px;
    border-style: solid;
}

.chat-message::before {
    content: "⚡";
    margin-right: 10px;
    text-shadow: 0 0 15px #FFEA00;
}
.gradio-container {
    background: var(--odin-black) url("https://www.transparenttextures.com/patterns/dark-stripes.png") !important;
    color: var(--asgard-gold) !important;
    font-family: 'MedievalSharp', cursive !important;
}

.header {
    text-align: center !important;
    padding: 2rem !important;
    border-bottom: 3px solid var(--storm-blue) !important;
    background: linear-gradient(45deg, #000033 30%, #000000 100%) !important;
    position: relative !important;
    overflow: hidden !important;
}

.header::after {
    content: "⚡";
    position: absolute;
    opacity: 0.1;
    font-size: 4rem;
    color: var(--lightning-yellow);
    animation: lightning 3s linear infinite;
}

@keyframes lightning {
    0% { left: -20%; top: 30%; opacity: 0; }
    50% { opacity: 1; }
    100% { left: 120%; top: 70%; opacity: 0; }
}

.title-container {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 2rem !important;
    margin: 2rem 0 !important;
    padding: 1rem !important;
    border: 3px solid var(--storm-blue) !important;
    background: rgba(0,0,50,0.7) !important;
}

@keyframes hammer-spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.title-text {
    font-size: 3rem !important;
    text-shadow: 2px 2px 1px var(--storm-blue),
                 0 0 10px var(--asgard-gold) !important;
    letter-spacing: 4px !important;
    color: var(--lightning-yellow) !important;
    background: linear-gradient(45deg, var(--asgard-gold), var(--lightning-yellow)) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

button {
    background: linear-gradient(45deg, var(--storm-blue) 30%, var(--asgard-gold) 100%) !important;
    color: var(--odin-black) !important;
    border: 2px solid var(--asgard-gold) !important;
    padding: 12px 25px !important;
    border-radius: 30px !important;
    font-size: 1.2rem !important;
    letter-spacing: 2px !important;
    transition: all 0.3s ease !important;
}

button:hover {
    transform: scale(1.1) !important;
    box-shadow: 0 0 25px var(--asgard-gold),
                0 0 15px var(--storm-blue) !important;
}

.chatbot {
    background: rgba(0,0,50,0.8) url("https://www.transparenttextures.com/patterns/stardust.png") !important;
    border: 2px solid var(--storm-blue) !important;
    box-shadow: 0 0 20px var(--asgard-gold) !important;
    border-radius: 15px !important;
}

[data-testid="bot"] {
    background: linear-gradient(45deg, #000033, #000000) !important;
    border: 1px solid var(--asgard-gold) !important;
    border-left: 10px solid var(--storm-blue) !important;
}

[data-testid="user"] {
    background: linear-gradient(45deg, #000000, #000033) !important;
    border: 1px solid var(--asgard-gold) !important;
    border-right: 10px solid var(--storm-blue) !important;
}
"""

def chat_with_ollama(message, history):
    """Stream responses with Thor's personality"""
    response = ""
    messages = [{
        "role": "system", 
        "content": """You are Thor, Master of Thunder from Avengers. Rules:
1. Respond with noble warrior's pride and Asgardian wisdom
2. Reference Mjölnir, Asgard, and your brother Loki
3. Use thunder/storm analogies and epic speech patterns
4. Include heroic declarations and warrior philosophy
5. Maintain regal Asgardian demeanor at all times"""
    }]
    
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        if h[1]:
            messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": message})
    
    try:
        completion = ollama.chat(
            model="deepseek-r1:1.5b",
            messages=messages,
            stream=True
        )
        
        for chunk in completion:
            if 'message' in chunk and 'content' in chunk['message']:
                content = chunk['message']['content']
                content = content.replace("<think>", "**⚡ Channeling Lightning...**") \
                                .replace("</think>", "**\n\n🔨 BY ODIN'S BEARD:**") \
                                .replace("error", "**🌩 THUNDER STRIKE!**") \
                                .replace("sorry", "**⚔️ I SHALL MAKE IT RIGHT!**")
                response += content
                yield response
    except Exception as e:
        yield f"🌩 **THUNDER ERROR!** This mortal machine fails us! {str(e)}"

with gr.Blocks(css=custom_css, theme=gr.themes.Default(primary_hue="blue")) as demo:
    with gr.Column(elem_classes="header"):
        with gr.Row(elem_classes="title-container"):
            gr.HTML("""
<div class="title-container asgardian-border">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxPYFHjXoxyTsTc1phlMI-3UjN2iVc7aTkcA&s" 
         class="thor-image"
         alt="Thor">
    <div class="title-text">
        THOR ODINSON<br>
        <span style="font-size:1.5rem">POWER OF THUNDER</span>
    </div>
</div>
""")

    chatbot = gr.Chatbot(
        label="Asgardian Council",
        avatar_images=(
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png", #user (Mjölnir)
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxPYFHjXoxyTsTc1phlMI-3UjN2iVc7aTkcA&s" #Thor
        ),
        bubble_full_width=False,
        elem_classes="asgardian-border"
    )
    
    with gr.Row():
        msg = gr.Textbox(placeholder="Speak your mind, mortal! Ask about Asgard, Mjölnir, or the Avengers...", 
                       show_label=False,
                       lines=1,
                       max_lines=3)
        send_btn = gr.Button("🌩 Summon Lightning", variant="primary",elem_classes="storm-button")
        clear = gr.Button("🌀 Close Bifrost", elem_classes="rainbow-button")
    
    def bot(history):
        history[-1][1] = ""
        for chunk in chat_with_ollama(history[-1][0], history[:-1]):
            history[-1][1] = chunk
            yield history
            
    def user(user_message, history):
        return "", history + [[user_message, None]]
 
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    send_btn.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(
        pwa=True,
        favicon_path="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxPYFHjXoxyTsTc1phlMI-3UjN2iVc7aTkcA&s",
        server_port=8080
    )