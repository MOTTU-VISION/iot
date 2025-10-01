#!/bin/bash

echo "Iniciando back-end..."

cd backend
# Ativa o ambiente virtual
source venv/bin/activate

# Instala dependências, se necessário
python3 pip install -r requirements.txt

# Roda o back-end em background
python3 app.py

# Volta para o diretório raiz
cd ../frontend

echo "Iniciando front-end..."
npm run dev
