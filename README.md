# 🚀 Binance Bot - Automated Cryptocurrency Trading Bot

> Um bot de trading automatizado para ajudar você a maximizar seus lucros no mercado de criptomoedas! 🤑

## 🌟 Funcionalidades

- 📉 **Compra na baixa, venda na alta**: Estratégias otimizadas para operar em mercados voláteis.
- ⏰ **Operações programadas**: Ideal para quem busca operações de médio/longo prazo.
- 📊 **Portfólio diversificado**: Reduza riscos mantendo diferentes ativos no radar.
- 🤖 **Sugestões baseadas em IA**: Recomendações inteligentes para tomada de decisões mais eficazes.
- 🔐 **Segurança**: Utiliza autenticação API para operar com segurança.

---

## 🛠️ Tecnologias Utilizadas

- **Python** 🐍: Linguagem principal do bot.
- **Binance API** 📡: Comunicação direta com a corretora.
- **Pandas** 📊: Para manipulação de dados financeiros.
- **Matplotlib** 📈: Visualização gráfica de tendências e indicadores.
- **Ta-Lib** 🧮: Para cálculos de indicadores técnicos (RSI, MACD, etc.).

---

## 🚀 Começando

### **Pré-requisitos**

1. ✅ Conta na Binance (habilitada para API).
2. ✅ Python 3.8 ou superior instalado.
3. ✅ Biblioteca `pip` atualizada:
   ```bash
   python -m ensurepip --upgrade
   ```

### **Instalação**

1. Clone este repositório:

   ```bash
   git clone https://github.com/mercuridev/binance-bot.git
   cd binance-bot
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv env
   source env/bin/activate  # Linux/macOS
   env\Scripts\activate   # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure as credenciais da Binance:
   - Crie um arquivo `.env` no diretório principal:
     ```env
     BINANCE_API_KEY=your_api_key_here
     BINANCE_SECRET_KEY=your_secret_key_here
     ```

---

## 💡 Como Usar

1. Execute o bot:

   ```bash
   python bot.py
   ```

2. Monitore as operações no terminal ou em logs gerados automaticamente.

3. Personalize estratégias editando os arquivos de configuração.

---

## 📂 Estrutura do Projeto

```plaintext
binance-bot/
├── bot.py                    # Script principal
├── config/                   # Configurações do bot
│   └── params.json           # Parâmetros de execução
├── logs/                     # Logs gerados
│   ├── trading_bot.log       # Log de operações
│   └── trading_report.log    # Relatório de desempenho
├── orders/                   # Gerenciamento de ordens
│   └── orders_manager.py     # Funções para envio e controle de ordens
├── strategies/               # Estratégias de trading
│   ├── rsi_strategy.py       # Estratégia RSI
│   ├── macd_strategy.py      # Estratégia MACD
│   └── sma_strategy.py       # Estratégia de Médias Móveis
├── backtest/                 # Simulador
│   ├── data_loader.py        # Carregador de dados históricos
│   └── simulator.py          # Executor de simulações
├── viewer/                   # Bot extra - Visualizador de portifólio
│   ├── bot.py                # ScriptPrincipal
│   └── config.json           # Configurações e chaves de API
│   └── main.py               # Script Root
│   └── portfolio_viewer.py   # Bot com interface apenas para visualização do portifólio
│   └── utils.py              # Conversão para BRL
├── requirements.txt          # Dependências
├── README.md                 # Documentação
└── .env                      # Credenciais da Binance
```

---

## 📖 Estratégias Incluídas

- **RSI Oversold/Overbought**: Compra quando o RSI está abaixo de 30, venda acima de 70.
- **Cruzamento de Médias Móveis**: Opera com base em cruzamentos de médias rápidas e lentas.
- **MACD Divergence**: Identifica divergências positivas e negativas.

### Adicione suas próprias estratégias 🚀:

- Personalize adicionando novos scripts na pasta `strategies` e conectando-os ao `bot.py`.

---

## ⚠️ Aviso Legal

> Este projeto é para fins educacionais. **Use por sua conta e risco**. Não nos responsabilizamos por perdas financeiras ou mau uso do bot. Sempre teste antes de utilizar em contas reais. 📛

---

## 📌 Contribuições

Sinta-se à vontade para contribuir com melhorias, sugestões ou novas estratégias. 💡 Crie uma **issue** ou envie um **pull request**! 🙌

---

## 🌟 Agradecimentos

Este projeto não seria possível sem as seguintes ferramentas e comunidades:

- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- Comunidade Open Source ❤️

---

## 📞 Contato

Rafael (@mercuridev)

- GitHub: [mercuridev](https://github.com/mercuridev)

---

🚀 **Hora de maximizar seus lucros com inteligência!**
