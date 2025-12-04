Estructura: 
PYCHATBOT-PDEV/
├── docker-compose.yaml
├── chatbot/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   ├── index.html
│   └── data/
│       ├── books.csv
│       ├── ratings.csv
│       └── users.csv

Comandos en Ubuntu en WSL:

    cd "/mnt/c/Users/pamel/Desktop/4o Trimestre PAPD/PYCHATBOT-PDEV"
    docker-compose down
    docker-compose up --build