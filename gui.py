import tkinter as tk
from tkinter import ttk, messagebox
import main  

class MusicApp:
    def __init__(self, root):
        BG_COLOR = "#121212"
        TEXT_COLOR = "#FFFFFF"
        BOX_COLOR = "#282828"
        
        self.root = root
        self.root.title("Music Discovery Engine")
        self.root.geometry("800x750")
        self.root.configure(bg=BG_COLOR)

        self.style = ttk.Style()
        self.style.theme_use('default')
        
        self.style.configure("TFrame", background=BG_COLOR)
        self.style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Helvetica", 11))
        self.style.configure("TRadiobutton", background=BG_COLOR, foreground=TEXT_COLOR, font=("Helvetica", 11))
        self.style.configure("TButton", font=("Helvetica", 11, "bold"))
        self.style.map("TRadiobutton", background=[('active', BG_COLOR)])

        title_label = tk.Label(root, text="Music Discovery Engine", 
                               font=("Helvetica", 28, "bold"), 
                               bg=BG_COLOR, fg=TEXT_COLOR)
        title_label.pack(pady=25)

        control_frame = ttk.Frame(root)
        control_frame.pack(pady=10)

        self.mode_var = tk.StringVar(value="song") 
        ttk.Radiobutton(control_frame, text="Find Songs", variable=self.mode_var, value="song").pack(side=tk.LEFT, padx=20)
        ttk.Radiobutton(control_frame, text="Find Albums", variable=self.mode_var, value="album").pack(side=tk.LEFT, padx=20)

        input_frame = ttk.Frame(root)
        input_frame.pack(pady=15)
        ttk.Label(input_frame, text="Provide search context or artist name:").pack()
        
        self.entry = ttk.Entry(input_frame, width=45, font=("Helvetica", 14))
        self.entry.pack(pady=5)
        self.entry.bind('<Return>', lambda event: self.run_search())

        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="SEARCH", command=self.run_search).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="LAST.FM CHARTS", command=self.show_charts).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="EXPORT PLAYLIST", command=self.save_playlist).pack(side=tk.LEFT, padx=10)

        result_frame = ttk.Frame(root)
        result_frame.pack(pady=20, padx=30, fill="both", expand=True)

        self.results_text = tk.Text(result_frame, height=18, 
                                    font=("Courier New", 12), 
                                    bg=BOX_COLOR,
                                    fg=TEXT_COLOR,
                                    insertbackground="white",
                                    relief="flat",
                                    padx=10, pady=10)
        self.results_text.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(result_frame, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.results_text['yscrollcommand'] = scrollbar.set

        ttk.Button(root, text="Clear Results", command=self.clear_text).pack(pady=15)

    def clear_text(self):
        self.results_text.delete(1.0, tk.END)

    def display_result(self, text):
        self.results_text.insert(tk.END, text + "\n")
        self.results_text.insert(tk.END, "-"*60 + "\n")
        self.results_text.see(tk.END)

    def run_search(self):
        query = self.entry.get().strip()
        mode = self.mode_var.get()
        
        if not query:
            messagebox.showwarning("Input Required", "Please provide a search term.")
            return

        self.results_text.insert(tk.END, f"STATUS: Analyzing '{query}'...\n")
        self.root.update_idletasks()

        try:
            # Execute Hybrid AI Discovery
            tags = main.get_ai_refined_tags(query)
            self.results_text.insert(tk.END, f"METADATA TAGS: {', '.join(tags)}\n")
            
            result_string = ""
            for tag in tags:
                if mode == 'song':
                    result_string += main.get_tracks_by_tag(tag)
                else:
                    result_string += main.get_albums_by_genre(tag)
            
            # Secondary check for direct artist matches if tag search is insufficient
            if not result_string.strip():
                if mode == 'song':
                    result_string = main.get_similar_tracks(query)
                else:
                    result_string = main.get_top_albums(query)

            self.display_result(result_string if result_string.strip() else "No data returned for this query.")
            
        except Exception as e:
            self.display_result(f"SYSTEM ERROR: {e}")

    def save_playlist(self):
        content = self.results_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Export Failed", "No data available to export.")
            return

        filename = "music_discovery_session.txt"
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write("\n" + "="*60 + "\n")
                f.write(f"EXPORT SESSION: {query if 'query' in locals() else 'System Search'}\n")
                f.write(content + "\n")
            messagebox.showinfo("Export Success", f"Data appended to {filename}.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to write file: {e}")

    def show_charts(self):
        try:
            result_string = main.get_current_hits()
            self.display_result(result_string)
        except Exception as e:
            self.display_result(f"SYSTEM ERROR: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicApp(root)
    root.mainloop()