import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import main

class MusicApp:
    def __init__(self, root):
        BG_COLOR = "#121212"
        TEXT_COLOR = "#FFFFFF"
        BOX_COLOR = "#282828"
        
        self.root = root
        self.root.title("Music Recommender")
        self.root.geometry("800x700")
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
        
        ttk.Radiobutton(control_frame, text="Find Songs 🎵", variable=self.mode_var, value="song").pack(side=tk.LEFT, padx=20)
        ttk.Radiobutton(control_frame, text="Find Albums 💿", variable=self.mode_var, value="album").pack(side=tk.LEFT, padx=20)

        input_frame = ttk.Frame(root)
        input_frame.pack(pady=15)
        
        ttk.Label(input_frame, text="Enter Artist or Genre:").pack()
        
        self.entry = ttk.Entry(input_frame, width=40, font=("Helvetica", 14))
        self.entry.pack(pady=5)
        self.entry.bind('<Return>', lambda event: self.run_search())

        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="SEARCH", command=self.run_search).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="LAST.FM CHARTS", command=self.show_charts).pack(side=tk.LEFT, padx=10)

        result_frame = ttk.Frame(root)
        result_frame.pack(pady=20, padx=30, fill="both", expand=True)

        self.results_text = tk.Text(result_frame, height=15, 
                                    font=("Courier New", 13), 
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
        self.results_text.insert(tk.END, text + "\n" + "-"*50 + "\n")
        self.results_text.see(tk.END)

    def run_search(self):
        query = self.entry.get().strip()
        mode = self.mode_var.get()
        
        if not query:
            messagebox.showwarning("Input Error", "Please enter an artist or genre!")
            return

        possible_subs = main.get_manual_subgenres(query)
        if possible_subs:
            options_str = ", ".join(possible_subs)
            refinement = simpledialog.askstring(
                "Sub-Genre Found", 
                f"Found: {options_str}\n\nType one below or leave blank:",
                parent=self.root
            )
            if refinement:
                query = refinement.strip()

        self.results_text.insert(tk.END, f" Searching for '{query}'...\n")
        result_string = ""
        
        try:
            if mode == 'song':
                if query.lower() in main.GENRE_MAP or possible_subs:
                    result_string = main.get_tracks_by_tag(query)
                else:
                    result_string = main.get_similar_tracks(query)

            elif mode == 'album':
                if query.lower() in main.GENRE_MAP or possible_subs:
                    result_string = main.get_albums_by_genre(query)
                else:
                    result_string = main.get_top_albums(query)
            
            self.display_result(result_string)
            
        except Exception as e:
            self.display_result(f"Error: {e}")

    def show_charts(self):
        try:
            result_string = main.get_current_hits()
            self.display_result(result_string)
        except Exception as e:
            self.display_result(f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicApp(root)
    root.mainloop()