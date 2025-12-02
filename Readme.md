Comandos en Ubuntu en WSL:

cd "/mnt/c/Users/pamel/Desktop/4o Trimestre PAPD/PYCHATBOT-PDEV"

docker build -t chatbot-py:latest . 

Instalar Ollama desde Ubuntu en WSL: curl -fsSL https://ollama.com/install.sh | sh
Ejecutar Ollama desde Ubuntu en WSL: ollama run llama2

Si se realizan ajustes en el app.py se debe hacer nuevamente el build del docker:
    docker build --no-cache -t chatbot-py .
