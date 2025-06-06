import tkinter as tk
from tkinter import messagebox, ttk
from auth import signup, login
from product import add_product, view_products, edit_product, delete_product

LOW_STOCK_THRESHOLD = 5  # Used for highlighting low stock items

class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management System")
        self.geometry("700x500")
        self.configure(bg="#f0f0f0")
        self.current_user = None
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if hasattr(self, "current_frame"):
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)


class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        tk.Label(self, text="Login", font=("Segoe UI", 20, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Label(self, text="Username", font=("Segoe UI", 12), bg="#f0f0f0").pack(pady=(10,0))
        self.username_entry = tk.Entry(self, font=("Segoe UI", 12))
        self.username_entry.pack(ipadx=5, ipady=5)

        tk.Label(self, text="Password", font=("Segoe UI", 12), bg="#f0f0f0").pack(pady=(10,0))
        self.password_entry = tk.Entry(self, show="*", font=("Segoe UI", 12))
        self.password_entry.pack(ipadx=5, ipady=5)

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=20, fill="x", padx=50)

        login_btn = tk.Button(btn_frame, text="Login", bg="#0078d7", fg="white", font=("Segoe UI", 14, "bold"),
                              activebackground="#005a9e", cursor="hand2", command=self.perform_login, height=2)
        login_btn.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5)

        signup_btn = tk.Button(btn_frame, text="Sign Up", bg="#28a745", fg="white", font=("Segoe UI", 14, "bold"),
                               activebackground="#1e7e34", cursor="hand2", command=lambda: master.switch_frame(SignupFrame), height=2)
        signup_btn.pack(side="left", fill="x", expand=True, pady=5)

    def perform_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if login(username, password):
            self.master.current_user = username
            self.master.switch_frame(DashboardFrame)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")


class SignupFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        tk.Label(self, text="Sign Up", font=("Segoe UI", 20, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Label(self, text="Username", font=("Segoe UI", 12), bg="#f0f0f0").pack(pady=(10,0))
        self.username_entry = tk.Entry(self, font=("Segoe UI", 12))
        self.username_entry.pack(ipadx=5, ipady=5)

        tk.Label(self, text="Password", font=("Segoe UI", 12), bg="#f0f0f0").pack(pady=(10,0))
        self.password_entry = tk.Entry(self, show="*", font=("Segoe UI", 12))
        self.password_entry.pack(ipadx=5, ipady=5)

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=20, fill="x", padx=50)

        signup_btn = tk.Button(btn_frame, text="Sign Up", bg="#28a745", fg="white", font=("Segoe UI", 14, "bold"),
                               activebackground="#1e7e34", cursor="hand2", command=self.perform_signup, height=2)
        signup_btn.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5)

        back_btn = tk.Button(btn_frame, text="Back to Login", bg="#6c757d", fg="white", font=("Segoe UI", 14, "bold"),
                             activebackground="#5a6268", cursor="hand2", command=lambda: master.switch_frame(LoginFrame), height=2)
        back_btn.pack(side="left", fill="x", expand=True, pady=5)

    def perform_signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if signup(username, password):
            messagebox.showinfo("Success", "Sign-up successful! Please log in.")
            self.master.switch_frame(LoginFrame)
        else:
            messagebox.showerror("Error", "Username already exists")


class DashboardFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        tk.Label(self, text=f"Welcome, {master.current_user}", font=("Segoe UI", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        btn_style = {
            "bg": "#0078d7",
            "fg": "white",
            "font": ("Segoe UI", 14, "bold"),
            "activebackground": "#005a9e",
            "cursor": "hand2",
            "height": 2,
            "bd": 0,
            "relief": "raised",
            "width": 20,
        }

        add_btn = tk.Button(self, text="Add Product", command=self.add_product, **btn_style)
        add_btn.pack(pady=10)

        view_btn = tk.Button(self, text="View Products", command=self.view_products, **btn_style)
        view_btn.pack(pady=10)

        logout_btn = tk.Button(self, text="Logout", command=lambda: master.switch_frame(LoginFrame),
                               bg="#dc3545", activebackground="#a71d2a")
        logout_btn.configure(fg="white", font=("Segoe UI", 14, "bold"), cursor="hand2", height=2, bd=0, relief="raised", width=20)
        logout_btn.pack(pady=10)

    def add_product(self):
        ProductForm(self.master, mode="add").pack(fill="both", expand=True)
        self.destroy()

    def view_products(self):
        ProductList(self.master).pack(fill="both", expand=True)
        self.destroy()


class ProductForm(tk.Frame):
    def __init__(self, master, mode="add", product=None):
        super().__init__(master, bg="#f0f0f0")
        self.mode = mode
        self.product = product

        title_text = "Add Product" if mode == "add" else "Edit Product"
        tk.Label(self, text=title_text, font=("Segoe UI", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(padx=50)

        tk.Label(form_frame, text="Product Name:", font=("Segoe UI", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=10)
        self.name_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=30)
        self.name_entry.grid(row=0, column=1, pady=10)

        tk.Label(form_frame, text="Quantity:", font=("Segoe UI", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=10)
        self.quantity_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=30)
        self.quantity_entry.grid(row=1, column=1, pady=10)

        tk.Label(form_frame, text="Price:", font=("Segoe UI", 12), bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=10)
        self.price_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=30)
        self.price_entry.grid(row=2, column=1, pady=10)

        if mode == "edit" and product:
            self.name_entry.insert(0, product[1])
            self.quantity_entry.insert(0, product[2])
            self.price_entry.insert(0, product[3])

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=20)

        save_btn = tk.Button(btn_frame, text="Save", bg="#28a745", fg="white", font=("Segoe UI", 14, "bold"),
                             activebackground="#1e7e34", cursor="hand2", command=self.save_product, height=2, width=15, bd=0)
        save_btn.pack(side="left", padx=10)

        back_btn = tk.Button(btn_frame, text="Back", bg="#6c757d", fg="white", font=("Segoe UI", 14, "bold"),
                             activebackground="#5a6268", cursor="hand2", command=lambda: self.master.switch_frame(DashboardFrame), height=2, width=15, bd=0)
        back_btn.pack(side="left", padx=10)

    def save_product(self):
        try:
            name = self.name_entry.get().strip()
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())

            if not name:
                messagebox.showerror("Error", "Product name cannot be empty.")
                return
            if quantity < 0 or price < 0:
                messagebox.showerror("Error", "Quantity and price must be non-negative.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity and price.")
            return

        if self.mode == "add":
            add_product(name, quantity, price)
            messagebox.showinfo("Added", "Product added.")
        elif self.mode == "edit":
            edit_product(self.product[0], name, quantity, price)
            messagebox.showinfo("Updated", "Product updated.")

        self.master.switch_frame(DashboardFrame)


class ProductList(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        tk.Label(self, text="Product List", font=("Segoe UI", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Label(self, text="* Double-click a product to edit it.", fg="gray", bg="#f0f0f0", font=("Segoe UI", 10, "italic")).pack()

        columns = ("ID", "Name", "Quantity", "Price")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=15)

        # Style the treeview for better look
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 11), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"))

        products = view_products()
        for p in products:
            id_, name, quantity, price = p
            row_id = self.tree.insert("", "end", values=(id_, name, quantity, f"${price:.2f}"))
            if quantity < LOW_STOCK_THRESHOLD:
                self.tree.item(row_id, tags=("low_stock",))

        self.tree.tag_configure("low_stock", foreground="red")
        self.tree.bind("<Double-1>", self.on_double_click)

        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=15)

        delete_btn = tk.Button(button_frame, text="Delete Selected Product", bg="#dc3545", fg="white",
                               font=("Segoe UI", 14, "bold"), activebackground="#a71d2a",
                               cursor="hand2", command=self.delete_selected_product, height=2, width=25, bd=0)
        delete_btn.grid(row=0, column=0, padx=10)

        back_btn = tk.Button(button_frame, text="Back to Dashboard", bg="#6c757d", fg="white",
                             font=("Segoe UI", 14, "bold"), activebackground="#5a6268",
                             cursor="hand2", command=lambda: master.switch_frame(DashboardFrame), height=2, width=25, bd=0)
        back_btn.grid(row=0, column=1, padx=10)

    def on_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item)["values"]
            ProductForm(self.master, mode="edit", product=item_values).pack(fill="both", expand=True)
            self.destroy()

    def delete_selected_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item)["values"]
            product_id = item_values[0]

            confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete Product ID {product_id}?")
            if confirm:
                delete_product(product_id)
                messagebox.showinfo("Deleted", f"Product ID {product_id} deleted.")
                self.master.switch_frame(ProductList)  # Refresh
        else:
            messagebox.showwarning("No selection", "Please select a product to delete.")


if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
