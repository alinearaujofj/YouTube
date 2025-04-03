import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader Plus")
        self.root.geometry("450x250")
        
        # Variáveis
        self.var_mp3 = tk.BooleanVar()
        self.progress_var = tk.DoubleVar()
        
        # Widgets
        self.create_widgets()
    
    def create_widgets(self):
        # URL Entry
        tk.Label(self.root, text="URL do Vídeo:").pack(pady=5)
        self.entry_url = tk.Entry(self.root, width=50)
        self.entry_url.pack(pady=5)
        
        # MP3 Checkbutton
        tk.Checkbutton(self.root, text="Baixar como MP3", variable=self.var_mp3).pack(pady=5)
        
        # Progress Bar
        self.progress_bar = ttk.Progressbar(
            self.root, 
            orient="horizontal",
            length=300, 
            mode="determinate",
            variable=self.progress_var
        )
        self.progress_bar.pack(pady=10)
        
        # Download Button
        tk.Button(self.root, text="Baixar", command=self.baixar).pack(pady=10)
        
        # Status Label
        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack(pady=5)
    
    def update_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress_var.set(percentage)
        self.status_label.config(text=f"Baixando: {percentage:.1f}%")
        self.root.update_idletasks()
    
    def baixar(self):
        url = self.entry_url.get().strip()
        pasta = filedialog.askdirectory()
        
        if not url:
            messagebox.showerror("Erro", "Insira uma URL válida do YouTube!")
            return
        
        if not pasta:
            return
        
        try:
            self.progress_var.set(0)
            self.status_label.config(text="Iniciando download...", fg="blue")
            
            yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
            
            
            if self.var_mp3.get():
                stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                file_type = "áudio"
            else:
                stream = yt.streams.get_highest_resolution()
                file_type = "vídeo"
            
            if not stream:
                raise Exception("Nenhuma stream disponível para download")
            
            self.status_label.config(text=f"Preparando {file_type}: {yt.title[:30]}...")
            
            arquivo = stream.download(output_path=pasta)
            
            if self.var_mp3.get():
                base, ext = os.path.splitext(arquivo)
                novo_nome = base + ".mp3"
                os.rename(arquivo, novo_nome)
                arquivo = novo_nome
            
            self.status_label.config(text="Download completo!", fg="green")
            messagebox.showinfo("Sucesso", f"{file_type.capitalize()} salvo como:\n{os.path.basename(arquivo)}")
            
        except RegexMatchError:
            messagebox.showerror("Erro", "URL inválida. Verifique o link do vídeo.")
            self.status_label.config(text="URL inválida", fg="red")
        except VideoUnavailable:
            messagebox.showerror("Erro", "Vídeo indisponível (pode ser privado, restrito ou removido).")
            self.status_label.config(text="Vídeo indisponível", fg="red")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no download:\n{str(e)}")
            self.status_label.config(text=f"Erro: {str(e)}", fg="red")
        finally:
            self.progress_var.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()