## Chatbot IT Support
Chatbot ini berbasis Retrieval Augmented Generation (RAG). Chatbot ini dirancang untuk mengatasi permasalahan troubleshooting berdasarkan knowledge base internal perusahaan, namun untuk saat ini data knowledge base masih berupa data dummy sambil menunggu konfirmasi divisi terkait.

### Scope
- Microsoft 365
- Printer & Drive
- Windows/Laptop
- Jaringan, VPN, dan sejenisnya

### Tech Stack
- **Frontend:** React, Tailwind CSS
- **Backend:** Python, Typescript, FastAPI
- **Model:** Gemini, Groq

### Dataset
Untuk dataset yang diambil, berupa dataset primer yang didapat dari internal perusahaan dan dataset sekunder yang diambil dari web hugging face
- **Primer:** File-file internal berupa pdf, txt, dan sejenisnya
- **Sekunder:** [IT Helpdesk Dataset](https://huggingface.co/datasets/Console-AI/IT-helpdesk-synthetic-tickets)
