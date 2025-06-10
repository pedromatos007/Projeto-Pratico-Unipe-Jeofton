import tkinter
import json
import os
from tkinter import messagebox
from datetime import datetime
import hashlib

USERS_FILE = "checklist_users.json"
TASKS_FILE_TEMPLATE = "checklist_tasks_{}.json"

username = ""
tasks = []
window = None
category_filter = "Todas"
difficulty_filter = "Todas"
status_filter = "Todas"

CATEGORIES = ["Trabalho", "Pessoal", "Estudo", "Saúde", "Finanças", "Outro"]
DIFFICULTY = ["Fácil", "Médio", "Difícil", "Muito Difícil"]

def main_screen():
    clear()
    label = tkinter.Label(window, text=f"Bem-vindo, {username}", font=("Arial", 12))
    label.pack(pady=8)
    tkinter.Button(window, text="Nova tarefa", command=add_screen, width=20).pack()
    tkinter.Button(window, text="Salvar tarefas", command=save_tasks, width=20).pack()
    tkinter.Button(window, text="Sair", command=logout, width=20).pack(pady=(0, 10))

    global category_filter, difficulty_filter, status_filter
    tkinter.Label(window, text="Filtros:").pack(pady=(8,0))
    cf = tkinter.StringVar(window, value=category_filter)
    df = tkinter.StringVar(window, value=difficulty_filter)
    sf = tkinter.StringVar(window, value=status_filter)
    tkinter.OptionMenu(window, cf, "Todas", *CATEGORIES, command=lambda x: filter_set('category', x)).pack()
    tkinter.OptionMenu(window, df, "Todas", *DIFFICULTY, command=lambda x: filter_set('difficulty', x)).pack()
    tkinter.OptionMenu(window, sf, "Todas", "Pendentes", "Concluídas", command=lambda x: filter_set('status', x)).pack()
  
    show_tasks()

def filter_set(option, value):
    global category_filter, difficulty_filter, status_filter
    if option == 'category':
        category_filter = value
    elif option == 'difficulty':
        difficulty_filter = value
    elif option == 'status':
        status_filter = value
    main_screen()

def show_tasks():
    filtered = []
    for t in tasks:
        if status_filter == "Pendentes" and t["completed"]:
            continue
        if status_filter == "Concluídas" and not t["completed"]:
            continue
        if category_filter != "Todas" and t["category"] != category_filter:
            continue
        if difficulty_filter != "Todas" and t["difficulty"] != difficulty_filter:
            continue
        filtered.append(t)
    if not filtered:
        tkinter.Label(window, text="Nenhuma tarefa encontrada.", fg="grey").pack()
    for idx, t in enumerate(filtered):
        f = tkinter.Frame(window)
        f.pack(fill="x", pady=2)
        txt = "[Concluída] " if t.get("completed") else ""
        txt += t["text"] + f" | {t['category']} | {t['difficulty']} | {t['date']}"
        tkinter.Label(f, text=txt, anchor="w", width=60).pack(side="left")
        tkinter.Button(f, text="✓" if not t["completed"] else "↺", width=2,
                       command=lambda i=tasks.index(t): toggle_done(i)).pack(side="left")
        tkinter.Button(f, text="X", fg="red", width=2,
                       command=lambda i=tasks.index(t): delete_task(i)).pack(side="left")
        tkinter.Button(f, text="?", width=2,
                       command=lambda text=t.get("comments", ""): messagebox.showinfo("Comentários", text)).pack(side="left")
    
def toggle_done(idx):
    tasks[idx]["completed"] = not tasks[idx]["completed"]
    main_screen()

def delete_task(idx):
    if messagebox.askyesno("Excluir", "Excluir esta tarefa?"):
        tasks.pop(idx)
        main_screen()

def add_screen():
    clear()
    tkinter.Label(window, text="Descrição:").pack()
    desc = tkinter.Entry(window, width=38)
    desc.pack()
    tkinter.Label(window, text="Categoria:").pack()
    cat = tkinter.StringVar(window)
    cat.set(CATEGORIES[0])
    tkinter.OptionMenu(window, cat, *CATEGORIES).pack()
    tkinter.Label(window, text="Dificuldade:").pack()
    diff = tkinter.StringVar(window)
    diff.set(DIFFICULTY[0])
    tkinter.OptionMenu(window, diff, *DIFFICULTY).pack()
    tkinter.Label(window, text="Comentários (opcional):").pack()
    comm = tkinter.Entry(window, width=38)
    comm.pack()
    def add_task():
        text = desc.get().strip()
        if len(text) == 0:
            messagebox.showwarning("Aviso", "Descrição obrigatória.")
            return
        t = {
            "text": text,
            "completed": False,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "category": cat.get(),
            "difficulty": diff.get(),
            "comments": comm.get().strip()
        }
        tasks.append(t)
        main_screen()
    tkinter.Button(window, text="Adicionar", command=add_task, width=20).pack(pady=8)
    tkinter.Button(window, text="Cancelar", command=main_screen, width=20).pack()

def save_tasks():
    if not username: return
    fname = TASKS_FILE_TEMPLATE.format(username)
    json.dump(tasks, open(fname, "w"), ensure_ascii=False)
    messagebox.showinfo("Salvo", "Tarefas salvas.")

def load_tasks():
    global tasks
    fname = TASKS_FILE_TEMPLATE.format(username)
    if os.path.exists(fname):
        with open(fname, "r") as file:
            tasks = json.load(file)
    else:
        tasks = []

def logout():
    global username, tasks
    username = ""
    tasks = []
    login_screen()

def login_screen():
    clear()
    tkinter.Label(window, text="LOGIN", font=("Arial", 15)).pack(pady=(20, 10))
    tkinter.Label(window, text="Usuário:").pack()
    user = tkinter.Entry(window, width=30)
    user.pack()
    tkinter.Label(window, text="Senha:").pack()
    pwd = tkinter.Entry(window, width=30, show="*")
    pwd.pack()
    def log():
        u, p = user.get().strip(), pwd.get()
        if not u or not p:
            messagebox.showwarning("Aviso", "Usuário/senha necessários.")
            return
        us = load_users()
        hp = hashlib.sha256(p.encode()).hexdigest()
        if u in us and us[u] == hp:
            global username
            username = u
            load_tasks()
            main_screen()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
    tkinter.Button(window, text="Entrar", command=log, width=20).pack(pady=8)
    tkinter.Button(window, text="Cadastre-se", command=register_screen, width=20).pack()

def register_screen():
    clear()
    tkinter.Label(window, text="Cadastro", font=("Arial", 15)).pack(pady=(20, 10))
    tkinter.Label(window, text="Usuário:").pack()
    user = tkinter.Entry(window, width=30)
    user.pack()
    tkinter.Label(window, text="Senha:").pack()
    pwd = tkinter.Entry(window, width=30, show="*")
    pwd.pack()
    tkinter.Label(window, text="Confirme a senha:").pack()
    pwd2 = tkinter.Entry(window, width=30, show="*")
    pwd2.pack()
    def reg():
        u, p, p2 = user.get().strip(), pwd.get(), pwd2.get()
        if not u or not p or not p2:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
        if p != p2:
            messagebox.showwarning("Aviso", "Senhas não coincidem.")
            return
        us = load_users()
        if u in us:
            messagebox.showwarning("Aviso", "Usuário já existe.")
            return
        us[u] = hashlib.sha256(p.encode()).hexdigest()
        json.dump(us, open(USERS_FILE, "w"), ensure_ascii=False)
        messagebox.showinfo("Cadastrado", "Conta criada.")
        login_screen()
    tkinter.Button(window, text="Cadastrar", command=reg, width=20).pack(pady=8)
    tkinter.Button(window, text="Voltar", command=login_screen, width=20).pack()

def load_users():
    if not os.path.exists(USERS_FILE):
        json.dump({}, open(USERS_FILE, "w"), ensure_ascii=False)
    with open(USERS_FILE, "r") as file:
        return json.load(file)

def clear():
    for widget in window.winfo_children():
        widget.destroy()

def main():
    global window
    window = tkinter.Tk()
    window.title("Checklist Procedural")
    window.geometry("500x600")
    login_screen()
    window.mainloop()

if __name__ == "__main__":
    main()
