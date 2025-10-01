# MottuVision – Reconhecimento de Placas Veiculares

O **MottuVision** é um sistema de visão computacional desenvolvido em **Python** que utiliza técnicas de **detecção de objetos (YOLO)** e **reconhecimento óptico de caracteres (OCR via EasyOCR)** para identificar automaticamente placas de veículos a partir de vídeos ou câmeras em tempo real.  

O sistema foi estruturado em **camadas independentes**, permitindo maior organização, escalabilidade e manutenibilidade:

- **Camada de Orquestração (app.py)**: Inicializa o sistema, gerencia os serviços de câmera, processamento e armazenamento.  
- **Camada de Processamento de Câmera (camera_processor.py)**: Leitura contínua dos vídeos/câmeras, envio de frames para análise.  
- **Camada de Visão Computacional (vision.py)**: Utiliza YOLO para detectar placas nos frames e EasyOCR para extrair o texto.  
- **Camada de Armazenamento (storage.py)**: Gerencia cache em memória e escrita otimizada em disco (JSON).

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)  
- [Vídeo de Demonstração](#-vídeo-de-demostração)
- [Funcionalidades](#-funcionalidades)  
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)  
- [Hardware Necessário](#-hardware-necessário)  
- [Configuração do Ambiente](#️-configuração-do-ambiente)  
- [Instalação](#-instalação)   
- [Estrutura do Projeto](#-estrutura-do-projeto)  
- [Simulação](#-simulação) 
- [Screenshots](#-screenshots) 
- [Estrutura de Dados](#-estrutura-de-dados) 
- [Desenvolvedores](#-desenvolvedores)  
- [Links Úteis](#-links-úteis)  
- [Licença](#-licença)  

---

## 🚦 Sobre o Projeto

O sistema detecta e reconhece **placas no padrão brasileiro Mercosul (ABC1D23)** em tempo real ou em vídeos previamente gravados.  
Ele mantém uma lista de registros atualizada em **background**, evitando perda de dados caso um veículo saia do campo de visão.  

Aplicações práticas:  
- Controle de acesso
- Monitoramento de tráfego
- Sistemas de segurança veicular

---

## 📹 Vídeo de Demonstração

**Demonstração Completa do Sistema**: [YouTube](https://youtu.be/W_g3iX-E5Y4)

O vídeo apresenta:
- Detecção de placas em tempo real com videos pré-gravados
- OCR com validação no padrão Mercosul
- Visualização de dados em dashboard

---

## ✨ Funcionalidades

- Captura contínua de vídeo (RTSP, webcam ou arquivos locais)  
- Detecção de placas com **YOLO**  
- Reconhecimento de caracteres com **EasyOCR**  
- Validação no formato brasileiro Mercosul  
- Armazenamento em cache com escrita otimizada em JSON  
- API Flask para consulta dos registros em tempo real  

---

## 🛠 Tecnologias Utilizadas

- **Python 3.9+**
- **Flask** – API REST
- **Git** - Versionamento
- **JSON** – Estrutura de dados
- **YOLOv8** – detecção de placas
- **OpenCV** – captura e manipulação de vídeo
- **EasyOCR** – reconhecimento de caracteres alfanuméricos
- **Threading** – execução simultânea do processamento das fontes
- **Next** – Framework Front-End
- **Axios** – Client HTTP baseado em promises

---

## 💻 Hardware Necessário

- GPU Dedicada (Opicional)
- 8GB RAM (mínimo)
- Processador Quad-Core
- Drivers **CUDA** + **cuDNN** configurados  
> ⚠️ Sem GPU, o sistema roda na CPU, porém com performance reduzida.  
> ⚠️ Os testes foram feitos com uma RTX 2070(GPU) e em um i7 de 4a Geração(CPU) separadamente.

---

## 🐈‍⬛ Clone do Projeto (GitHub)

Acesse o projeto em https://github.com/MOTTU-VISION/iot.git

![alt text](/assets/image-2.png)

selecione uma das opções em **<> Code**

![alt text](/assets/image-4.png)

#### Ou simplesmente execute no git bash:
```
git clone https://github.com/MOTTU-VISION/iot.git.

```

## ⚙️ Configuração do Ambiente

#### Dentro da pasta iot execute:

```bash
cd backend

# Criação do ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\\Scripts\\activate      # Windows

# Instalação das dependências
pip install -r requirements.txt

```

## 📁 Estrutura do Projeto

```
iot/
├── backend/
├── frontend/
├── .gitignore
├── LICENSE
└── README.md

iot/
└── backend/
    └── data/
    │   ├── alerts/             # Alertas criados pelo sistema
    │   ├── records/            # Registros criados via OCR
    │   └── video/              # Videos locais para análise
    └── .venv/
    └── app.py                  # Inicializa o sistema
    └── vision.py               # Recebe frames e aplica 
    └── worker.py               # Inicializa o processamento em threads
    └── storage.py              # Realiza a montagem e persistência local dos dados
    └── analyzer.py             # Recebe a analiza os frames em tempo real com YOLO e OCR
    └── camera_processor.py     # Cria instâncias de camera em threads com base no worker.py
    └── gpu_support_test.py     # Verifica se os drivers CUDA e cuDNN estão configurados previamente

iot/
└── frontend/
    └── public/
    └── src/
    |   └── api/                # Criação do client com axios
    |   └── app/                # Página principal
    |   └── components/         # Components funcionais
    |   └── types/              # Tipagem typescript
    └── package-lock.json
    └── package.json
    └── tsconfig.json

```

## 💻 Simulação

Após configurar o ambiente virtual execute os seguintes comandos

```bash
# Dentro da pasta iot

cd frontend

npm install

npm run dev

# Após executar os comandos aparecerá em qual porta do sistema a aplicação estará em execução
```
![alt text](/assets/image-5.png)

Após iniciar o frontend vamos iniciar o backend. Execute os seguintes comandos:

```bash
# Desntro da pasta iot

cd backend

python app.py 

# Após executar os comandos aparecerá em qual porta do sistema a aplicação estará em execução
```
![alt text](/assets/image-6.png)

## 📸 Screenshots

![alt text](/assets/image-7.png)

![alt text](/assets/image-8.png)

![alt text](/assets/image-9.png)

## 💾 Estrutura de Dados

Abaixo veremos a representação dos dados criados pelo sistema

### Registros

```bash
[
  {
    "camera_id": "camera1",
    "timestamp": 1759342285.234748,
    "placa": "JAF9344",
    "bounding_box": [
      82,
      487,
      214,
      783
    ],
    "label": "3"
  },
]
```

### Alertas

```bash
[
  {
    "camera_id": "camera2",
    "placa": "EBR8E70",
    "timestamp": 1759342285.6055796,
    "alert": "Placa n\u00e3o cadastrada",
    "severity": "low"
  },
]
```

## 👨‍💻 Desenvolvedores

Este projeto foi desenvolvido por:

- **Daniel Barros RM 556152** - *Desenvolvedor* - [GitHub](https://github.com/Barros263inf) | [LinkedIn](https://www.linkedin.com/in/danielbarros63)
- **Luccas Alencar RM 558253** - *Desenvolvedor* - [GitHub](https://github.com/LuccasAlencar) | [LinkedIn](https://www.linkedin.com/in/luccasalencar/)
- **Raul Claussn RM 556152** - *Desenvolvedor* - [GitHub](https://https://github.com/RaulClauson) | [LinkedIn](https://www.linkedin.com/in/raul-clauson/)

## 🔗 Links Úteis

- [OCR](https://nextjs.org/)
- [YOLO](https://nextjs.org/)
- [Next Js](https://nextjs.org/)
- [Baixe o Git](https://git-scm.com/downloads)

## 📄 MIT License

Copyright (c) 2025 MOTTU-VISION

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.