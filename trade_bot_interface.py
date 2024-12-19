import time
import random
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext
from bot import CriptoBot  # Importando a classe real integrada com a carteira atual

# Regras do bot
COMPRAR_QUEDA = -0.05  # Comprar quando cair mais de 5%
VENDER_ALTA = 0.05     # Vender quando subir mais de 5%
LUCRO_MINIMO = 0.003   # Lucro mínimo de 0,3%
STOP_LOSS = -0.02      # Stop-loss em 2%
SLIPPAGE_TOLERANCIA = 0.0005  # Slippage tolerável de 0,05%
VOLUME_LIMITE = 0.8    # Usar no máximo 80% do saldo
INTERVALO = 10         # Intervalo de 10 segundos para demonstração

# Interface Gráfica
class TradeBotGUI:
    def __init__(self, root):
        self.bot = CriptoBot()  # Agora utiliza a classe real integrada com a carteira atual
        self.root = root
        self.root.title("Bot de Trade - Interface")
        self.log_count = 1
        self.precos_anterior = {}
        self.running = False  # Estado do bot

        # Widgets
        self.log_area = scrolledtext.ScrolledText(root, width=80, height=20)
        self.log_area.pack(padx=10, pady=10)
        self.start_button = tk.Button(root, text="Iniciar Bot", command=self.toggle_bot)
        self.start_button.pack(pady=5)

    def log(self, mensagem):
        """Adiciona uma mensagem numerada na área de log."""
        self.log_area.insert(tk.END, f"{self.log_count}. {mensagem}\n")
        self.log_area.yview(tk.END)
        self.log_count += 1

    def toggle_bot(self):
        """Inicia ou para o bot."""
        if self.running:
            self.running = False
            self.start_button.config(text="Iniciar Bot")
            self.log("Bot parado pelo usuário.")
        else:
            self.running = True
            self.start_button.config(text="Parar Bot")
            self.log("Conectando com a carteira...")
            if self.verify_connection():
                self.log("Conexão bem-sucedida. Iniciando o bot de trade...")
                self.run_bot()
            else:
                self.log("Falha ao conectar com a carteira. Verifique suas credenciais e API.")
                self.start_button.config(text="Iniciar Bot")
                self.running = False

    def verify_connection(self):
        """Verifica a conexão inicial com a API."""
        try:
            self.bot.get_balance()
            return True
        except Exception as e:
            self.log(f"Erro de conexão: {e}")
            return False

    def run_bot(self):
        """Executa as regras de trade periodicamente."""
        if not self.running:
            return
        try:
            self.log("Atualizando portfólio...")
            portfolio = self.bot.get_balance()  # Utiliza o saldo real da carteira
            for moeda, saldo in portfolio.items():
                pair = f"{moeda}BRL"  # Construindo o par correto com BRL
                try:
                    self.log(f"Verificando preço de {pair}...")
                    preco_atual = float(self.bot.get_price_data(pair))  # Preço real da API
                    preco_antigo = self.precos_anterior.get(moeda, preco_atual)
                    variacao = (preco_atual - preco_antigo) / preco_antigo

                    self.log(f"{moeda}: Preço R${preco_atual:.2f} | Variação: {variacao:.2%}")

                    # Regras de compra e venda seguras
                    if variacao <= COMPRAR_QUEDA:  # Comprar na queda
                        valor_para_comprar = sum(self.bot.get_balance().values()) * VOLUME_LIMITE
                        mensagem = self.bot.buy(moeda, valor_para_comprar)
                        self.log(f"Detectada queda em {moeda}. {mensagem}")

                    elif variacao >= VENDER_ALTA and saldo > 0:  # Vender na alta
                        preco_min_venda = preco_antigo * (1 + LUCRO_MINIMO + SLIPPAGE_TOLERANCIA)
                        if preco_atual >= preco_min_venda:
                            mensagem = self.bot.sell(moeda)
                            self.log(f"Detectada alta em {moeda}. {mensagem}")
                        else:
                            self.log(f"Preço atual não atinge lucro mínimo com slippage. Aguardando...")

                    elif variacao <= STOP_LOSS:  # Stop-loss para limitar perdas
                        mensagem = self.bot.sell(moeda)
                        self.log(f"Stop-loss acionado em {moeda}. {mensagem}")

                    self.precos_anterior[moeda] = preco_atual

                except Exception as e:
                    self.log(f"Erro ao obter dados para {pair}: {e}")
        except Exception as e:
            self.log(f"Erro ao acessar API: {e}. Verifique o status da API.")
            self.running = False
            self.start_button.config(text="Iniciar Bot")

        self.log("Próxima verificação em alguns segundos...")
        self.log("--------------------------------------------")
        self.root.after(INTERVALO * 1000, self.run_bot)

# Inicialização da interface
if __name__ == "__main__":
    root = tk.Tk()
    app = TradeBotGUI(root)
    root.mainloop()
