import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import hashlib

COLORS = {
    "bg_dark": "#1e1e2e",
    "bg_darker": "#181825",
    "bg_lighter": "#313244",
    "accent": "#89b4fa",
    "accent_hover": "#b4befe",
    "accent_green": "#a6e3a1",
    "accent_green_hover": "#b5e8b0",
    "accent_red": "#f38ba8",
    "accent_yellow": "#f9e2af",
    "accent_purple": "#cba6f7",
    "accent_purple_hover": "#d8beff",
    "text": "#cdd6f4",
    "text_muted": "#a6adc8",
    "border": "#45475a",
    "shadow": "#11111b"
}

DIFFICULTY_COLORS = {
    "Fácil": "#313250",
    "Médio": "#2d2f42",
    "Difícil": "#372d3f",
    "Muito Difícil": "#3a2c36"
}

CATEGORY_COLORS = {
    "Trabalho": "#2d3f50",
    "Pessoal": "#3d3250",
    "Estudo": "#2d4242",
    "Saúde": "#2d4235",
    "Finanças": "#3f3d2d",
    "Outro": "#3d2d3f"
}

STATUS_COLORS = {
    "Pendentes": "#2d3f50",
    "Concluídas": "#2d4235"
}

FONTS = {
    "header": ("Segoe UI", 18, "bold"),
    "subheader": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 10),
    "body_bold": ("Segoe UI", 10, "bold"),
    "small": ("Segoe UI", 9),
    "tiny": ("Segoe UI", 8)
}

class AnimatedButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        self.default_bg = kwargs.pop('bg', COLORS["accent"])
        self.hover_bg = kwargs.pop('hover_bg', COLORS["accent_hover"])
        self.default_fg = kwargs.pop('fg', COLORS["text"])
        self.hover_fg = kwargs.pop('hover_fg', self.default_fg)
        self.animation_offset = kwargs.pop('animation_offset', 5)
        
        kwargs.update({
            'bg': self.default_bg,
            'fg': self.default_fg,
            'font': kwargs.pop('font', FONTS["body_bold"]),
            'borderwidth': kwargs.pop('borderwidth', 0),
            'padx': kwargs.pop('padx', 15),
            'pady': kwargs.pop('pady', 8),
            'cursor': 'hand2',
            'activebackground': self.hover_bg,
            'activeforeground': self.hover_fg,
            'relief': 'flat'
        })
        
        super().__init__(master, **kwargs)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        self.original_y = None
    
    def on_enter(self, e):
        self.config(background=self.hover_bg, foreground=self.hover_fg)
        if self.original_y is None:
            self.original_y = self.winfo_y()
        
        self.animate_up()
    
    def on_leave(self, e):
        self.config(background=self.default_bg, foreground=self.default_fg)
        
        self.animate_down()
    
    def animate_up(self, current_offset=0):
        if current_offset < self.animation_offset:
            self.place(y=self.original_y - current_offset)
            self.after(5, lambda: self.animate_up(current_offset + 1))
    
    def animate_down(self, current_offset=0):
        if current_offset < self.animation_offset:
            self.place(y=self.original_y - (self.animation_offset - current_offset))
            self.after(5, lambda: self.animate_down(current_offset + 1))
        else:
            self.place(y=self.original_y)

class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        self.default_bg = kwargs.pop('bg', COLORS["accent"])
        self.hover_bg = kwargs.pop('hover_bg', COLORS["accent_hover"])
        self.default_fg = kwargs.pop('fg', COLORS["text"])
        self.hover_fg = kwargs.pop('hover_fg', self.default_fg)
        
        kwargs.update({
            'bg': self.default_bg,
            'fg': self.default_fg,
            'font': kwargs.pop('font', FONTS["body_bold"]),
            'borderwidth': kwargs.pop('borderwidth', 0),
            'padx': kwargs.pop('padx', 15),
            'pady': kwargs.pop('pady', 8),
            'cursor': 'hand2',
            'activebackground': self.hover_bg,
            'activeforeground': self.hover_fg,
            'relief': 'flat'
        })
        
        super().__init__(master, **kwargs)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        self.config(background=self.hover_bg, foreground=self.hover_fg)
    
    def on_leave(self, e):
        self.config(background=self.default_bg, foreground=self.default_fg)

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Checklist")
        
        
        self.root.geometry("500x750")  
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg_dark"])
        
        self.users_file = "checklist_users.json"
        
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as file:
                json.dump({}, file)
        
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.register_username_var = tk.StringVar()
        self.register_password_var = tk.StringVar()
        self.register_confirm_password_var = tk.StringVar()
        
        self.create_login_widgets()
        
        self.center_window()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_login_widgets(self):
      
        self.login_frame = tk.Frame(
            self.root, 
            bg=COLORS["bg_darker"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=30,
            pady=30
        )
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=700)  
        
        shadow_frame = tk.Frame(
            self.root,
            bg=COLORS["shadow"],
            bd=0
        )
        shadow_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=700, x=5, y=5)  
        self.login_frame.lift()
        
        logo_frame = tk.Frame(self.login_frame, bg=COLORS["bg_darker"], height=80)
        logo_frame.pack(fill=tk.X, pady=(0, 10))
        
        logo_label = tk.Label(
            logo_frame,
            text="✓",
            font=("Segoe UI", 50),
            fg=COLORS["accent"],
            bg=COLORS["bg_darker"]
        )
        logo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        def animate_logo(direction=1, offset=0):
            if 0 <= offset <= 10:
                logo_label.place(rely=0.5 + (offset/200) * direction)
                logo_frame.after(50, lambda: animate_logo(direction, offset + 1))
            else:
                logo_frame.after(1000, lambda: animate_logo(-direction, 0))
        
        animate_logo()
        
        header_label = tk.Label(
            self.login_frame, 
            text="Gerenciador de Metas", 
            font=FONTS["header"],
            fg=COLORS["text"],
            bg=COLORS["bg_darker"]
        )
        header_label.pack(pady=(0, 5))
        
        subheader_label = tk.Label(
            self.login_frame, 
            text="Organize suas tarefas com estilo", 
            font=FONTS["small"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"]
        )
        subheader_label.pack(pady=(0, 20))
        
        self.show_login_page()
    
    def show_login_page(self):
        for widget in self.login_frame.winfo_children()[3:]:
            widget.destroy()
        
        user_icon_frame = tk.Frame(self.login_frame, bg=COLORS["bg_darker"], height=40)
        user_icon_frame.pack(fill=tk.X, pady=(10, 0))
        
        user_icon = tk.Label(
            user_icon_frame,
            text="👤",
            font=("Segoe UI", 20),
            fg=COLORS["accent"],
            bg=COLORS["bg_darker"]
        )
        user_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        username_label = tk.Label(
            user_icon_frame, 
            text="Usuário", 
            font=FONTS["body_bold"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"],
            anchor="w"
        )
        username_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        username_entry = tk.Entry(
            self.login_frame,
            textvariable=self.username_var,
            font=FONTS["body"],
            bg=COLORS["bg_lighter"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"]
        )
        username_entry.pack(fill=tk.X, ipady=10, pady=(5, 20))
        username_entry.focus()
        
        pass_icon_frame = tk.Frame(self.login_frame, bg=COLORS["bg_darker"], height=40)
        pass_icon_frame.pack(fill=tk.X)
        
        pass_icon = tk.Label(
            pass_icon_frame,
            text="🔒",
            font=("Segoe UI", 20),
            fg=COLORS["accent"],
            bg=COLORS["bg_darker"]
        )
        pass_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        password_label = tk.Label(
            pass_icon_frame, 
            text="Senha", 
            font=FONTS["body_bold"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"],
            anchor="w"
        )
        password_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        password_entry = tk.Entry(
            self.login_frame,
            textvariable=self.password_var,
            font=FONTS["body"],
            bg=COLORS["bg_lighter"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"],
            show="•"
        )
        password_entry.pack(fill=tk.X, ipady=10, pady=(5, 30))
        
        login_button_container = tk.Frame(self.login_frame, bg=COLORS["bg_darker"], height=50)
        login_button_container.pack(fill=tk.X, pady=(0, 15))
        login_button_container.pack_propagate(False)
        
        login_button = AnimatedButton(
            login_button_container,
            text="ENTRAR",
            command=self.login,
            bg=COLORS["accent_green"],
            hover_bg=COLORS["accent_green_hover"],
            fg=COLORS["bg_darker"],
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=10
        )
        login_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=200, height=40)
        

        create_account_container = tk.Frame(self.login_frame, bg=COLORS["bg_darker"], height=50)
        create_account_container.pack(fill=tk.X, pady=(0, 15))
        create_account_container.pack_propagate(False)
        
   
        glow_frame = tk.Frame(
            create_account_container,
            bg=COLORS["accent_green"],
            highlightbackground=COLORS["accent_green"],
            highlightthickness=1,
            bd=0
        )
        glow_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=210, height=46)
        
        create_account_button = AnimatedButton(
            create_account_container,
            text="CRIAR CONTA",
            command=self.show_register_page,  
            bg=COLORS["accent_green"],
            hover_bg=COLORS["accent_green_hover"],
            fg=COLORS["bg_darker"],
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=10
        )
        create_account_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=200, height=40)
        
  
        def add_icon_to_button():
            icon_label = tk.Label(
                create_account_button,
                text="✚",
                font=("Segoe UI", 11, "bold"),
                fg=COLORS["bg_darker"],
                bg=COLORS["accent_green"]
            )
            icon_label.place(x=25, rely=0.5, anchor="w")
            

            def update_icon_color(event=None):
                icon_label.config(bg=create_account_button["bg"])
            
            create_account_button.bind("<Enter>", lambda e: update_icon_color())
            create_account_button.bind("<Leave>", lambda e: update_icon_color())
        
        self.login_frame.after(100, add_icon_to_button)

        help_label = tk.Label(
            self.login_frame,
            text="Precisa de uma conta para acessar o sistema",
            font=FONTS["tiny"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"]
        )
        help_label.pack(pady=(5, 0))
        
        self.root.bind("<Return>", lambda event: login_button.invoke())
    
    def show_register_page(self):
        for widget in self.login_frame.winfo_children()[3:]:
            widget.destroy()
        
 
        page_title = tk.Label(
            self.login_frame,
            text="Criar Nova Conta",
            font=FONTS["subheader"],
            fg=COLORS["accent_purple"],
            bg=COLORS["bg_darker"]
        )
        page_title.pack(pady=(0, 20))
        
        reg_user_icon_frame = tk.Frame(self.login_frame, bg=COLORS["bg_darker"], height=40)
        reg_user_icon_frame.pack(fill=tk.X, pady=(10, 0))
        
        reg_user_icon = tk.Label(
            reg_user_icon_frame,
            text="👤",
            font=("Segoe UI", 20),
            fg=COLORS["accent_purple"],
            bg=COLORS["bg_darker"]
        )
        reg_user_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        reg_username_label = tk.Label(
            reg_user_icon_frame, 
            text="Usuário", 
            font=FONTS["body_bold"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"],
            anchor="w"
        )
        reg_username_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        reg_username_entry = tk.Entry(
            self.login_frame,
            textvariable=self.register_username_var,
            font=FONTS["body"],
            bg=COLORS["bg_lighter"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent_purple"]
        )
        reg_username_entry.pack(fill=tk.X, ipady=10, pady=(5, 15))
        reg_username_entry.focus()
        
        reg_pass_icon_frame = tk.Frame(self.login_frame, bg=COLORS["bg_darker"], height=40)
        reg_pass_icon_frame.pack(fill=tk.X)
        
        reg_pass_icon = tk.Label(
            reg_pass_icon_frame,
            text="🔒",
            font=("Segoe UI", 20),
            fg=COLORS["accent_purple"],
            bg=COLORS["bg_darker"]
        )
        reg_pass_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        reg_password_label = tk.Label(
            reg_pass_icon_frame, 
            text="Senha", 
            font=FONTS["body_bold"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"],
            anchor="w"
        )
        reg_password_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        reg_password_entry = tk.Entry(
            self.login_frame,
            textvariable=self.register_password_var,
            font=FONTS["body"],
            bg=COLORS["bg_lighter"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent_purple"],
            show="•"
        )
        reg_password_entry.pack(fill=tk.X, ipady=10, pady=(5, 15))
        
        confirm_pass_icon_frame = tk.Frame(self.login_frame, bg=COLORS["bg_darker"], height=40)
        confirm_pass_icon_frame.pack(fill=tk.X)
        
        confirm_pass_icon = tk.Label(
            confirm_pass_icon_frame,
            text="🔐",
            font=("Segoe UI", 20),
            fg=COLORS["accent_purple"],
            bg=COLORS["bg_darker"]
        )
        confirm_pass_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        confirm_password_label = tk.Label(
            confirm_pass_icon_frame, 
            text="Confirmar Senha", 
            font=FONTS["body_bold"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"],
            anchor="w"
        )
        confirm_password_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        confirm_password_entry = tk.Entry(
            self.login_frame,
            textvariable=self.register_confirm_password_var,
            font=FONTS["body"],
            bg=COLORS["bg_lighter"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent_purple"],
            show="•"
        )
        confirm_password_entry.pack(fill=tk.X, ipady=10, pady=(5, 30))
       
        create_account_container = tk.Frame(self.login_frame, bg=COLORS["bg_darker"], height=70) 
        create_account_container.pack(fill=tk.X, pady=(0, 20))
        create_account_container.pack_propagate(False)

        glow_frame = tk.Frame(
            create_account_container,
            bg=COLORS["accent_green"],
            highlightbackground=COLORS["accent_green"],
            highlightthickness=1,
            bd=0
        )
        glow_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=280, height=66)  
        
        create_account_button = AnimatedButton(
            create_account_container,
            text="CRIAR CONTA",
            command=self.register,
            bg=COLORS["accent_green"],
            hover_bg=COLORS["accent_green_hover"],
            fg=COLORS["bg_darker"],
            font=("Segoe UI", 14, "bold"),  
            padx=20,
            pady=15  
        )
        create_account_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=270, height=60)  
        
        
        def add_icon_to_button():
            icon_label = tk.Label(
                create_account_button,
                text="✚",
                font=("Segoe UI", 14, "bold"),  
                fg=COLORS["bg_darker"],
                bg=COLORS["accent_green"]
            )
            icon_label.place(x=35, rely=0.5, anchor="w") 
            
           
            def update_icon_color(event=None):
                icon_label.config(bg=create_account_button["bg"])
            
            create_account_button.bind("<Enter>", lambda e: update_icon_color())
            create_account_button.bind("<Leave>", lambda e: update_icon_color())
        
        self.login_frame.after(100, add_icon_to_button)
       
        separator_frame = tk.Frame(self.login_frame, bg=COLORS["bg_darker"], height=30)
        separator_frame.pack(fill=tk.X, pady=(10, 10))
        
        separator_line = tk.Frame(separator_frame, bg=COLORS["border"], height=1)
        separator_line.place(relx=0.5, rely=0.5, width=290, anchor="center")
        
        back_button_container = tk.Frame(self.login_frame, bg=COLORS["bg_darker"], height=40)
        back_button_container.pack(fill=tk.X)
        back_button_container.pack_propagate(False)
        
        back_button = ModernButton(
            back_button_container,
            text="← VOLTAR PARA LOGIN",
            command=self.show_login_page,
            bg=COLORS["bg_lighter"],
            hover_bg=COLORS["accent"],
            hover_fg=COLORS["bg_darker"],
            fg=COLORS["text_muted"],
            font=FONTS["body_bold"],
            padx=15,
            pady=8
        )
        back_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=200)
        
        self.root.bind("<Return>", lambda event: create_account_button.invoke())
        self.root.bind("<Escape>", lambda event: back_button.invoke())
    
    def register(self):
        username = self.register_username_var.get().strip()
        password = self.register_password_var.get()
        confirm_password = self.register_confirm_password_var.get()
        
        if not username or not password or not confirm_password:
            self.show_message("Aviso", "Por favor, preencha todos os campos.", "warning")
            return
        
        if password != confirm_password:
            self.show_message("Aviso", "As senhas não coincidem.", "warning")
            return
        
        try:
            with open(self.users_file, "r") as file:
                users = json.load(file)
        except Exception as e:
            self.show_message("Erro", f"Erro ao carregar usuários: {str(e)}", "error")
            return
        
        if username in users:
            self.show_message("Aviso", "Este nome de usuário já está em uso.", "warning")
            return
        
        users[username] = self.hash_password(password)
        
        try:
            with open(self.users_file, "w") as file:
                json.dump(users, file)
            
            self.show_message("Sucesso", "Conta criada com sucesso! Agora você pode fazer login.", "success")
            
            self.username_var.set(username)
            self.password_var.set(password)
            
            self.register_username_var.set("")
            self.register_password_var.set("")
            self.register_confirm_password_var.set("")
            
            self.show_login_page()
            
        except Exception as e:
            self.show_message("Erro", f"Erro ao salvar usuário: {str(e)}", "error")
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            self.show_message("Aviso", "Por favor, preencha todos os campos.", "warning")
            return
        
        try:
            with open(self.users_file, "r") as file:
                users = json.load(file)
        except Exception as e:
            self.show_message("Erro", f"Erro ao carregar usuários: {str(e)}", "error")
            return
        
        hashed_password = self.hash_password(password)
        if username in users and users[username] == hashed_password:
            self.show_message("Sucesso", f"Bem-vindo, {username}!", "success")
            
            self.root.destroy()
            
            self.start_checklist_app(username)
        else:
            self.show_message("Erro", "Usuário ou senha incorretos.", "error")
    
    def show_message(self, title, message, message_type="info"):
        if message_type == "error":
            messagebox.showerror(title, message)
        elif message_type == "warning":
            messagebox.showwarning(title, message)
        elif message_type == "success":
            messagebox.showinfo(title, message)
        else:
            messagebox.showinfo(title, message)
    
    def start_checklist_app(self, username):
        root = tk.Tk()
        app = ChecklistApp(root, username)
        root.mainloop()


class ChecklistApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Checklist - {username}")
        
    
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.state('zoomed') 
        
        self.root.minsize(800, 600)
        self.root.configure(bg=COLORS["bg_dark"])
        
        self.tasks_file = f"checklist_tasks_{username}.json"
        
        self.tasks = []
        
        self.categories = ["Trabalho", "Pessoal", "Estudo", "Saúde", "Finanças", "Outro"]
        
        self.difficulty_levels = ["Fácil", "Médio", "Difícil", "Muito Difícil"]
        self.create_widgets()
        
        self.load_tasks()
    
    def create_widgets(self):
        style = ttk.Style()
        
        style.configure("TCombobox", 
                       background=COLORS["bg_dark"],
                       foreground=COLORS["text"],
                       fieldbackground=COLORS["bg_dark"],
                       arrowcolor=COLORS["accent"])
        
        style.map("TCombobox", 
                 fieldbackground=[("readonly", COLORS["bg_dark"])],
                 selectbackground=[("readonly", COLORS["accent"])],
                 selectforeground=[("readonly", COLORS["bg_darker"])])
        
        self.main_frame = tk.Frame(self.root, bg=COLORS["bg_dark"], padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(self.main_frame, bg=COLORS["bg_dark"])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = tk.Label(
            header_frame, 
            text="Minha Lista de Metas", 
            font=FONTS["header"],
            fg=COLORS["text"],
            bg=COLORS["bg_dark"]
        )
        header_label.pack(side=tk.LEFT)
        
        user_frame = tk.Frame(header_frame, bg=COLORS["bg_dark"])
        user_frame.pack(side=tk.RIGHT)
        
        user_label = tk.Label(
            user_frame, 
            text=f"Olá, {self.username}", 
            font=FONTS["body_bold"],
            fg=COLORS["text"],
            bg=COLORS["bg_dark"]
        )
        user_label.pack(side=tk.LEFT, padx=(0, 15))
        
        logout_button = ModernButton(
            user_frame,
            text="Sair",
            command=self.logout,
            bg=COLORS["bg_lighter"],
            hover_bg=COLORS["bg_lighter"],
            fg=COLORS["text"],
            padx=10
        )
        logout_button.pack(side=tk.RIGHT)
        
        action_frame = tk.Frame(self.main_frame, bg=COLORS["bg_dark"])
        action_frame.pack(fill=tk.X, pady=(0, 15))
        
        add_button = ModernButton(
            action_frame,
            text="+ Nova Meta",
            command=self.show_add_task_dialog,
            bg=COLORS["accent"],
            hover_bg=COLORS["accent_hover"],
            fg=COLORS["bg_darker"]
        )
        add_button.pack(side=tk.LEFT)
        
        save_button = ModernButton(
            action_frame,
            text="Salvar Metas",
            command=self.save_tasks,
            bg=COLORS["accent_green"],
            hover_bg=COLORS["accent_green_hover"],
            fg=COLORS["bg_darker"],
            padx=10
        )
        save_button.pack(side=tk.RIGHT)
        
        filter_frame = tk.Frame(self.main_frame, bg=COLORS["bg_darker"], padx=15, pady=15)
        filter_frame.pack(fill=tk.X, pady=(0, 15))
        
        filter_title = tk.Label(
            filter_frame,
            text="Filtros",
            font=FONTS["body_bold"],
            fg=COLORS["text"],
            bg=COLORS["bg_darker"]
        )
        filter_title.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        category_label = tk.Label(
            filter_frame,
            text="Categoria:",
            font=FONTS["body"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"]
        )
        category_label.grid(row=1, column=0, sticky="w", padx=(0, 10))
        
        self.category_filter_var = tk.StringVar(value="Todas")
        category_filter = ttk.Combobox(
            filter_frame, 
            textvariable=self.category_filter_var,
            values=["Todas"] + self.categories,
            width=12,
            state="readonly"
        )
        category_filter.grid(row=1, column=1, sticky="w", padx=(0, 20))
        category_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        category_filter.configure(background=COLORS["bg_dark"])  
        
        difficulty_label = tk.Label(
            filter_frame,
            text="Dificuldade:",
            font=FONTS["body"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"]
        )
        difficulty_label.grid(row=1, column=2, sticky="w", padx=(0, 10))
        
        self.difficulty_filter_var = tk.StringVar(value="Todas")
        difficulty_filter = ttk.Combobox(
            filter_frame, 
            textvariable=self.difficulty_filter_var,
            values=["Todas"] + self.difficulty_levels,
            width=12,
            state="readonly"
        )
        difficulty_filter.grid(row=1, column=3, sticky="w", padx=(0, 20))
        difficulty_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        difficulty_filter.configure(background=COLORS["bg_dark"])  
        
        status_label = tk.Label(
            filter_frame,
            text="Status:",
            font=FONTS["body"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"]
        )
        status_label.grid(row=1, column=4, sticky="w", padx=(0, 10))
        
        self.status_filter_var = tk.StringVar(value="Todas")
        status_filter = ttk.Combobox(
            filter_frame, 
            textvariable=self.status_filter_var,
            values=["Todas", "Pendentes", "Concluídas"],
            width=12,
            state="readonly"
        )
        status_filter.grid(row=1, column=5, sticky="w")
        status_filter.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        status_filter.configure(background=COLORS["bg_dark"])  
        
        tasks_container = tk.Frame(self.main_frame, bg=COLORS["bg_dark"])
        tasks_container.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(
            tasks_container, 
            bg=COLORS["bg_dark"],
            highlightthickness=0,
            bd=0
        )
        scrollbar = ttk.Scrollbar(tasks_container, orient="vertical", command=self.canvas.yview)
        
        self.tasks_list_frame = tk.Frame(self.canvas, bg=COLORS["bg_dark"])
        self.tasks_list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.tasks_list_frame, anchor="nw", width=self.canvas.winfo_width())
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def on_canvas_configure(event):
            canvas_width = event.width
            self.canvas.itemconfig(1, width=canvas_width)
        
        self.canvas.bind("<Configure>", on_canvas_configure)
    
    def show_add_task_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Adicionar Nova Meta")
        dialog.geometry("500x450")
        dialog.resizable(False, False)
        dialog.configure(bg=COLORS["bg_dark"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        main_frame = tk.Frame(
            dialog, 
            bg=COLORS["bg_darker"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=25,
            pady=25
        )
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=400)
        
        shadow_frame = tk.Frame(
            dialog,
            bg=COLORS["shadow"],
            bd=0
        )
        shadow_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=400, x=5, y=5)
        main_frame.lift()
        
        header_label = tk.Label(
            main_frame, 
            text="Adicionar Nova Meta", 
            font=FONTS["subheader"],
            fg=COLORS["text"],
            bg=COLORS["bg_darker"]
        )
        header_label.pack(pady=(0, 20))
        
        form_frame = tk.Frame(main_frame, bg=COLORS["bg_darker"])
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        desc_label = tk.Label(
            form_frame, 
            text="Descrição da Meta", 
            font=FONTS["body"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"],
            anchor="w"
        )
        desc_label.pack(fill=tk.X)
        
        desc_entry = tk.Entry(
            form_frame,
            font=FONTS["body"],
            bg=COLORS["bg_lighter"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"]
        )
        desc_entry.pack(fill=tk.X, ipady=8, pady=(5, 15))
        desc_entry.focus()
        
        options_frame = tk.Frame(form_frame, bg=COLORS["bg_darker"])
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        category_frame = tk.Frame(options_frame, bg=COLORS["bg_darker"])
        category_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        category_label = tk.Label(
            category_frame, 
            text="Categoria", 
            font=FONTS["body"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"],
            anchor="w"
        )
        category_label.pack(fill=tk.X)
        
        style = ttk.Style()
        style.configure("TCombobox", background=COLORS["bg_lighter"], foreground=COLORS["text"], fieldbackground=COLORS["bg_lighter"], arrowcolor=COLORS["accent"])
        style.map("TCombobox", fieldbackground=[("readonly", COLORS["bg_lighter"])], selectbackground=[("readonly", COLORS["accent"])], selectforeground=[("readonly", COLORS["bg_darker"])])
        
        category_var = tk.StringVar(value=self.categories[0])
        category_combo = ttk.Combobox(
            category_frame, 
            textvariable=category_var,
            values=self.categories,
            state="readonly"
        )
        category_combo.pack(fill=tk.X, pady=(5, 0))
        
        difficulty_frame = tk.Frame(options_frame, bg=COLORS["bg_darker"])
        difficulty_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        difficulty_label = tk.Label(
            difficulty_frame, 
            text="Dificuldade", 
            font=FONTS["body"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"],
            anchor="w"
        )
        difficulty_label.pack(fill=tk.X)
        
        difficulty_var = tk.StringVar(value=self.difficulty_levels[0])
        difficulty_combo = ttk.Combobox(
            difficulty_frame, 
            textvariable=difficulty_var,
            values=self.difficulty_levels,
            state="readonly"
        )
        difficulty_combo.pack(fill=tk.X, pady=(5, 0))
        
        comments_label = tk.Label(
            form_frame, 
            text="Comentários", 
            font=FONTS["body"],
            fg=COLORS["text_muted"],
            bg=COLORS["bg_darker"],
            anchor="w"
        )
        comments_label.pack(fill=tk.X, pady=(0, 5))
        
        comments_text = tk.Text(
            form_frame,
            height=5,
            font=FONTS["body"],
            bg=COLORS["bg_lighter"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"]
        )
        comments_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        button_frame = tk.Frame(form_frame, bg=COLORS["bg_darker"])
        button_frame.pack(fill=tk.X)
        
        def add_task():
            task_text = desc_entry.get().strip()
            if not task_text:
                messagebox.showwarning("Aviso", "Por favor, digite uma descrição para a meta.")
                return
            
            current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
            task = {
                "text": task_text,
                "completed": False,
                "date": current_time,
                "category": category_var.get(),
                "difficulty": difficulty_var.get(),
                "comments": comments_text.get("1.0", tk.END).strip()
            }
            
            self.tasks.append(task)
            self.apply_filters()
            dialog.destroy()
        
        add_button = ModernButton(
            button_frame,
            text="ADICIONAR",
            command=add_task,
            bg=COLORS["accent_green"],
            hover_bg=COLORS["accent_green_hover"],
            fg=COLORS["bg_darker"]
        )
        add_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        cancel_button = ModernButton(
            button_frame,
            text="CANCELAR",
            command=dialog.destroy,
            bg=COLORS["bg_lighter"],
            hover_bg=COLORS["bg_lighter"],
            fg=COLORS["text"]
        )
        cancel_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        dialog.bind("<Return>", lambda event: add_button.invoke())
    
    def apply_filters(self):
        for widget in self.tasks_list_frame.winfo_children():
            widget.destroy()
        
        category_filter = self.category_filter_var.get()
        difficulty_filter = self.difficulty_filter_var.get()
        status_filter = self.status_filter_var.get()
        
        filtered_tasks = []
        for task in self.tasks:
            if status_filter == "Pendentes" and task["completed"]:
                continue
            elif status_filter == "Concluídas" and not task["completed"]:
                continue
                
            if category_filter != "Todas" and task["category"] != category_filter:
                continue
                
            if difficulty_filter != "Todas" and task["difficulty"] != difficulty_filter:
                continue
                
            filtered_tasks.append(task)
        
        if not filtered_tasks:
            empty_frame = tk.Frame(
                self.tasks_list_frame,
                bg=COLORS["bg_darker"],
                padx=20,
                pady=30
            )
            empty_frame.pack(fill=tk.X, pady=10)
            
            empty_label = tk.Label(
                empty_frame,
                text="Nenhuma meta encontrada com os filtros atuais.",
                font=FONTS["body"],
                fg=COLORS["text_muted"],
                bg=COLORS["bg_darker"]
            )
            empty_label.pack()
            
            add_suggestion = tk.Label(
                empty_frame,
                text="Clique em '+ Nova Meta' para adicionar uma meta.",
                font=FONTS["small"],
                fg=COLORS["text_muted"],
                bg=COLORS["bg_darker"]
            )
            add_suggestion.pack()
            
            return
        
        for i, task in enumerate(filtered_tasks):
            original_index = self.tasks.index(task)
            
            category_color = CATEGORY_COLORS.get(task["category"], COLORS["bg_darker"])
            difficulty_color = DIFFICULTY_COLORS.get(task["difficulty"], COLORS["bg_darker"])
            
            task_bg_color = self.blend_colors(category_color, difficulty_color, 0.5)
            
            task_frame = tk.Frame(
                self.tasks_list_frame,
                bg=task_bg_color,
                highlightbackground=COLORS["border"],
                highlightthickness=1,
                padx=15,
                pady=15
            )
            task_frame.pack(fill=tk.X, pady=10, padx=5)
            
            top_frame = tk.Frame(task_frame, bg=task_bg_color)
            top_frame.pack(fill=tk.X)
            
            check_var = tk.BooleanVar(value=task["completed"])
            
            check_frame = tk.Frame(top_frame, bg=task_bg_color, width=30, height=30)
            check_frame.pack(side=tk.LEFT, padx=(0, 10))
            check_frame.pack_propagate(False)
            
            check = tk.Checkbutton(
                check_frame,
                variable=check_var,
                command=lambda i=original_index, v=check_var: self.toggle_task(i, v.get()),
                bg=task_bg_color,
                activebackground=task_bg_color,
                selectcolor=COLORS["bg_lighter"],
                fg=COLORS["accent"],
                bd=0,
                highlightthickness=0
            )
            check.pack(fill=tk.BOTH, expand=True)
            
            category_indicator = tk.Frame(
                top_frame,
                bg=CATEGORY_COLORS.get(task["category"], COLORS["bg_darker"]),
                width=5,
                height=20
            )
            category_indicator.pack(side=tk.LEFT, padx=(0, 10))
            
            if task["completed"]:
                task_label = tk.Label(
                    top_frame, 
                    text=task["text"], 
                    font=(FONTS["body"][0], FONTS["body"][1], "overstrike"),
                    fg=COLORS["text_muted"], 
                    bg=task_bg_color,
                    anchor="w",
                    justify=tk.LEFT,
                    wraplength=600
                )
            else:
                task_label = tk.Label(
                    top_frame, 
                    text=task["text"], 
                    font=FONTS["body_bold"],
                    fg=COLORS["text"], 
                    bg=task_bg_color,
                    anchor="w",
                    justify=tk.LEFT,
                    wraplength=600
                )
            
            task_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            delete_button = tk.Button(
                top_frame, 
                text="×", 
                font=(FONTS["body"][0], 14),
                fg=COLORS["text_muted"],
                bg=task_bg_color,
                activebackground=COLORS["accent_red"],
                activeforeground=COLORS["text"],
                bd=0,
                highlightthickness=0,
                cursor="hand2",
                command=lambda i=original_index: self.delete_task(i)
            )
            delete_button.pack(side=tk.RIGHT)
            
            bottom_frame = tk.Frame(task_frame, bg=task_bg_color)
            bottom_frame.pack(fill=tk.X, pady=(10, 0))
            
            info_frame = tk.Frame(bottom_frame, bg=task_bg_color)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            badges_frame = tk.Frame(info_frame, bg=task_bg_color)
            badges_frame.pack(anchor=tk.W, pady=(0, 5))
            
            category_badge = tk.Label(
                badges_frame,
                text=f" {task['category']} ",
                font=FONTS["tiny"],
                fg=COLORS["text"],
                bg=CATEGORY_COLORS.get(task["category"], COLORS["bg_darker"]),
                padx=5,
                pady=2,
                relief="flat"
            )
            category_badge.pack(side=tk.LEFT, padx=(0, 5))
            
            difficulty_badge = tk.Label(
                badges_frame,
                text=f" {task['difficulty']} ",
                font=FONTS["tiny"],
                fg=COLORS["text"],
                bg=DIFFICULTY_COLORS.get(task["difficulty"], COLORS["bg_darker"]),
                padx=5,
                pady=2,
                relief="flat"
            )
            difficulty_badge.pack(side=tk.LEFT)
            
            date_label = tk.Label(
                info_frame,
                text=f"Criada em: {task['date']}",
                font=FONTS["tiny"],
                fg=COLORS["text_muted"],
                bg=task_bg_color
            )
            date_label.pack(anchor=tk.W)
            
            if task.get("comments"):
                comments_button = ModernButton(
                    bottom_frame,
                    text="Comentários",
                    command=lambda t=task, f=task_frame: self.toggle_comments(t, f),
                    bg=COLORS["bg_lighter"],
                    hover_bg=COLORS["bg_lighter"],
                    fg=COLORS["text"],
                    padx=10,
                    pady=5,
                    font=FONTS["small"]
                )
                comments_button.pack(side=tk.RIGHT)
    
    def blend_colors(self, color1, color2, ratio=0.5):
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        r = int(r1 * ratio + r2 * (1 - ratio))
        g = int(g1 * ratio + g2 * (1 - ratio))
        b = int(b1 * ratio + b2 * (1 - ratio))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def toggle_comments(self, task, parent_frame):
        comments_frame = None
        for child in parent_frame.winfo_children():
            if hasattr(child, 'comments_tag') and child.comments_tag:
                comments_frame = child
                break
        
        if comments_frame:
            comments_frame.destroy()
        else:
            task_bg_color = self.blend_colors(
                CATEGORY_COLORS.get(task["category"], COLORS["bg_darker"]),
                DIFFICULTY_COLORS.get(task["difficulty"], COLORS["bg_darker"]),
                0.5
            )
            
            comments_frame = tk.Frame(
                parent_frame,
                bg=COLORS["bg_lighter"],
                padx=15,
                pady=10
            )
            comments_frame.comments_tag = True
            comments_frame.pack(fill=tk.X, pady=(10, 0))
            
            comments_title = tk.Label(
                comments_frame,
                text="Comentários:",
                font=FONTS["body_bold"],
                fg=COLORS["text"],
                bg=COLORS["bg_lighter"]
            )
            comments_title.pack(anchor=tk.W, pady=(0, 5))
            
            comments_text = tk.Label(
                comments_frame,
                text=task.get("comments", ""),
                font=FONTS["body"],
                fg=COLORS["text"],
                bg=COLORS["bg_lighter"],
                justify=tk.LEFT,
                wraplength=600
            )
            comments_text.pack(anchor=tk.W)
    
    def toggle_task(self, index, completed):
        self.tasks[index]["completed"] = completed
        self.apply_filters()
    
    def delete_task(self, index):
        response = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta meta?")
        if response:
            del self.tasks[index]
            self.apply_filters()
    
    def save_tasks(self):
        try:
            with open(self.tasks_file, "w") as file:
                json.dump(self.tasks, file)
            messagebox.showinfo("Sucesso", "Suas metas foram salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar metas: {str(e)}")
    
    def load_tasks(self):
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, "r") as file:
                    self.tasks = json.load(file)
                
                for task in self.tasks:
                    if "category" not in task:
                        task["category"] = "Outro"
                    if "difficulty" not in task:
                        task["difficulty"] = "Médio"
                    if "comments" not in task:
                        task["comments"] = ""
                
                self.apply_filters()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar metas: {str(e)}")
    
    def logout(self):
        if self.tasks:
            response = messagebox.askyesnocancel("Sair", "Deseja salvar suas metas antes de sair?")
            if response is None:
                return
            if response:
                self.save_tasks()
        
        self.root.destroy()
        
        login_root = tk.Tk()
        login_app = LoginApp(login_root)
        login_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
