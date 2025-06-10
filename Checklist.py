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

CATEGORY_COLORS = {
    "Trabalho": "#2d3f50",
    "Pessoal": "#3d3250",
    "Estudo": "#2d4242",
    "Saúde": "#2d4235",
    "Finanças": "#3f3d2d",
    "Outro": "#3d2d3f"
}
DIFFICULTY_COLORS = {
    "Fácil": "#313250",
    "Médio": "#2d2f42",
    "Difícil": "#372d3f",
    "Muito Difícil": "#3a2c36"
}
FONTS = {
    "header": ("Segoe UI", 18, "bold"),
    "subheader": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 10),
    "body_bold": ("Segoe UI", 10, "bold"),
    "small": ("Segoe UI", 9),
    "tiny": ("Segoe UI", 8)
}
CATEGORIES = ["Trabalho", "Pessoal", "Estudo", "Saúde", "Finanças", "Outro"]
DIFFICULTY_LEVELS = ["Fácil", "Médio", "Difícil", "Muito Difícil"]

root = None
username_var = None
password_var = None
register_username_var = None
register_password_var = None
register_confirm_password_var = None
users_file = "checklist_users.json"
tasks_file = ""
tasks = []
username_global = ""
category_filter_var = None
difficulty_filter_var = None
status_filter_var = None
task_widgets = []
main_vars = {}
canvas = None
tasks_list_frame = None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(users_file):
        with open(users_file, "w") as file:
            json.dump({}, file)
    with open(users_file, "r") as file:
        return json.load(file)

def save_users(users):
    with open(users_file, "w") as file:
        json.dump(users, file)

def login():
    username = username_var.get().strip()
    password = password_var.get()
    if not username or not password:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
        return
    users = load_users()
    hashed = hash_password(password)
    if username in users and users[username] == hashed:
        show_main(username)
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

def register():
    username = register_username_var.get().strip()
    password = register_password_var.get()
    confirm = register_confirm_password_var.get()
    if not username or not password or not confirm:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
        return
    if password != confirm:
        messagebox.showwarning("Aviso", "As senhas não coincidem.")
        return
    users = load_users()
    if username in users:
        messagebox.showwarning("Aviso", "Este nome de usuário já está em uso.")
        return
    users[username] = hash_password(password)
    save_users(users)
    messagebox.showinfo("Sucesso", "Conta criada! Faça login.")
    show_login()

def clear_window(frame_ref=None):
    fr = frame_ref if frame_ref else root
    for widget in fr.winfo_children():
        widget.destroy()

def show_login():
    clear_window()
    global username_var, password_var
    username_var = tk.StringVar()
    password_var = tk.StringVar()
    frame = tk.Frame(root, bg=COLORS["bg_darker"], padx=30, pady=30)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=700)
    tk.Label(frame, text="Gerenciador de Metas", font=FONTS["header"], bg=COLORS["bg_darker"], fg=COLORS["text"]).pack(pady=(20,10))
    tk.Label(frame, text="Usuário", font=FONTS["body_bold"],bg=COLORS["bg_darker"], fg=COLORS["text_muted"]).pack(anchor="w")
    tk.Entry(frame, textvariable=username_var, font=FONTS["body"],
             bg=COLORS["bg_lighter"], fg=COLORS["text"], relief="flat").pack(fill=tk.X, ipady=10, pady=(0,14))
    tk.Label(frame, text="Senha", font=FONTS["body_bold"],bg=COLORS["bg_darker"], fg=COLORS["text_muted"]).pack(anchor="w")
    tk.Entry(frame, textvariable=password_var, font=FONTS["body"],
             bg=COLORS["bg_lighter"], fg=COLORS["text"], show="•", relief="flat").pack(fill=tk.X, ipady=10, pady=(0,24))
    login_btn = tk.Button(frame, text="Entrar", bg=COLORS["accent_green"], fg=COLORS["bg_darker"], font=FONTS["body_bold"], command=login)
    login_btn.pack(fill=tk.X, ipady=10)
    tk.Label(frame, text="Não tem conta?", bg=COLORS["bg_darker"], fg=COLORS["text_muted"], font=FONTS["small"]).pack(pady=(30,15))
    tk.Button(frame, text="Criar Conta", bg=COLORS["accent_purple"], fg=COLORS["bg_darker"], font=FONTS["body_bold"],
              command=show_register).pack(fill=tk.X, ipady=10)
    root.bind('<Return>', lambda e: login_btn.invoke())

def show_register():
    clear_window()
    global register_username_var, register_password_var, register_confirm_password_var
    register_username_var = tk.StringVar()
    register_password_var = tk.StringVar()
    register_confirm_password_var = tk.StringVar()
    frame = tk.Frame(root, bg=COLORS["bg_darker"], padx=30, pady=30)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=700)
    tk.Label(frame, text="Criar Nova Conta", font=FONTS["header"], bg=COLORS["bg_darker"], fg=COLORS["accent_purple"]).pack(pady=(20,12))
    tk.Label(frame, text="Usuário", font=FONTS["body_bold"],bg=COLORS["bg_darker"], fg=COLORS["text_muted"]).pack(anchor="w")
    tk.Entry(frame, textvariable=register_username_var, font=FONTS["body"],bg=COLORS["bg_lighter"], fg=COLORS["text"], relief="flat").pack(fill=tk.X, ipady=10, pady=(0,10))
    tk.Label(frame, text="Senha", font=FONTS["body_bold"],bg=COLORS["bg_darker"], fg=COLORS["text_muted"]).pack(anchor="w")
    tk.Entry(frame, textvariable=register_password_var, font=FONTS["body"],bg=COLORS["bg_lighter"], fg=COLORS["text"], relief="flat", show="•").pack(fill=tk.X, ipady=10, pady=(0,10))
    tk.Label(frame, text="Confirmar Senha", font=FONTS["body_bold"],bg=COLORS["bg_darker"], fg=COLORS["text_muted"]).pack(anchor="w")
    tk.Entry(frame, textvariable=register_confirm_password_var, font=FONTS["body"],bg=COLORS["bg_lighter"], fg=COLORS["text"], relief="flat", show="•").pack(fill=tk.X, ipady=10, pady=(0,15))
    reg_btn = tk.Button(frame, text="Criar Conta", bg=COLORS["accent_green"], fg=COLORS["bg_darker"], font=FONTS["body_bold"], command=register)
    reg_btn.pack(fill=tk.X, ipady=10)
    tk.Button(frame, text="Voltar", bg=COLORS["bg_lighter"], fg=COLORS["text_muted"], font=FONTS["body"],
              command=show_login).pack(fill=tk.X, ipady=7, pady=(30,0))
    root.bind('<Return>', lambda e: reg_btn.invoke())

def show_main(username):
    global username_global, tasks_file, tasks, category_filter_var, difficulty_filter_var, status_filter_var, canvas, tasks_list_frame
    clear_window()
    username_global = username
    tasks_file = f"checklist_tasks_{username_global}.json"
    tasks = []
    frame = tk.Frame(root, bg=COLORS["bg_dark"], padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    header_frame = tk.Frame(frame, bg=COLORS["bg_dark"])
    header_frame.pack(fill=tk.X)
    tk.Label(header_frame, text="Minha Lista de Metas", font=FONTS["header"], fg=COLORS["text"], bg=COLORS["bg_dark"]).pack(side=tk.LEFT)
    tk.Label(header_frame, text=f"Olá, {username_global}", font=FONTS["body_bold"], fg=COLORS["text"], bg=COLORS["bg_dark"]).pack(side=tk.RIGHT)
    btn_frame = tk.Frame(frame, bg=COLORS["bg_dark"])
    btn_frame.pack(fill=tk.X, pady=(0,12))
    tk.Button(btn_frame, text="+ Nova Meta", bg=COLORS["accent"], fg=COLORS["bg_darker"], font=FONTS["body_bold"], command=add_task_dialog).pack(side=tk.LEFT)
    tk.Button(btn_frame, text="Salvar Metas", bg=COLORS["accent_green"], fg=COLORS["bg_darker"], font=FONTS["body_bold"], command=save_tasks).pack(side=tk.RIGHT)
    tk.Button(btn_frame, text="Sair", bg=COLORS["bg_lighter"], fg=COLORS["text"], font=FONTS["body_bold"], command=logout).pack(side=tk.RIGHT, padx=(0,10))
    filter_frame = tk.Frame(frame, bg=COLORS["bg_darker"], padx=15, pady=10)
    filter_frame.pack(fill=tk.X)
    tk.Label(filter_frame, text="Filtros", font=FONTS["body_bold"], fg=COLORS["text"], bg=COLORS["bg_darker"]).grid(row=0, column=0)
    category_filter_var = tk.StringVar(value="Todas")
    difficulty_filter_var = tk.StringVar(value="Todas")
    status_filter_var = tk.StringVar(value="Todas")
    ttk.Combobox(filter_frame, values=["Todas"]+CATEGORIES, textvariable=category_filter_var, state="readonly", width=12).grid(row=1,column=1)
    ttk.Combobox(filter_frame, values=["Todas"]+DIFFICULTY_LEVELS, textvariable=difficulty_filter_var, state="readonly", width=12).grid(row=1,column=3)
    ttk.Combobox(filter_frame, values=["Todas", "Pendentes", "Concluídas"], textvariable=status_filter_var, state="readonly", width=12).grid(row=1,column=5)
    tk.Label(filter_frame, text="Categoria:", font=FONTS["body"], fg=COLORS["text_muted"], bg=COLORS["bg_darker"]).grid(row=1,column=0)
    tk.Label(filter_frame, text="Dificuldade:", font=FONTS["body"], fg=COLORS["text_muted"], bg=COLORS["bg_darker"]).grid(row=1,column=2)
    tk.Label(filter_frame, text="Status:", font=FONTS["body"], fg=COLORS["text_muted"], bg=COLORS["bg_darker"]).grid(row=1,column=4)
    category_filter_var.trace_add('write', lambda *args: apply_filters())
    difficulty_filter_var.trace_add('write', lambda *args: apply_filters())
    status_filter_var.trace_add('write', lambda *args: apply_filters())
    tasks_container = tk.Frame(frame, bg=COLORS["bg_dark"])
    tasks_container.pack(fill=tk.BOTH, expand=True)
    canvas = tk.Canvas(tasks_container, bg=COLORS["bg_dark"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(tasks_container, orient="vertical", command=canvas.yview)
    tasks_list_frame = tk.Frame(canvas, bg=COLORS["bg_dark"])
    canvas.create_window((0,0), window=tasks_list_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tasks_list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    load_tasks()
    apply_filters()

def add_task_dialog():
    global CATEGORIES, DIFFICULTY_LEVELS, tasks
    dialog = tk.Toplevel(root)
    dialog.title("Adicionar Nova Meta")
    dialog.geometry("400x340")
    dialog.configure(bg=COLORS["bg_dark"])
    desc_var = tk.StringVar()
    cat_var = tk.StringVar(value=CATEGORIES[0])
    dif_var = tk.StringVar(value=DIFFICULTY_LEVELS[0])
    tk.Label(dialog, text="Descrição", font=FONTS["body"],bg=COLORS["bg_dark"], fg=COLORS["text"]).pack(anchor="w")
    ent = tk.Entry(dialog, textvariable=desc_var, font=FONTS["body"], bg=COLORS["bg_lighter"], fg=COLORS["text"], relief="flat")
    ent.pack(fill=tk.X, ipady=8, pady=(0,8))
    ent.focus()
    tk.Label(dialog, text="Categoria", font=FONTS["body"],bg=COLORS["bg_dark"], fg=COLORS["text"]).pack(anchor="w")
    ttk.Combobox(dialog, values=CATEGORIES, textvariable=cat_var, state="readonly").pack(fill=tk.X, pady=(0,7))
    tk.Label(dialog, text="Dificuldade", font=FONTS["body"],bg=COLORS["bg_dark"], fg=COLORS["text"]).pack(anchor="w")
    ttk.Combobox(dialog, values=DIFFICULTY_LEVELS, textvariable=dif_var, state="readonly").pack(fill=tk.X, pady=(0,7))
    tk.Label(dialog, text="Comentários", font=FONTS["body"], bg=COLORS["bg_dark"], fg=COLORS["text"]).pack(anchor="w")
    comm_text = tk.Text(dialog, height=3, font=FONTS["body"], bg=COLORS["bg_lighter"], fg=COLORS["text"])
    comm_text.pack(fill=tk.X)
    def add():
        desc = desc_var.get().strip()
        if not desc:
            messagebox.showwarning("Aviso", "Descrição obrigatória.")
            return
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        task = {"text": desc, "completed": False, "date": now,
                "category": cat_var.get(), "difficulty": dif_var.get(),
                "comments": comm_text.get("1.0", tk.END).strip()}
        tasks.append(task)
        apply_filters()
        dialog.destroy()
    tk.Button(dialog, text="Adicionar", bg=COLORS["accent_green"], fg=COLORS["bg_darker"], font=FONTS["body_bold"], command=add).pack(side=tk.LEFT, padx=(20,10), pady=16)
    tk.Button(dialog, text="Cancelar", bg=COLORS["bg_lighter"], fg=COLORS["text"], font=FONTS["body"], command=dialog.destroy).pack(side=tk.RIGHT, padx=(10,20), pady=16)
    dialog.bind('<Return>', lambda e: add())

def apply_filters():
    global tasks_list_frame, tasks
    for widget in tasks_list_frame.winfo_children():
        widget.destroy()
    cat = category_filter_var.get() if category_filter_var else "Todas"
    dif = difficulty_filter_var.get() if difficulty_filter_var else "Todas"
    stat = status_filter_var.get() if status_filter_var else "Todas"
    filtered = []
    for t in tasks:
        if stat == "Pendentes" and t["completed"]: continue
        if stat == "Concluídas" and not t["completed"]: continue
        if cat != "Todas" and t["category"] != cat: continue
        if dif != "Todas" and t["difficulty"] != dif: continue
        filtered.append(t)
    if not filtered:
        tk.Label(tasks_list_frame, text="Nenhuma meta encontrada com os filtros atuais.", bg=COLORS["bg_darker"], fg=COLORS["text_muted"], font=FONTS["body"]).pack(fill="x", pady=10)
        tk.Label(tasks_list_frame, text="Clique em '+ Nova Meta' para adicionar.", bg=COLORS["bg_darker"], fg=COLORS["text_muted"], font=FONTS["tiny"]).pack()
        return
    for i, t in enumerate(filtered):
        idx = tasks.index(t)
        frame = tk.Frame(tasks_list_frame, bg=COLORS["bg_lighter"], padx=10, pady=10)
        frame.pack(fill=tk.X, pady=5)
        check_var = tk.BooleanVar(value=t["completed"])
        tk.Checkbutton(frame, variable=check_var, bg=COLORS["bg_lighter"], command=lambda i=idx, v=check_var: on_toggle(i, v.get())).pack(side=tk.LEFT)
        txt = t["text"]
        fg = COLORS["text_muted"] if t["completed"] else COLORS["text"]
        tk.Label(frame, text=txt, font=FONTS["body"], fg=fg, bg=COLORS["bg_lighter"]).pack(side=tk.LEFT, padx=8)
        tk.Label(frame, text=f"[{t['category']}, {t['difficulty']}] {t['date']}", font=FONTS["tiny"], fg=COLORS["text_muted"], bg=COLORS["bg_lighter"]).pack(side=tk.LEFT, padx=6)
        tk.Button(frame, text="Excluir", font=FONTS["tiny"], bg=COLORS["accent_red"], fg=COLORS["bg_lighter"], command=lambda i=idx: delete_task(i)).pack(side=tk.RIGHT)
        if t.get("comments"):
            tk.Button(frame, text="Ver Comentários", font=FONTS["tiny"], bg=COLORS["accent"], fg=COLORS["bg_lighter"], command=lambda t=t: messagebox.showinfo("Comentários", t["comments"])).pack(side=tk.RIGHT, padx=5)

def on_toggle(index, completed):
    tasks[index]["completed"] = completed
    apply_filters()

def delete_task(index):
    if messagebox.askyesno("Excluir", "Deseja realmente excluir esta meta?"):
        del tasks[index]
        apply_filters()

def save_tasks():
    if not tasks_file:
        return
    with open(tasks_file, "w") as file:
        json.dump(tasks, file)
    messagebox.showinfo("Salvo", "Suas metas foram salvas!")

def load_tasks():
    if not tasks_file or not os.path.exists(tasks_file):
        return
    global tasks
    with open(tasks_file, "r") as file:
        tasks = json.load(file)
    apply_filters()

def logout():
    if messagebox.askyesnocancel("Sair", "Deseja salvar suas metas antes de sair?"):
        save_tasks()
    show_login()

def main():
    global root
    root = tk.Tk()
    root.title("Checklist")
    root.geometry("500x700")
    root.configure(bg=COLORS["bg_dark"])
    show_login()
    root.mainloop()

if __name__ == "__main__":
    main()
