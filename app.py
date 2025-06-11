import streamlit as st
from langchain_ibm import WatsonxLLM
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 550,
        "min_new_tokens": 450,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50,
        "repetition_penalty": 1.1,
        "stop_sequences": ["\n\n", "###", "Human:"]
    }

watsonx_llm = WatsonxLLM(
    model_id="meta-llama/llama-2-13b-chat",
    url="https://jp-tok.ml.cloud.ibm.com",
    project_id="a2958eed-53df-4dd3-b1e0-a484fa2ca965",
    apikey="7vKcuTXUQKeYBWIHrSCh3DtkSFhdokjnrS4sZ_hqKaTL",
    params=parameters,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

def estimate_tokens(text: str) -> int:
    """Estimasi lebih akurat dengan mix karakter-kata"""
    word_count = len(text.split())
    char_count = len(text)
    return int((word_count * 1.5) + (char_count / 6))

def generate_precise_response(prompt: str, target_tokens=500) -> str:
    """Generasi respons dengan presisi token"""

    init_prompt = f"""
    Buat respons tentang: {prompt}
    - Target: {target_tokens} token (~375 kata)
    - Format: Pendahuluan singkat, 3 poin utama, kesimpulan singkat
    - Akhiri dengan "[END]"
    """
    
    chunks = []
    total_tokens = 0
    max_attempts = 3
    
    while total_tokens < target_tokens and max_attempts > 0:
        chunk = watsonx_llm(init_prompt if not chunks else 
                           f"Lanjutkan dengan detail tambahan: {chunks[-1][-200:]}")
        
        chunks.append(chunk)
        total_tokens = estimate_tokens(' '.join(chunks))
        max_attempts -= 1
        
        if "[END]" in chunk:
            break
    
    full_response = ' '.join(chunks)
    
    if "[END]" in full_response:
        full_response = full_response.split("[END]")[0]
    
    final_tokens = estimate_tokens(full_response)
    if final_tokens > target_tokens:
        words = full_response.split()
        adjusted = ' '.join(words[:int(target_tokens * 0.67)])
        return adjusted
    
    return full_response

st.title('Ask watsonx!')
with st.expander("ℹ️ About This Chatbot"):
    st.markdown("""
    **Chatbot Capabilities:**
    - Can generate responses up to 500 tokens or ~370 words
    - Provides responses in structured format:
      * Brief introduction
      * Three main points
      * Concise conclusion
    
    **Current Limitations:**
    - May not understand all questions, potentially resulting in empty responses
    - Responses may occasionally deviate from the intended context
    - Accuracy may vary for complex or ambiguous queries
    """)

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

if prompt := st.chat_input('Pass Your Prompt here'):
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role':'user', 'content':prompt})
    
    try:
        with st.spinner('Thinking...'):
            response = generate_precise_response(prompt)
        
        st.chat_message('assistant').markdown(response)
        st.session_state.messages.append({'role':'assistant', 'content':response})
    
    except Exception as e:
        st.error(f"Error mendapatkan respons: {str(e)}")
        st.session_state.messages.append({'role':'assistant', 'content':f"Error: {str(e)}"})
