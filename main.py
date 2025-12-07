
import tkinter as tk
from tkinter import messagebox, simpledialog


class Client:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def __str__(self):
        return f"{self.name} | Телефон: {self.phone} | Email: {self.email}"


class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.products = []

    def add_product(self, product, price, qty):
        self.products.append({"product": product, "price": price, "qty": qty})

    def total(self):
        return sum(p["price"] * p["qty"] for p in self.products)

    def __str__(self):
        items = ", ".join([f'{p["product"]} x{p["qty"]}' for p in self.products])
        return f"Заказ {self.order_id}: {items} | Сумма: {self.total()} руб."


class StoreManager:
    def __init__(self):
        self.clients = []
        self.orders = []
        self.next_order_id = 1

    def add_client(self, name, phone, email):
        client = Client(name, phone, email)
        self.clients.append(client)
        return client

    def add_order(self, client):
        order = Order(self.next_order_id)
        self.next_order_id += 1
        client.add_order(order)
        self.orders.append(order)
        return order

    def list_clients(self):
        return "\n".join(str(c) for c in self.clients)

    def list_orders(self):
        return "\n".join(str(o) for o in self.orders)

    def find_client(self, name):
        return [c for c in self.clients if name.lower() in c.name.lower()]


class SimpleStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Магазин")
        self.root.geometry("350x200")

        self.manager = StoreManager()

        # Поисковая строка
        tk.Label(root, text="Поиск клиента:").pack(pady=5)

        self.search_entry = tk.Entry(root, width=30)
        self.search_entry.pack(pady=5)

        # Кнопки
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.action_btn = tk.Button(btn_frame, text="Поиск", command=self.search_client, width=15)
        self.action_btn.grid(row=0, column=0, padx=5)

        self.view_btn = tk.Button(btn_frame, text="Просмотр клиентов", command=self.view_clients, width=20)
        self.view_btn.grid(row=0, column=1, padx=5)

    def search_client(self):
        name = self.search_entry.get().strip()
        if not name:
            messagebox.showwarning("Внимание", "Введите имя для поиска")
            return

        found = self.manager.find_client(name)
        if found:
            result = "Найдены клиенты:\n" + "\n".join(str(c) for c in found)
            messagebox.showinfo("Результат поиска", result)
        else:
            if messagebox.askyesno("Клиент не найден", "Хотите добавить нового клиента?"):
                self.add_client()

    def add_client(self):
        name = self.search_entry.get().strip()
        if not name:
            name = simpledialog.askstring("Добавить клиента", "Введите имя:")
            if not name:
                return

        phone = simpledialog.askstring("Добавить клиента", "Введите телефон:")
        if not phone:
            return

        email = simpledialog.askstring("Добавить клиента", "Введите email:")
        if not email:
            return

        self.manager.add_client(name, phone, email)
        messagebox.showinfo("Успех", "Клиент добавлен!")

        if messagebox.askyesno("Добавить заказ", "Хотите добавить заказ для этого клиента?"):
            self.add_order(name)

    def add_order(self, client_name):
        client = next((c for c in self.manager.clients if c.name == client_name), None)
        if not client:
            messagebox.showerror("Ошибка", "Клиент не найден")
            return

        order = self.manager.add_order(client)

        while True:
            product = simpledialog.askstring("Добавить товар", "Название товара (отмена - закончить):")
            if not product:
                break

            try:
                price = float(simpledialog.askstring("Добавить товар", "Цена:"))
                qty = int(simpledialog.askstring("Добавить товар", "Количество:"))
            except (ValueError, TypeError):
                messagebox.showerror("Ошибка", "Неверный формат числа")
                continue

            order.add_product(product, price, qty)

        messagebox.showinfo("Успех", f"Заказ #{order.order_id} добавлен!")

    def view_clients(self):
        if not self.manager.clients:
            messagebox.showinfo("Клиенты", "Клиентов пока нет.")
            return

        win = tk.Toplevel(self.root)
        win.title("Список клиентов")
        win.geometry("500x300")

        listbox = tk.Listbox(win, width=70, height=12)
        listbox.pack(pady=10, padx=10, fill="both", expand=True)

        for idx, client in enumerate(self.manager.clients, start=1):
            listbox.insert(tk.END, f"{idx}. {client}")

        def show_orders(event):
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                client = self.manager.clients[idx]
                if client.orders:
                    orders_text = "\n".join(str(o) for o in client.orders)
                else:
                    orders_text = "У этого клиента пока нет заказов."
                messagebox.showinfo(f"Заказы {client.name}", orders_text)

        listbox.bind("<Double-Button-1>", show_orders)


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleStoreApp(root)
    root.mainloop()
