import os
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def converter_e_renomear_arquivos(pasta_origem, formato=".webp", qualidade=80, progress_bar=None):
    try:
        total_files = sum([len(files) for _, _, files in os.walk(pasta_origem)])
        current_file = 0

        for subdir, _, files in os.walk(pasta_origem):
            for file in files:
                if not file.lower().endswith(formato):
                    imagem_path = os.path.join(subdir, file)
                    base_name, ext = os.path.splitext(file)

                    try:
                        num = int(base_name)
                    except ValueError:
                        num = 0

                    novo_nome = f"{num:03}{formato}"
                    caminho_saida = os.path.join(subdir, novo_nome)

                    try:
                        img = Image.open(imagem_path)
                        img.convert("RGB").save(caminho_saida, "WEBP", quality=qualidade)
                        os.remove(imagem_path)
                    except Exception as e:
                        print(f"Erro ao converter {imagem_path} para {formato}: {e}")
                        raise

                    current_file += 1
                    progress_value = int((current_file / total_files) * 100)
                    progress_bar["value"] = progress_value
                    root.update_idletasks()

        resultado_label.config(text="Arquivos renomeados e convertidos!")
    except Exception as e:
        resultado_label.config(text=f"Erro durante o processo: {str(e)}")

def selecionar_pasta():
    pasta_origem = filedialog.askdirectory()
    pasta_origem_entry.delete(0, tk.END)
    pasta_origem_entry.insert(0, pasta_origem)

def processar():
    try:
        pasta_origem = pasta_origem_entry.get()
        formato_desejado = formato_entry.get()
        qualidade = int(qualidade_entry.get())

        if not pasta_origem:
            resultado_label.config(text="Por favor, selecione um diretório.")
            return

        progress_bar["value"] = 0
        converter_e_renomear_arquivos(pasta_origem, formato=formato_desejado, qualidade=qualidade, progress_bar=progress_bar)

    except KeyboardInterrupt:
        resultado_label.config(text="\nProcesso interrompido pelo usuário.")
    except Exception as e:
        resultado_label.config(text=f"Erro inesperado: {str(e)}")

# Configuração da janela principal
root = tk.Tk()
root.title("Conversor e Renomeador de Arquivos")

# Adiciona estilo ttk
style = ttk.Style()
style.theme_use("clam")

# Frame principal
main_frame = ttk.Frame(root, padding="20")
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Widgets
tk.Label(main_frame, text="Diretório do Usuário:").grid(row=0, column=0, sticky=tk.W, pady=5)
pasta_origem_entry = ttk.Entry(main_frame, width=50)
pasta_origem_entry.grid(row=0, column=1, pady=5)
ttk.Button(main_frame, text="Selecionar Pasta", command=selecionar_pasta).grid(row=0, column=2, pady=5)

tk.Label(main_frame, text="Formato Desejado:").grid(row=1, column=0, sticky=tk.W, pady=5)
formato_entry = ttk.Entry(main_frame, width=20)
formato_entry.grid(row=1, column=1, pady=5)

tk.Label(main_frame, text="Qualidade (0-100):").grid(row=2, column=0, sticky=tk.W, pady=5)
qualidade_entry = ttk.Entry(main_frame, width=10)
qualidade_entry.grid(row=2, column=1, pady=5)

progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=3, pady=10)

processar_button = ttk.Button(main_frame, text="Processar", command=processar)
processar_button.grid(row=4, column=0, columnspan=3, pady=10)

resultado_label = ttk.Label(main_frame, text="")
resultado_label.grid(row=5, column=0, columnspan=3, pady=5)

# Inicia o loop da aplicação
root.mainloop()
