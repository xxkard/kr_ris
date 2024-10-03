import sqlite3
import tkinter
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime

root = tk.Tk()

# Підключення до бази даних
conn = sqlite3.connect('exchange_db.db')
c = conn.cursor()

# Створення таблиць
c.execute("""CREATE TABLE IF NOT EXISTS Cashier (
    cashier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone_number TEXT,
    email TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Currency (
    currency_id INTEGER PRIMARY KEY AUTOINCREMENT,
    c_name TEXT,
    exchange_rate REAL,
    cur_amount BOOLEAN
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Exchange (
    exchange_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cashier_id INTEGER,
    currency_from_id INTEGER,
    currency_to_id INTEGER,
    amount_to REAL,
    commission REAL,
    tax REAL,
    full_amount REAL,
    exchange_info TEXT,
    FOREIGN KEY (cashier_id) REFERENCES Cashier(cashier_id),
    FOREIGN KEY (currency_from_id) REFERENCES Currency(currency_id),
    FOREIGN KEY (currency_to_id) REFERENCES Currency(currency_id)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Receipt (
    receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exchange_id INTEGER,
    date DATE,
    time TIME,
    name TEXT,
    FOREIGN KEY (exchange_id) REFERENCES Exchange(exchange_id)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Commission (
    commission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rate REAL,
    c_amount REAL
)""")

c.execute("""CREATE TABLE IF NOT EXISTS Tax (
    tax_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rate REAL,
    t_amount REAL
)""")

conn.commit()


class Register:
    @staticmethod
    def add_exchange(cashier_id, currency_from_id, currency_to_id, amount_to, commission, tax, full_amount, exchange_info):
        exchange = Exchange(cashier_id=cashier_id, currency_from_id=currency_from_id, currency_to_id=currency_to_id, amount_to=amount_to, commission=commission, tax=tax, full_amount=full_amount, exchange_info=exchange_info)
        exchange.save()
        return exchange

    @staticmethod
    def get_receipt(exchange_id, date, time, name):
        receipt = Receipt(exchange_id=exchange_id, date=date, time=time, name=name)
        receipt.save()
        return receipt


# Клас Cashier
class Cashier:
    def __init__(self, cashier_id=None, name=None, phone_number=None, email=None):
        self.cashier_id = cashier_id
        self.name = name
        self.phone_number = phone_number
        self.email = email

    def save(self):
        if self.cashier_id:
            c.execute("""UPDATE Cashier SET name=?, phone_number=?, email=?
                        WHERE cashier_id=?""", (self.name, self.phone_number, self.email, self.cashier_id))
        else:
            c.execute("""INSERT INTO Cashier (name, phone_number, email)
                        VALUES (?, ?, ?)""", (self.name, self.phone_number, self.email))
        conn.commit()

    def delete(self):
        if self.cashier_id:
            c.execute("""DELETE FROM Cashier WHERE cashier_id=?""", (self.cashier_id,))
            conn.commit()


# Клас Currency
class Currency:
    def __init__(self, currency_id=None, c_name=None, exchange_rate=None, cur_amount=None):
        self.currency_id = currency_id
        self.c_name = c_name
        self.exchange_rate = exchange_rate
        self.cur_amount = cur_amount

    def save(self):
        if self.currency_id:
            c.execute("""UPDATE Currency SET c_name=?, exchange_rate=?, cur_amount=? WHERE currency_id=?""",
                      (self.c_name, self.exchange_rate, self.cur_amount, self.currency_id))
        else:
            c.execute("""INSERT INTO Currency (c_name, exchange_rate, cur_amount) VALUES (?, ?, ?)""",
                      (self.c_name, self.exchange_rate, self.cur_amount))
        conn.commit()

    def delete(self):
        c.execute("""DELETE FROM Currency WHERE currency_id=?""", (self.currency_id,))
        conn.commit()


# Клас Exchange
class Exchange:
    def __init__(self, exchange_id=None, cashier_id=None, currency_from_id=None, currency_to_id=None, amount_to=None, commission=None, tax=None, full_amount=None, exchange_info=None):
        self.exchange_id = exchange_id
        self.cashier_id = cashier_id
        self.currency_from_id = currency_from_id
        self.currency_to_id = currency_to_id
        self.amount_to = amount_to
        self.commission = commission
        self.tax = tax
        self.full_amount = full_amount
        self.exchange_info = exchange_info

    def save(self):
        if self.exchange_id:  # Update existing record
            c.execute("""UPDATE Exchange SET cashier_id=?, currency_from_id=?, currency_to_id=?, amount_to=?, commission=?, tax=?, full_amount=?, exchange_info=? WHERE exchange_id=?""",
                      (self.cashier_id, self.currency_from_id, self.currency_to_id, self.amount_to, self.commission, self.tax, self.full_amount, self.exchange_info, self.exchange_id))
        else:  # Insert new record
            c.execute("""INSERT INTO Exchange (cashier_id, currency_from_id, currency_to_id, amount_to, commission, tax, full_amount, exchange_info) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                      (self.cashier_id, self.currency_from_id, self.currency_to_id, self.amount_to, self.commission, self.tax, self.full_amount, self.exchange_info))
        conn.commit()

    def delete(self):
        c.execute("""DELETE FROM Exchange WHERE exchange_id=?""", (self.exchange_id,))
        conn.commit()


# Клас Receipt
class Receipt:
    def __init__(self, receipt_id=None, exchange_id=None, date=None, time=None, name=None):
        self.receipt_id = receipt_id
        self.exchange_id = exchange_id
        self.date = date
        self.time = time
        self.name = name

    def save(self):
        if self.receipt_id:
            c.execute("""UPDATE Receipt SET exchange_id=?, date=?, time=?, name=?
                        WHERE receipt_id=?""", (self.exchange_id, self.date, self.time, self.name, self.receipt_id))
        else:
            c.execute("""INSERT INTO Receipt (exchange_id, date, time, name)
                        VALUES (?, ?, ?, ?)""", (self.exchange_id, self.date, self.time, self.name))
        conn.commit()

    def delete(self):
        if self.receipt_id:
            c.execute("""DELETE FROM Receipt WHERE receipt_id=?""", (self.receipt_id,))
            conn.commit()


# Клас Commission
class Commission:
    def __init__(self, commission_id=None, rate=None, c_amount=None):
        self.commission_id = commission_id
        self.rate = rate
        self.c_amount = c_amount

    def save(self):
        if self.commission_id:
            c.execute("""UPDATE Commission SET rate=?, c_amount=?
                        WHERE commission_id=?""", (self.rate, self.c_amount, self.commission_id))
        else:
            c.execute("""INSERT INTO Commission (rate, c_amount)
                        VALUES (?, ?)""", (self.rate, self.c_amount))
        conn.commit()

    def delete(self):
        if self.commission_id:
            c.execute("""DELETE FROM Commission WHERE commission_id=?""", (self.commission_id,))
            conn.commit()


# Клас Tax
class Tax:
    def __init__(self, tax_id=None, rate=None, t_amount=None):
        self.tax_id = tax_id
        self.rate = rate
        self.t_amount = t_amount

    def save(self):
        if self.tax_id:
            c.execute("""UPDATE Tax SET rate=?, t_amount=?
                        WHERE tax_id=?""", (self.rate, self.t_amount, self.tax_id))
        else:
            c.execute("""INSERT INTO Tax (rate, t_amount)
                        VALUES (?, ?)""", (self.rate, self.t_amount))
        conn.commit()

    def delete(self):
        if self.tax_id:
            c.execute("""DELETE FROM Tax WHERE tax_id=?""", (self.tax_id,))
            conn.commit()


# Функції для роботи з Cashier
def is_valid_phone_number(phone_number):
    return re.fullmatch(r'\d{10}', phone_number) is not None

def add_cashier():
    def save_cashier():
        name = name_entry.get()
        phone_number = phone_number_entry.get()
        email = email_entry.get()

        if not (name and phone_number and email):  # Перевірка, чи всі поля заповнені
            messagebox.showerror("Помилка", "Будь ласка, заповніть усі поля вводу.")
            return

        if not is_valid_phone_number(phone_number):
            messagebox.showerror("Помилка", "Номер телефону має складатися з 10 цифр")
            return

        cashier = Cashier(name=name, phone_number=phone_number, email=email)
        cashier.save()
        cashier_window.destroy()
        update_cashier_listbox(cashier_tree)

    cashier_window = tk.Toplevel(root)
    cashier_window.title('Додати касира')

    name_label = tk.Label(cashier_window, text='Ім\'я:')
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(cashier_window)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    phone_number_label = tk.Label(cashier_window, text='Номер телефону:')
    phone_number_label.grid(row=1, column=0, padx=5, pady=5)
    phone_number_entry = tk.Entry(cashier_window)
    phone_number_entry.grid(row=1, column=1, padx=5, pady=5)

    email_label = tk.Label(cashier_window, text='Електронна пошта:')
    email_label.grid(row=2, column=0, padx=5, pady=5)
    email_entry = tk.Entry(cashier_window)
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    save_button = tk.Button(cashier_window, text='Зберегти', command=save_cashier)
    save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)


def edit_cashier(cashier_tree):
    selected_item = cashier_tree.selection()
    if selected_item:
        cashier_id = cashier_tree.item(selected_item[0], 'values')[0]
        c.execute("""SELECT * FROM Cashier WHERE cashier_id =?""", (cashier_id,))
        cashier_data = c.fetchone()
        if cashier_data:
            def save_cashier():
                name = name_entry.get()
                phone_number = phone_number_entry.get()
                email = email_entry.get()

                if not is_valid_phone_number(phone_number):
                    messagebox.showerror("Помилка", "Номер телефону має складатися з 10 цифр")
                    return

                cashier = Cashier(cashier_id=cashier_id, name=name, phone_number=phone_number, email=email)
                cashier.save()
                cashier_window.destroy()
                update_cashier_listbox(cashier_tree)

            cashier_window = tk.Toplevel(root)
            cashier_window.title('Редагувати касира')

            name_label = tk.Label(cashier_window, text='Ім\'я:')
            name_label.grid(row=0, column=0, padx=5, pady=5)
            name_entry = tk.Entry(cashier_window)
            name_entry.insert(0, str(cashier_data[1]))
            name_entry.grid(row=0, column=1, padx=5, pady=5)

            phone_number_label = tk.Label(cashier_window, text='Номер телефону:')
            phone_number_label.grid(row=1, column=0, padx=5, pady=5)
            phone_number_entry = tk.Entry(cashier_window)
            phone_number_entry.insert(0, str(cashier_data[2]))
            phone_number_entry.grid(row=1, column=1, padx=5, pady=5)

            email_label = tk.Label(cashier_window, text='Електронна пошта:')
            email_label.grid(row=2, column=0, padx=5, pady=5)
            email_entry = tk.Entry(cashier_window)
            email_entry.insert(0, str(cashier_data[3]))
            email_entry.grid(row=2, column=1, padx=5, pady=5)

            save_button = tk.Button(cashier_window, text='Зберегти', command=save_cashier)
            save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    else:
        messagebox.showwarning('Попередження', 'Виберіть касира для редагування')


def delete_cashier(tree):
    selected_item = tree.selection()
    if selected_item:
        cashier_id = tree.item(selected_item[0], 'values')[0]
        if messagebox.askyesno('Підтвердження', 'Ви дійсно бажаєте видалити касира?'):
            cashier = Cashier(cashier_id=cashier_id)
            cashier.delete()
            update_cashier_listbox(tree)
    else:
        messagebox.showwarning('Попередження', 'Виберіть касира для видалення')


# Оновлена функція для заповнення Treeview
def update_cashier_listbox(treeview):
    for row in treeview.get_children():
        treeview.delete(row)
    c.execute("""SELECT cashier_id, name, phone_number, email FROM Cashier""")
    cashiers = c.fetchall()
    for cashier in cashiers:
        treeview.insert('', tk.END, values=cashier)


# Функції для роботи з Currency
cur_amount_var = tk.BooleanVar(value=True)

def add_currency():
    def save_currency():
        c_name = c_name_entry.get()
        exchange_rate = exchange_rate_entry.get()
        cur_amount = cur_amount_var.get()

        try:
            exchange_rate = float(exchange_rate)
        except ValueError:
            messagebox.showerror("Помилка", "Курс обміну має бути числом")
            return

        currency = Currency(c_name=c_name, exchange_rate=exchange_rate, cur_amount=cur_amount)
        currency.save()
        currency_window.destroy()
        update_currency_listbox(currency_tree)

    currency_window = tk.Toplevel(root)
    currency_window.title('Додати валюту')

    c_name_label = tk.Label(currency_window, text='Назва валюти:')
    c_name_label.grid(row=0, column=0, padx=5, pady=5)
    c_name_entry = tk.Entry(currency_window)
    c_name_entry.grid(row=0, column=1, padx=5, pady=5)

    exchange_rate_label = tk.Label(currency_window, text='Курс обміну:')
    exchange_rate_label.grid(row=1, column=0, padx=5, pady=5)
    exchange_rate_entry = tk.Entry(currency_window)
    exchange_rate_entry.grid(row=1, column=1, padx=5, pady=5)

    cur_amount_label = tk.Label(currency_window, text='Доступна кількість:')
    cur_amount_label.grid(row=2, column=0, padx=5, pady=5)
    cur_amount_var = tk.BooleanVar()
    cur_amount_checkbutton = tk.Checkbutton(currency_window, variable=cur_amount_var)
    cur_amount_checkbutton.grid(row=2, column=1, padx=5, pady=5)

    save_button = tk.Button(currency_window, text='Зберегти', command=save_currency)
    save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

def edit_currency(currency_tree):
    selected_item = currency_tree.selection()
    if selected_item:
        currency_id = currency_tree.item(selected_item[0], 'values')[0]
        c.execute("""SELECT * FROM Currency WHERE currency_id=?""", (currency_id,))
        currency_data = c.fetchone()
        if currency_data:
            def save_currency():
                c_name = c_name_entry.get()
                exchange_rate = exchange_rate_entry.get()
                cur_amount = cur_amount_var.get()

                try:
                    exchange_rate = float(exchange_rate)
                except ValueError:
                    messagebox.showerror("Помилка", "Курс обміну має бути числом")
                    return

                currency = Currency(currency_id=currency_id, c_name=c_name, exchange_rate=exchange_rate, cur_amount=cur_amount)
                currency.save()
                currency_window.destroy()
                update_currency_listbox(currency_tree)

            currency_window = tk.Toplevel(root)
            currency_window.title('Редагувати валюту')

            c_name_label = tk.Label(currency_window, text='Назва:')
            c_name_label.grid(row=0, column=0, padx=5, pady=5)
            c_name_entry = tk.Entry(currency_window)
            c_name_entry.insert(0, currency_data[1])
            c_name_entry.grid(row=0, column=1, padx=5, pady=5)

            exchange_rate_label = tk.Label(currency_window, text='Курс обміну:')
            exchange_rate_label.grid(row=1, column=0, padx=5, pady=5)
            exchange_rate_entry = tk.Entry(currency_window)
            exchange_rate_entry.insert(0, currency_data[2])
            exchange_rate_entry.grid(row=1, column=1, padx=5, pady=5)

            cur_amount_label = tk.Label(currency_window, text='Доступна кількість:')
            cur_amount_label.grid(row=2, column=0, padx=5, pady=5)
            cur_amount_var = tk.BooleanVar(currency_window, value=currency_data[3])
            cur_amount_checkbutton = tk.Checkbutton(currency_window, variable=cur_amount_var)
            cur_amount_checkbutton.grid(row=2, column=1, padx=5, pady=5)

            save_button = tk.Button(currency_window, text='Зберегти', command=save_currency)
            save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    else:
        messagebox.showwarning('Попередження', 'Виберіть валюту для редагування')

def delete_currency(currency_tree):
    selected_item = currency_tree.selection()
    if selected_item:
        currency_id = currency_tree.item(selected_item[0], 'values')[0]
        if messagebox.askyesno('Підтвердження', 'Ви дійсно бажаєте видалити валюту?'):
            currency = Currency(currency_id=currency_id)
            currency.delete()
            update_currency_listbox(currency_tree)
    else:
        messagebox.showwarning('Попередження', 'Виберіть валюту для видалення')

def update_currency_listbox(currency_tree):
    for row in currency_tree.get_children():
        currency_tree.delete(row)
    c.execute("""SELECT currency_id, c_name, exchange_rate, cur_amount FROM Currency""")
    currencies = c.fetchall()
    for currency in currencies:
        currency_tree.insert('', tk.END, values=currency)


# Функції для роботи з Exchange
def get_exchange_rate(currency_from_id, currency_to_id):
    currency_from_rate = c.execute("""SELECT exchange_rate FROM Currency WHERE currency_id = ?""", (currency_from_id,)).fetchone()
    currency_to_rate = c.execute("""SELECT exchange_rate FROM Currency WHERE currency_id = ?""", (currency_to_id,)).fetchone()

    if currency_from_rate and currency_to_rate:
        return currency_to_rate[0] / currency_from_rate[0]
    else:
        raise ValueError(f"Exchange rate not found for currency IDs {currency_from_id} and {currency_to_id}")


def add_exchange():
    def calculate_exchange_amount():
        try:
            exchange_amount = float(exchange_amount_entry.get())
            commission = float(commission_entry.get())
            tax = float(tax_entry.get())
        except ValueError:
            messagebox.showerror("Помилка", "Сума для обміну, комісія та податок мають бути числовими значеннями")
            return

        # Розрахунок обміняної суми валюти
        currency_from_id = int(currency_from_combobox.get())
        currency_to_id = int(currency_to_combobox.get())
        exchange_rate = get_exchange_rate(currency_from_id, currency_to_id)
        exchanged_amount = exchange_amount * exchange_rate

        exchanged_amount_entry.delete(0, tk.END)
        exchanged_amount_entry.insert(0, exchanged_amount)

        full_amount = exchange_amount + (exchange_amount * commission / 100) + (exchange_amount * tax / 100)
        full_amount_entry.delete(0, tk.END)
        full_amount_entry.insert(0, full_amount)

    def save_exchange():
        try:
            amount_to = float(exchange_amount_entry.get())
            commission = float(commission_entry.get())
            tax = float(tax_entry.get())
            full_amount = float(full_amount_entry.get())
        except ValueError:
            messagebox.showerror("Помилка", "Сума для обміну, комісія, податок та повна сума мають бути числовими значеннями")
            return

        cashier_id = cashier_combobox.get()
        currency_from_id = currency_from_combobox.get()
        currency_to_id = currency_to_combobox.get()
        exchange_info = exchange_info_entry.get()
        exchange = Exchange(cashier_id=cashier_id, currency_from_id=currency_from_id, currency_to_id=currency_to_id,
                            amount_to=amount_to, commission=commission, tax=tax, full_amount=full_amount,
                            exchange_info=exchange_info)
        exchange.save()
        exchange_window.destroy()
        update_exchange_listbox(exchange_tree)

    exchange_window = tk.Toplevel(root)
    exchange_window.title('Додати обмін')

    cashier_label = tk.Label(exchange_window, text='Касир:')
    cashier_label.grid(row=0, column=0, padx=5, pady=5)
    cashier_combobox = ttk.Combobox(exchange_window)
    cashier_combobox['values'] = [str(row[0]) for row in c.execute("""SELECT cashier_id FROM Cashier""").fetchall()]
    cashier_combobox.grid(row=0, column=1, padx=5, pady=5)

    currency_from_label = tk.Label(exchange_window, text='Валюта з:')
    currency_from_label.grid(row=1, column=0, padx=5, pady=5)
    currency_from_combobox = ttk.Combobox(exchange_window)
    currency_from_combobox['values'] = [str(row[0]) for row in c.execute("""SELECT currency_id FROM Currency""").fetchall()]
    currency_from_combobox.grid(row=1, column=1, padx=5, pady=5)

    currency_to_label = tk.Label(exchange_window, text='Валюта на:')
    currency_to_label.grid(row=2, column=0, padx=5, pady=5)
    currency_to_combobox = ttk.Combobox(exchange_window)
    currency_to_combobox['values'] = [str(row[0]) for row in c.execute("""SELECT currency_id FROM Currency""").fetchall()]
    currency_to_combobox.grid(row=2, column=1, padx=5, pady=5)

    exchange_amount_label = tk.Label(exchange_window, text='Сума для обміну:')
    exchange_amount_label.grid(row=3, column=0, padx=5, pady=5)
    exchange_amount_entry = tk.Entry(exchange_window)
    exchange_amount_entry.grid(row=3, column=1, padx=5, pady=5)

    commission_label = tk.Label(exchange_window, text='Комісія(%):')
    commission_label.grid(row=4, column=0, padx=5, pady=5)
    commission_entry = tk.Entry(exchange_window)
    commission_entry.grid(row=4, column=1, padx=5, pady=5)

    tax_label = tk.Label(exchange_window, text='Податок(%):')
    tax_label.grid(row=5, column=0, padx=5, pady=5)
    tax_entry = tk.Entry(exchange_window)
    tax_entry.grid(row=5, column=1, padx=5, pady=5)

    calculate_button = tk.Button(exchange_window, text='Розрахувати', command=calculate_exchange_amount)
    calculate_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    exchanged_amount_label = tk.Label(exchange_window, text='Обміняна сума:')
    exchanged_amount_label.grid(row=7, column=0, padx=5, pady=5)
    exchanged_amount_entry = tk.Entry(exchange_window)
    exchanged_amount_entry.grid(row=7, column=1, padx=5, pady=5)

    full_amount_label = tk.Label(exchange_window, text='Повна сума:')
    full_amount_label.grid(row=8, column=0, padx=5, pady=5)
    full_amount_entry = tk.Entry(exchange_window)
    full_amount_entry.grid(row=8, column=1, padx=5, pady=5)

    exchange_info_label = tk.Label(exchange_window, text='Інформація про обмін:')
    exchange_info_label.grid(row=9, column=0, padx=5, pady=5)
    exchange_info_entry = tk.Entry(exchange_window)
    exchange_info_entry.grid(row=9, column=1, padx=5, pady=5)

    save_button = tk.Button(exchange_window, text='Зберегти', command=save_exchange)
    save_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

def edit_exchange(exchange_tree):
    selected_item = exchange_tree.selection()
    if selected_item:
        exchange_id = exchange_tree.item(selected_item[0], 'values')[0]
        c.execute("""SELECT * FROM Exchange WHERE exchange_id=?""", (exchange_id,))
        exchange_data = c.fetchone()
        if exchange_data:
            def save_exchange():
                try:
                    amount_to = float(amount_to_entry.get())
                    commission = float(commission_entry.get())
                    tax = float(tax_entry.get())
                    full_amount = float(full_amount_entry.get())
                except ValueError:
                    messagebox.showerror("Помилка", "Сума для обміну, комісія, податок та повна сума мають бути числовими значеннями")
                    return

                cashier_id = cashier_combobox.get()
                currency_from_id = currency_from_combobox.get()
                currency_to_id = currency_to_combobox.get()
                exchange_info = exchange_info_entry.get()
                exchange = Exchange(exchange_id=exchange_id, cashier_id=cashier_id,
                                    currency_from_id=currency_from_id, currency_to_id=currency_to_id,
                                    amount_to=amount_to, commission=commission, tax=tax, full_amount=full_amount,
                                    exchange_info=exchange_info)
                exchange.save()
                exchange_window.destroy()
                update_exchange_listbox(exchange_tree)

            exchange_window = tk.Toplevel(root)
            exchange_window.title('Редагувати обмін')

            cashier_label = tk.Label(exchange_window, text='Касир:')
            cashier_label.grid(row=0, column=0, padx=5, pady=5)
            cashier_combobox = ttk.Combobox(exchange_window)
            cashier_combobox['values'] = [str(row[0]) for row in c.execute("""SELECT cashier_id FROM Cashier""").fetchall()]
            cashier_combobox.grid(row=0, column=1, padx=5, pady=5)
            cashier_combobox.set(exchange_data[1])

            currency_from_label = tk.Label(exchange_window, text='Валюта з:')
            currency_from_label.grid(row=1, column=0, padx=5, pady=5)
            currency_from_combobox = ttk.Combobox(exchange_window)
            currency_from_combobox['values'] = [str(row[0]) for row in c.execute("""SELECT currency_id FROM Currency""").fetchall()]
            currency_from_combobox.grid(row=1, column=1, padx=5, pady=5)
            currency_from_combobox.set(exchange_data[2])

            currency_to_label = tk.Label(exchange_window, text='Валюта на:')
            currency_to_label.grid(row=2, column=0, padx=5, pady=5)
            currency_to_combobox = ttk.Combobox(exchange_window)
            currency_to_combobox['values'] = [str(row[0]) for row in c.execute("""SELECT currency_id FROM Currency""").fetchall()]
            currency_to_combobox.grid(row=2, column=1, padx=5, pady=5)
            currency_to_combobox.set(exchange_data[3])

            amount_to_label = tk.Label(exchange_window, text='Сума:')
            amount_to_label.grid(row=3, column=0, padx=5, pady=5)
            amount_to_entry = tk.Entry(exchange_window)
            amount_to_entry.insert(0, exchange_data[4])
            amount_to_entry.grid(row=3, column=1, padx=5, pady=5)

            commission_label = tk.Label(exchange_window, text='Комісія(%):')
            commission_label.grid(row=4, column=0, padx=5, pady=5)
            commission_entry = tk.Entry(exchange_window)
            commission_entry.insert(0, exchange_data[5])
            commission_entry.grid(row=4, column=1, padx=5, pady=5)

            tax_label = tk.Label(exchange_window, text='Податок(%):')
            tax_label.grid(row=5, column=0, padx=5, pady=5)
            tax_entry = tk.Entry(exchange_window)
            tax_entry.insert(0, exchange_data[6])
            tax_entry.grid(row=5, column=1, padx=5, pady=5)

            full_amount_label = tk.Label(exchange_window, text='Загальна сума:')
            full_amount_label.grid(row=6, column=0, padx=5, pady=5)
            full_amount_entry = tk.Entry(exchange_window)
            full_amount_entry.insert(0, exchange_data[7])
            full_amount_entry.grid(row=6, column=1, padx=5, pady=5)

            exchange_info_label = tk.Label(exchange_window, text='Інформація про обмін:')
            exchange_info_label.grid(row=7, column=0, padx=5, pady=5)
            exchange_info_entry = tk.Entry(exchange_window)
            exchange_info_entry.insert(0, exchange_data[8])
            exchange_info_entry.grid(row=7, column=1, padx=5, pady=5)

            save_button = tk.Button(exchange_window, text='Зберегти', command=save_exchange)
            save_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
    else:
        messagebox.showwarning('Попередження', 'Виберіть обмін для редагування')

def delete_exchange(exchange_tree):
    selected_item = exchange_tree.selection()
    if selected_item:
        exchange_id = exchange_tree.item(selected_item[0], 'values')[0]
        if messagebox.askyesno('Підтвердження', 'Ви дійсно бажаєте видалити обмін?'):
            exchange = Exchange(exchange_id=exchange_id)
            exchange.delete()
            update_exchange_listbox(exchange_tree)
    else:
        messagebox.showwarning('Попередження', 'Виберіть обмін для видалення')


def update_exchange_listbox(exchange_tree):
    for item in exchange_tree.get_children():
        exchange_tree.delete(item)
    for row in c.execute("""SELECT * FROM Exchange"""):
        exchange_tree.insert('', 'end', values=row)


# Функції для роботи з Receipt
def add_receipt(receipt_tree):
    def save_receipt():
        exchange_id = exchange_combobox.get()
        date = date_entry.get()
        time = time_entry.get()
        name = name_entry.get()

        # Перевірка формату дати і часу
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Помилка", "Дата має бути в форматі YYYY-MM-DD")
            return

        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror("Помилка", "Час має бути в форматі HH:MM")
            return

        c.execute("""INSERT INTO Receipt (exchange_id, date, time, name) VALUES (?, ?, ?, ?)""",
                  (exchange_id, date, time, name))
        conn.commit()
        receipt_window.destroy()
        update_receipt_tree()

    receipt_window = tk.Toplevel(root)
    receipt_window.title('Додати квитанцію')

    exchange_label = tk.Label(receipt_window, text='Обмін:')
    exchange_label.grid(row=0, column=0, padx=5, pady=5)
    exchange_combobox = ttk.Combobox(receipt_window)
    exchange_combobox['values'] = [str(row[0]) for row in c.execute("""SELECT exchange_id FROM Exchange""").fetchall()]
    exchange_combobox.grid(row=0, column=1, padx=5, pady=5)

    date_label = tk.Label(receipt_window, text='Дата(YYYY-MM-DD):')
    date_label.grid(row=1, column=0, padx=5, pady=5)
    date_entry = tk.Entry(receipt_window)
    date_entry.grid(row=1, column=1, padx=5, pady=5)

    time_label = tk.Label(receipt_window, text='Час(HH:MM):')
    time_label.grid(row=2, column=0, padx=5, pady=5)
    time_entry = tk.Entry(receipt_window)
    time_entry.grid(row=2, column=1, padx=5, pady=5)

    name_label = tk.Label(receipt_window, text='Ім\'я клієнта:')
    name_label.grid(row=3, column=0, padx=5, pady=5)
    name_entry = tk.Entry(receipt_window)
    name_entry.grid(row=3, column=1, padx=5, pady=5)

    save_button = tk.Button(receipt_window, text='Зберегти', command=save_receipt)
    save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)


def edit_receipt(receipt_tree):
    selected_item = receipt_tree.selection()
    if selected_item:
        receipt_id = receipt_tree.item(selected_item[0], 'values')[0]
        c.execute("""SELECT * FROM Receipt WHERE receipt_id=?""", (receipt_id,))
        receipt = c.fetchone()

        def save_receipt():
            exchange_id = exchange_combobox.get()
            date = date_entry.get()
            time = time_entry.get()
            name = name_entry.get()

            # Перевірка формату дати і часу
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Помилка", "Дата має бути в форматі YYYY-MM-DD")
                return

            try:
                datetime.strptime(time, "%H:%M")
            except ValueError:
                messagebox.showerror("Помилка", "Час має бути в форматі HH:MM")
                return

            c.execute("""UPDATE Receipt SET exchange_id=?, date=?, time=?, name=? WHERE receipt_id=?""",
                      (exchange_id, date, time, name, receipt_id))
            conn.commit()
            receipt_window.destroy()
            update_receipt_tree()

        receipt_window = tk.Toplevel(root)
        receipt_window.title('Редагувати квитанцію')

        exchange_label = tk.Label(receipt_window, text='Обмін:')
        exchange_label.grid(row=0, column=0, padx=5, pady=5)
        exchange_combobox = ttk.Combobox(receipt_window)
        exchange_combobox['values'] = [str(row[0]) for row in
                                       c.execute("""SELECT exchange_id FROM Exchange""").fetchall()]
        exchange_combobox.set(receipt[1])
        exchange_combobox.grid(row=0, column=1, padx=5, pady=5)

        date_label = tk.Label(receipt_window, text='Дата(YYYY-MM-DD):')
        date_label.grid(row=1, column=0, padx=5, pady=5)
        date_entry = tk.Entry(receipt_window)
        date_entry.insert(0, receipt[2])
        date_entry.grid(row=1, column=1, padx=5, pady=5)

        time_label = tk.Label(receipt_window, text='Час(HH:MM):')
        time_label.grid(row=2, column=0, padx=5, pady=5)
        time_entry = tk.Entry(receipt_window)
        time_entry.insert(0, receipt[3])
        time_entry.grid(row=2, column=1, padx=5, pady=5)

        name_label = tk.Label(receipt_window, text='Ім\'я клієнта:')
        name_label.grid(row=3, column=0, padx=5, pady=5)
        name_entry = tk.Entry(receipt_window)
        name_entry.insert(0, receipt[4])
        name_entry.grid(row=3, column=1, padx=5, pady=5)

        save_button = tk.Button(receipt_window, text='Зберегти', command=save_receipt)
        save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    else:
        messagebox.showwarning('Попередження', 'Будь ласка, виберіть квитанцію для редагування.')


def delete_receipt(receipt_tree):
    if receipt_tree.selection():
        receipt_index = receipt_tree.selection()[0]
        receipt_id = receipt_tree.item(receipt_index, 'values')[0]
        c.execute("""DELETE FROM Receipt WHERE receipt_id=?""", (receipt_id,))
        # Оновлення таблиці після видалення
        update_receipt_tree()
    else:
        messagebox.showwarning('Попередження', 'Виберіть квитанцію для видалення')
def update_receipt_tree():
    # Очищення таблиці перед оновленням
    for row in receipt_tree.get_children():
        receipt_tree.delete(row)

    # Вибір всіх записів з таблиці Receipt
    for row in c.execute("""SELECT receipt_id, exchange_id, date, time, name FROM Receipt""").fetchall():
        receipt_tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4]))





def execute_query(query, *args):
    try:
        c.execute(query, args)
        results = c.fetchall()
        display_results(results, [desc[0] for desc in c.description])
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_results(results, columns):
    result_window = tk.Toplevel()
    result_window.title("Результат запиту")

    tree = ttk.Treeview(result_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)

    for row in results:
        tree.insert("", tk.END, values=row)

    tree.pack(expand=True, fill=tk.BOTH)

def query_1():
    def execute_query_and_show_results(cashier_name):
        if cashier_name:
            execute_query("""SELECT e.exchange_id, e.exchange_info
                             FROM Exchange e
                             JOIN Cashier c ON e.cashier_id = c.cashier_id
                             WHERE c.name = ?
                             ORDER BY e.exchange_id""", cashier_name)
        else:
            messagebox.showwarning("Input Error", "Cashier name cannot be empty")

    def select_cashier():
        cashier_window = tk.Toplevel(root)
        cashier_window.title("Select Cashier")

        cashier_label = tk.Label(cashier_window, text="Enter Cashier Name:")
        cashier_label.pack()

        cashier_entry = tk.Entry(cashier_window)
        cashier_entry.pack()

        confirm_button = tk.Button(cashier_window, text="Confirm",
                                   command=lambda: execute_query_and_show_results(cashier_entry.get()))
        confirm_button.pack()

    select_cashier()

def query_2():
    def get_letter():
        letter_window = tk.Toplevel(root)
        letter_window.title("Введіть букву")

        letter_label = tk.Label(letter_window, text="Введіть букву:")
        letter_label.pack()

        letter_entry = tk.Entry(letter_window)
        letter_entry.pack()

        def show_results_window():
            letter = letter_entry.get()
            if letter:
                results = execute_query("""SELECT name
                                           FROM Cashier
                                           WHERE name LIKE ?""", letter + '%')
            else:
                messagebox.showwarning("Input Error", "Letter cannot be empty")
            letter_window.destroy()

        confirm_button = tk.Button(letter_window, text="Підтвердити", command=show_results_window)
        confirm_button.pack()

    get_letter()


def query_3():
    def is_valid_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    start_date = simpledialog.askstring("Input", "Введіть початкову дату (формат: YYYY-MM-DD):")
    end_date = simpledialog.askstring("Input", "Введіть кінцеву дату (формат: YYYY-MM-DD):")

    if start_date and end_date:
        if is_valid_date(start_date) and is_valid_date(end_date):
            execute_query("""SELECT *
                             FROM Receipt
                             WHERE date BETWEEN ? AND ?""", start_date, end_date)
        else:
            messagebox.showwarning("Input Error", "Both dates must be in the format YYYY-MM-DD")
    else:
        messagebox.showwarning("Input Error", "Both dates must be provided")

def query_4():
    execute_query("""SELECT COUNT(*)
                     FROM Receipt
                     WHERE date BETWEEN DATE('now', '-7 days') AND DATE('now')""")

def query_5():
    execute_query("""SELECT c.name, COUNT(e.exchange_id) AS total_exchanges
                     FROM Cashier c
                     LEFT JOIN Exchange e ON c.cashier_id = e.cashier_id
                     GROUP BY c.cashier_id""")

def query_6():
    execute_query("""SELECT c.name
                     FROM Cashier c
                     WHERE (
                         SELECT COUNT(*)
                         FROM Exchange e
                         WHERE e.cashier_id = c.cashier_id
                     ) >= (
                         SELECT MAX(exchange_count)
                         FROM (
                             SELECT COUNT(*) AS exchange_count
                             FROM Exchange
                             GROUP BY cashier_id
                         )
                     )""")


def query_7():
    execute_query("""SELECT c.name, cu.c_name, COUNT(e.exchange_id) AS total_exchanges
                     FROM Cashier c
                     JOIN Exchange e ON c.cashier_id = e.cashier_id
                     JOIN Currency cu ON e.currency_from_id = cu.currency_id OR e.currency_to_id = cu.currency_id
                     GROUP BY c.cashier_id, cu.currency_id
                     ORDER BY total_exchanges DESC""")

def query_8_left_join():
    execute_query("""SELECT c.name
                     FROM Cashier c
                     LEFT JOIN Exchange e ON c.cashier_id = e.cashier_id
                     WHERE e.exchange_id IS NULL""")

def query_8_in():
    execute_query("""SELECT name
                     FROM Cashier
                     WHERE cashier_id NOT IN (SELECT DISTINCT cashier_id FROM Exchange)""")

def query_8_exists():
    execute_query("""SELECT name
                     FROM Cashier c
                     WHERE NOT EXISTS (SELECT 1 FROM Exchange e WHERE c.cashier_id = e.cashier_id)""")

def query_9():
    exchange_info = simpledialog.askstring("Input", "Введіть Exchange info:")
    if exchange_info:
        execute_query(
            """SELECT e.exchange_id, e.exchange_info, c.name as cashier_name
               FROM Exchange e
               JOIN Cashier c ON e.cashier_id = c.cashier_id
               WHERE e.exchange_info = ?
               UNION
               SELECT e.exchange_id, e.exchange_info, c.name as cashier_name
               FROM Exchange e
               LEFT JOIN Cashier c ON e.cashier_id = c.cashier_id
               WHERE e.exchange_info = ?
               ORDER BY cashier_name""",
            exchange_info, exchange_info)
    else:
        messagebox.showwarning("Input Error", "Exchange info cannot be empty")


# Головне вікно
root.title('Система обміну валют')

# Меню
menu = tk.Menu(root)
root.config(menu=menu)

# Меню для виконання запитів
query_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='Запити', menu=query_menu)

query_menu.add_command(label='Обміни які провів даний касир', command=query_1)
query_menu.add_command(label='Знайти імена касирів на задану букву', command=query_2)
query_menu.add_command(label='Список квитанцій, складених у заданий період', command=query_3)
query_menu.add_command(label='Кількість квитанцій за останній тиждень', command=query_4)
query_menu.add_command(label='Кількість обмінів кожного касира', command=query_5)
query_menu.add_command(label='Хто з касирів провів найбільшу кількість обмінів', command=query_6)
query_menu.add_command(label='Для валюти визнвчити касира що провів найбільше обмінів з нею', command=query_7)
query_menu.add_command(label='Хто з касирів не провів жодного обміну (LEFT JOIN)', command=query_8_left_join)
query_menu.add_command(label='Хто з касирів не провів жодного обміну (IN)', command=query_8_in)
query_menu.add_command(label='Хто з касирів не провів жодного обміну (EXISTS)', command=query_8_exists)
query_menu.add_command(label='Список обмінів з Коментарем ', command=query_9)

cashier_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='Касири', menu=cashier_menu)
cashier_menu.add_command(label='Додати касира', command=add_cashier)
cashier_menu.add_command(label='Редагувати касира', command=lambda: edit_cashier(cashier_tree))
cashier_menu.add_command(label='Видалити касира', command=lambda: delete_cashier(cashier_tree))

currency_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='Валюти', menu=currency_menu)
currency_menu.add_command(label='Додати валюту', command=add_currency)
currency_menu.add_command(label='Редагувати валюту', command=lambda: edit_currency(currency_tree))
currency_menu.add_command(label='Видалити валюту', command=lambda: delete_currency(currency_tree))

exchange_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='Обміни', menu=exchange_menu)
exchange_menu.add_command(label='Додати обмін', command=add_exchange)
exchange_menu.add_command(label='Редагувати обмін', command=lambda: edit_exchange(exchange_tree))
exchange_menu.add_command(label='Видалити обмін', command=lambda: delete_exchange(exchange_tree))

receipt_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='Квитанції', menu=receipt_menu)
receipt_menu.add_command(label='Додати квитанцію', command=lambda: add_receipt(receipt_tree))
receipt_menu.add_command(label='Редагувати квитанцію', command=lambda: edit_receipt(receipt_tree))
receipt_menu.add_command(label='Видалити квитанцію', command=lambda: delete_receipt(receipt_tree))


# Списки
frame = tk.Frame(root)
frame.grid(row=0, column=0, padx=5, pady=5)

label = tk.Label(frame, text="Список касирів")
label.pack(side=tk.TOP, anchor=tk.W)

cashier_tree = ttk.Treeview(frame, columns=('ID', 'Name', 'Phone', 'Email'), show='headings')
cashier_tree.heading('ID', text='ID')
cashier_tree.heading('Name', text='Ім\'я')
cashier_tree.heading('Phone', text='Телефон')
cashier_tree.heading('Email', text='Email')
cashier_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=cashier_tree.yview)
cashier_tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

update_cashier_listbox(cashier_tree)


# Віджети для валют
frame_currency = tk.Frame(root)
frame_currency.grid(row=2, column=0, padx=5, pady=5)

label_currency = tk.Label(frame_currency, text="Список валют")
label_currency.pack(side=tk.TOP, anchor=tk.W)

currency_tree = ttk.Treeview(frame_currency, columns=('ID', 'Name', 'Rate', 'Available'), show='headings')
currency_tree.heading('ID', text='ID')
currency_tree.heading('Name', text='Назва')
currency_tree.heading('Rate', text='Курс обміну')
currency_tree.heading('Available', text='Доступність')
currency_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_currency = ttk.Scrollbar(frame_currency, orient=tk.VERTICAL, command=currency_tree.yview)
currency_tree.configure(yscroll=scrollbar_currency.set)
scrollbar_currency.pack(side=tk.RIGHT, fill=tk.Y)

update_currency_listbox(currency_tree)

# Таблиця обмінів
frame_exchange = tk.Frame(root)
frame_exchange.grid(row=3, column=0, padx=5, pady=5)

label_exchange = tk.Label(frame_exchange, text="Список обмінів")
label_exchange.pack(side=tk.TOP, anchor=tk.W)
exchange_tree = ttk.Treeview(root, columns=('exchange_id', 'cashier_id', 'currency_from_id', 'currency_to_id', 'amount_to',
                                            'commission', 'tax', 'full_amount', 'exchange_info'), show='headings')
exchange_tree.heading('exchange_id', text='ID Обміну')
exchange_tree.heading('cashier_id', text='ID Касира')
exchange_tree.heading('currency_from_id', text='ID Валюти з')
exchange_tree.heading('currency_to_id', text='ID Валюти на')
exchange_tree.heading('amount_to', text='Сума для обміну')
exchange_tree.heading('commission', text='Комісія')
exchange_tree.heading('tax', text='Податок')
exchange_tree.heading('full_amount', text='Повна сума')
exchange_tree.heading('exchange_info', text='Інформація про обмін')

exchange_tree.column('exchange_id', width=80)
exchange_tree.column('cashier_id', width=80)
exchange_tree.column('currency_from_id', width=80)
exchange_tree.column('currency_to_id', width=80)
exchange_tree.column('amount_to', width=100)
exchange_tree.column('commission', width=80)
exchange_tree.column('tax', width=80)
exchange_tree.column('full_amount', width=100)
exchange_tree.column('exchange_info', width=200)

exchange_tree.grid(row=3, column=0, columnspan=4, padx=6, pady=6, sticky='nsew')

scrollbar_exchange = ttk.Scrollbar(root, orient=tk.VERTICAL, command=exchange_tree.yview)
exchange_tree.configure(yscroll=scrollbar_exchange.set)
scrollbar_exchange.grid(row=0, column=4, sticky='ns')


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

# Оновлення списку обмінів при запуску
update_exchange_listbox(exchange_tree)

table_label = tk.Label(root, text="Список квитанцій")
table_label.grid(row=1, column=3, pady=(0,5))

# Створення таблиці
receipt_tree = ttk.Treeview(root, columns=('Receipt ID', 'Exchange ID', 'Date', 'Time', 'Name'))
receipt_tree.heading('#0', text='')
receipt_tree.heading('#1', text='Receipt ID')
receipt_tree.heading('#2', text='Exchange ID')
receipt_tree.heading('#3', text='Date')
receipt_tree.heading('#4', text='Time')
receipt_tree.heading('#5', text='Name')
receipt_tree.column('#0', width=0)
receipt_tree.column('#1', width=80)
receipt_tree.column('#2', width=90)
receipt_tree.column('#3', width=90)
receipt_tree.column('#4', width=90)
receipt_tree.column('#5', width=130)
receipt_tree.grid(row=0, column=3, padx=5, pady=5)
# Оновлення списку квитанцій
update_receipt_tree()


root.mainloop()

