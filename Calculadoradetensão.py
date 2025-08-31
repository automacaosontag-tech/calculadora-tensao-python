import tkinter as tk
from tkinter import messagebox

# ===================================================================
# 1. FUNÇÕES DE CÁLCULO E LÓGICA
# (É uma boa prática definir as funções primeiro)
# ===================================================================

def calcular_resistencia(material, secao, comprimento):
    """Calcula a resistência do cabo em ohms."""
    # Usando resistividade padrão para Cobre e Alumínio em ohm.mm²/m
    resistividade = 0.0172 if material.lower() == 'cobre' else 0.0282
    # A fórmula considera o caminho de ida e volta do circuito
    resistencia = resistividade * (comprimento * 2) / secao
    return resistencia

def calcular_queda_tensao(tipo_instalacao, tensao, corrente, resistencia):
    """Calcula a queda de tensão em volts e percentual."""
    # Em um circuito monofásico, a queda é direta.
    # Em um trifásico, o fator sqrt(3) é usado para tensão de linha.
    # Como a resistência já considera 2x o comprimento, a fórmula se ajusta.
    if tipo_instalacao.lower() == 'monofásica':
        queda_volts = corrente * resistencia
    else:  # Trifásica
        # A fórmula correta para queda de tensão de linha é: V_queda = I * R_fio * sqrt(3)
        # Como nossa resistência já é 2 * R_fio, a fórmula fica: V_queda = I * (Resistencia_calculada / 2) * 1.732
        queda_volts = (corrente * resistencia / 2) * 1.732
        
    queda_percentual = (queda_volts / tensao) * 100
    return queda_volts, queda_percentual

def executar_calculo():
    """
    Função principal acionada pelo botão.
    Valida as entradas e exibe o resultado.
    """
    # --- Validação de Entradas ---
    campos = {
        "Tensão": entry_tensao.get(),
        "Corrente": entry_corrente.get(),
        "Comprimento": entry_comprimento.get(),
        "Seção": entry_secao.get()
    }

    # Verifica se algum campo está vazio
    for nome, valor in campos.items():
        if not valor:
            messagebox.showerror("Erro de Entrada", f"O campo '{nome}' não pode estar vazio.")
            return

    try:
        # Converte os valores para números, trocando vírgula por ponto
        tensao = float(campos["Tensão"].replace(',', '.'))
        corrente = float(campos["Corrente"].replace(',', '.'))
        comprimento = float(campos["Comprimento"].replace(',', '.'))
        secao = float(campos["Seção"].replace(',', '.'))
        
        material = var_material.get()
        tipo_instalacao = var_tipo.get()

        # Verifica valores lógicos
        if secao <= 0:
            messagebox.showerror("Erro de Lógica", "A seção do cabo deve ser um valor positivo.")
            return
        if tensao <= 0 or corrente < 0 or comprimento <= 0:
            messagebox.showerror("Erro de Lógica", "Tensão, corrente e comprimento devem ser valores positivos.")
            return

    except ValueError:
        messagebox.showerror("Erro de Formato", "Por favor, insira apenas números válidos nos campos.")
        return
    
    # --- Execução do Cálculo ---
    resistencia = calcular_resistencia(material, secao, comprimento)
    queda_volts, queda_percentual = calcular_queda_tensao(tipo_instalacao, tensao, corrente, resistencia)

    # --- Exibição do Resultado ---
    resultado = (
        f"Queda de tensão: {queda_volts:.2f} V\n"
        f"Queda em %: {queda_percentual:.2f}%\n\n"
    )

    if queda_percentual > 4:
        resultado += "Atenção: Queda acima do limite da NBR 5410 (> 4%)."
        lbl_resultado.config(fg="red")
    else:
        resultado += "Queda dentro do limite NBR 5410 (≤ 4%)."
        lbl_resultado.config(fg="green")

    lbl_resultado.config(text=resultado)


# ===================================================================
# 2. CONFIGURAÇÃO DA INTERFACE GRÁFICA (GUI)
# ===================================================================

# --- Janela Principal ---
root = tk.Tk()
root.title("Calculadora de Queda de Tensão")
root.geometry("320x300") # Define um tamanho inicial
root.resizable(False, False) # Impede que a janela seja redimensionada

# --- Frame para os Widgets ---
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(expand=True, fill="both")

# --- Widgets da Interface ---
labels = [
    "Tensão Nominal (V):", "Corrente da Carga (A):", "Comprimento do Cabo (m):",
    "Material do Cabo:", "Seção do Cabo (mm²):", "Tipo de Instalação:"
]

for i, text in enumerate(labels):
    tk.Label(frame, text=text).grid(row=i, column=0, sticky="w", pady=2)

# Entradas de texto
entry_tensao = tk.Entry(frame)
entry_corrente = tk.Entry(frame)
entry_comprimento = tk.Entry(frame)
entry_secao = tk.Entry(frame)

# Menus de Opção
var_material = tk.StringVar(value="Cobre")
option_material = tk.OptionMenu(frame, var_material, "Cobre", "Alumínio")

var_tipo = tk.StringVar(value="Monofásica")
option_tipo = tk.OptionMenu(frame, var_tipo, "Monofásica", "Trifásica")

# Posicionando os widgets no grid
entry_tensao.grid(row=0, column=1, sticky="ew")
entry_corrente.grid(row=1, column=1, sticky="ew")
entry_comprimento.grid(row=2, column=1, sticky="ew")
option_material.grid(row=3, column=1, sticky="ew")
entry_secao.grid(row=4, column=1, sticky="ew")
option_tipo.grid(row=5, column=1, sticky="ew")

# Botão de Calcular
btn_calcular = tk.Button(frame, text="Calcular", command=executar_calculo)
btn_calcular.grid(row=6, column=0, columnspan=2, pady=15)

# Label para o Resultado
lbl_resultado = tk.Label(frame, text="", justify="left", font=("Segoe UI", 9))
lbl_resultado.grid(row=7, column=0, columnspan=2, sticky="w")

# Configura o grid para expandir a coluna 1
frame.grid_columnconfigure(1, weight=1)

# ===================================================================
# 3. INICIAR A APLICAÇÃO
# ===================================================================
root.mainloop()
