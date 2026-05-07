<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=3000&pause=1000&color=5865F2&center=true&vCenter=true&width=600&lines=Live+Pix+Payment+Notifier+%F0%9F%94%94;Discord+%2B+Livepix+Integration;Real-time+donation+alerts!" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Discord](https://img.shields.io/badge/Discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Livepix](https://img.shields.io/badge/Livepix-API-00C896?style=for-the-badge)

<br/>

> 🤖 Bot para Discord que notifica em tempo real cada doação recebida via **Livepix** — com nome, valor, moeda e mensagem do doador.

</div>

---

## 📸 Notificação em ação

<div align="center">
  <img src="./assets/notification-preview.png" alt="Prévia da notificação no Discord" width="480"/>
</div>

---

## ✨ Funcionalidades

- 🔔 **Notificação instantânea** de doações no Discord (~5 segundos após o pagamento)
- 👤 Exibe o **nome do doador**
- 💰 Mostra o **valor e a moeda** da doação
- 💬 Inclui a **mensagem** deixada pelo doador
- 🔗 Integração com a **API oficial do Livepix**
- 🚀 Webhook leve via **Flask**

---

## 🔄 Fluxo da aplicação

```
Usuário realiza doação no Livepix
          │
          ▼
Livepix dispara o Webhook → [POST /webhook]
          │
          ▼
Aplicação consulta a API do Livepix
  GET https://api.livepix.gg/v2/messages/{messageId}
          │
          ▼
Bot envia notificação no Discord com os dados completos
```

---

## 🛠️ Tecnologias

| Tecnologia | Papel |
|---|---|
| `Python` | Linguagem principal |
| `Flask` | Servidor HTTP / exposição do webhook |
| `discord.py` | Envio de notificações no Discord |
| `Livepix API` | Fonte dos dados de pagamento |

---

## ⚙️ Configuração

### Pré-requisitos

- Python 3.10+
- Uma conta no [Livepix](https://livepix.gg) com acesso à API
- Um bot criado no [Discord Developer Portal](https://discord.com/developers/applications)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/fabiomoraisdevbr/live-pix-payment-notifier.git
cd live-pix-payment-notifier

# Instale as dependências
pip install -r requirements.txt
```

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DISCORD_TOKEN= seu token de bot do discord
DISCORD_USER_ID= id od usuario que sera notificado
DISCORD_CHANNEL_ID= id do canal (chat) em que ocorrerá a notificação (tem que ser canal de servidor)
LIVE_PIX_CLIENT_ID= id do cliente livepix
LIVE_PIX_CLIENT_SECRET= segredo do cliente livepix

```

### Executando

```bash
python main.py
```

> O servidor Flask ficará escutando na porta `8080` por padrão. Configure o webhook no painel do Livepix apontando para `http://seu-servidor:5000/webhook`.

---

## 📦 Estrutura do projeto

```
live-pix-payment-notifier/
├── main.py              # logica do bot
├── webserver.py         # Rota Flask que recebe os eventos do Livepix
├── service.py           # logica pra chamar o livepix
├── cache.py             # Lógica para guardar dados temporarios, sem precisar de uma DB
├── requirements.txt
└── .env.example
```

---
