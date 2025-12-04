Integrantes:
- Pamela Jacqueline Selman David 25002792,
- Jenniffer Jeannette Rojas Gaitán 17003167,
- Julio Aq'ab'al Rodriguez Xicará 25005373

------------------------------------------

Estructura: 
PYCHATBOT-PDEV/
├── chatbot/
│   ├── assets/                # Archivos estáticos (logo, CSS, imágenes)
│   │   └── bibliobot.png
│   │
│   ├── data/                  # Datasets para el chatbot
│   │   ├── books.csv
│   │   ├── ratings.csv
│   │   └── users.csv
│   │
│   ├── app.py                 # Backend principal con FastAPI
│   ├── Dockerfile             # Configuración de la imagen Docker
│   ├── index.html             # Interfaz web del chatbot
│   └── requirements.txt       # Dependencias del proyecto
│
├── ollama/
│   └── models/                # Modelos / llaves SSH
│       ├── id_ed25519
│       └── id_ed25519.pub
│
├── .gitignore                 # Archivos ignorados por Git
└── docker-compose.yaml        # Orquestación de servicios con Docker Compose


------------------------------------------
Comandos en Ubuntu en WSL:

    cd "/mnt/c/Users/pamel/Desktop/4o Trimestre PAPD/PYCHATBOT-PDEV"
    docker-compose down
    docker-compose up --build

