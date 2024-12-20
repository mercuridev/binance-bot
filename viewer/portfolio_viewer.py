import tkinter as tk
from tkinter import ttk
from datetime import datetime  # Para pegar a hora atual
from bot import CriptoBot
from utils import convert_to_brl

def update_portfolio():
    bot = CriptoBot()

    # Exibir mensagem de carregamento
    update_button.config(state=tk.DISABLED, text="Carregando...")
    root.update_idletasks()  # Atualiza a interface antes de processar

    balances = bot.get_balance()
    selected_currency = currency_combo.get()

    # Limpar a área de exibição
    portfolio_text.delete(1.0, tk.END)
    portfolio_text.insert(tk.END, f"Seu Portfólio (valores em {selected_currency}):\n\n")

    try:
        total_value = 0  # Para somar o valor total do portfólio

        for asset, amount in balances.items():
            if amount > 0:
                price = 0  # Valor padrão para moedas sem conversão

                # Determinar o par para conversão
                try:
                    if asset == selected_currency:
                        price = 1  # Exemplo: 1 USDT = 1 USDT
                    else:
                        # Buscar preço do par direto (ex.: GALABRL ou GALAUSDT)
                        pair = f"{asset}{selected_currency}"
                        price = float(bot.get_price_data(pair)[0])
                except Exception:
                    try:
                        # Tentar conversão indireta via BTC (ex.: YOYO → BTC → USDT)
                        pair_to_btc = f"{asset}BTC"
                        price_in_btc = float(bot.get_price_data(pair_to_btc)[0])
                        btc_to_selected = float(bot.get_price_data(f"BTC{selected_currency}")[0])
                        price = price_in_btc * btc_to_selected
                    except Exception:
                        price = 0  # Moeda sem par disponível

                # Calcular o valor total da moeda
                value_in_currency = amount * price
                total_value += value_in_currency

                # Exibir moeda no formato "MOEDA: VALOR / QTDE"
                portfolio_text.insert(
                    tk.END, f"- {asset}: {value_in_currency:.2f} {selected_currency} / {amount:.6f}\n"
                    if price > 0
                    else f"- {asset}: Preço não disponível / {amount:.6f}\n"
                )

        # Exibir o valor total do portfólio
        portfolio_text.insert(tk.END, f"\nValor Total: {total_value:.2f} {selected_currency}\n")

    except Exception as e:
        portfolio_text.insert(tk.END, f"\nErro ao buscar dados: {str(e)}")

    # Atualizar hora da última atualização
    current_time = datetime.now().strftime("%H:%M:%S")
    last_update_label.config(text=f"Última atualização: {current_time}")

    # Remover mensagem de carregamento
    update_button.config(state=tk.NORMAL, text="Atualizar Portfólio")

    # Atualizar novamente após 1 minuto (60000 ms)
    root.after(60000, update_portfolio)

# Carregar configurações ao abrir
def load_initial_portfolio():
    currency_combo.set("BRL")  # Define BRL como padrão
    update_portfolio()

# Criar janela principal
root = tk.Tk()
root.title("CriptoBot - Portfólio")

# Combobox para seleção de moeda
tk.Label(root, text="Selecione a moeda para exibir:").pack()
currency_combo = ttk.Combobox(root, values=["BRL", "USDT", "BTC", "ETH"], state="readonly")
currency_combo.set("BRL")  # Padrão inicial
currency_combo.pack()

# Botão para atualizar portfólio
update_button = tk.Button(root, text="Atualizar Portfólio", command=update_portfolio)
update_button.pack()

# Área de texto para exibição do portfólio
portfolio_text = tk.Text(root, height=20, width=50)
portfolio_text.pack()

# Rótulo para exibir a hora da última atualização
last_update_label = tk.Label(root, text="Última atualização: --:--:--", font=("Helvetica", 10))
last_update_label.pack()

# Carregar portfólio automaticamente ao abrir
load_initial_portfolio()

# Iniciar janela
root.mainloop()
