# simple-chatbot-watsonxai
Simple chatbot dengan menggunakan library LangChain dan IBM Watsonx AI model yang diintegrasikan dengan UI Chatbot Streamlit. Menggunakan model meta-llama/llama-2-13b-chat dengan maksimal responses sebanyak 500 tokens. Simple chatbot ini merupakan hasil belajar yang saya lakukan untuk memperdalam pengetahuan saya terkait pembuatan chatbot menggunakan model yang telah disediakan oleh pihak ke-tiga (di sini adalah IBM Cloud).

## Kemampuan chatbot ini:
- Dapat me-generate respon dengan maksimal 500 token atau ~370 kata
- Memberikan respon dengan format:
  * Pendahuluan singkat
  * Tiga poin utama
  * Kesimpulan singkat

## Kekurangan chatbot ini:
- Tidak semua pertanyaan dapat dipahami oleh model sehingga menghasilkan respon kosong
- Chatbot terkadang menghasilkan respon yang tidak selalu sesuai dengan context yang diinginkan

## Library yang digunakan (requirements.txt):
- streamlit==1.45.1
- langchain-ibm==0.3.12
