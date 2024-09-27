import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector

# Function to connect to the MySQL database
def connect_to_mysql():
    try:
        return mysql.connector.connect(
            host='localhost',  # Replace with your MySQL host
            database='larp_db',  # Replace with your database name
            user='your_username',  # Replace with your MySQL username
            password='your_password'  # Replace with your MySQL password
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None

# Function to handle player check-in
def check_in():
    player_name = entry_player_name.get()
    character_name = entry_character_name.get()
    gold = entry_gold.get() or 0
    silver = entry_silver.get() or 0
    copper = entry_copper.get() or 0
    items = entry_items.get()

    check_in_time = datetime.now()

    if not player_name or not character_name:
        messagebox.showwarning("Input Error", "Player and Character names are required!")
        return

    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        insert_query = ("INSERT INTO player_log (player_name, character_name, gold, silver, copper, items, check_in_time) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(insert_query, (player_name, character_name, gold, silver, copper, items, check_in_time))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Check-In", f"{player_name} checked in successfully!")
        clear_fields()

# Function to handle player check-out
def check_out():
    player_name = entry_player_name.get()

    if not player_name:
        messagebox.showwarning("Input Error", "Player name is required to check out!")
        return

    check_out_time = datetime.now()
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        update_query = ("UPDATE player_log SET check_out_time = %s WHERE player_name = %s AND check_out_time IS NULL")
        cursor.execute(update_query, (check_out_time, player_name))
        if cursor.rowcount > 0:
            connection.commit()
            messagebox.showinfo("Check-Out", f"{player_name} checked out successfully!")
        else:
            messagebox.showerror("Check-Out Error", f"No active session found for {player_name}.")
        cursor.close()
        connection.close()

# Function to clear all input fields
def clear_fields():
    entry_player_name.delete(0, tk.END)
    entry_character_name.delete(0, tk.END)
    entry_gold.delete(0, tk.END)
    entry_silver.delete(0, tk.END)
    entry_copper.delete(0, tk.END)
    entry_items.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Player Check-In/Out")

# Labels and Entry fields
tk.Label(root, text="Player Name:").grid(row=0, column=0)
entry_player_name = tk.Entry(root)
entry_player_name.grid(row=0, column=1)

tk.Label(root, text="Character Name:").grid(row=1, column=0)
entry_character_name = tk.Entry(root)
entry_character_name.grid(row=1, column=1)

tk.Label(root, text="Gold:").grid(row=2, column=0)
entry_gold = tk.Entry(root)
entry_gold.grid(row=2, column=1)

tk.Label(root, text="Silver:").grid(row=3, column=0)
entry_silver = tk.Entry(root)
entry_silver.grid(row=3, column=1)

tk.Label(root, text="Copper:").grid(row=4, column=0)
entry_copper = tk.Entry(root)
entry_copper.grid(row=4, column=1)

tk.Label(root, text="Items:").grid(row=5, column=0)
entry_items = tk.Entry(root)
entry_items.grid(row=5, column=1)

# Buttons for Check-In and Check-Out
btn_check_in = tk.Button(root, text="Check In", command=check_in)
btn_check_in.grid(row=6, column=0, pady=10)

btn_check_out = tk.Button(root, text="Check Out", command=check_out)
btn_check_out.grid(row=6, column=1, pady=10)

# Start the GUI loop
root.mainloop()
