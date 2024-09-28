import tkinter as tk
from tkinter import messagebox
# from datetime import datetime
import mysql.connector
import PySimpleGUI as sg

# Function to connect to the MySQL database
def connect_to_mysql():
    try:
        return mysql.connector.connect(
            host='localhost',  # Replace with your MySQL host
            database='larp_db',  # Replace with your database name
            user='root',  # Replace with your MySQL username
            password='HellBorn'  # Replace with your MySQL password
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None

def submit(values):
    player_name = values['player_name']
    character_name = values['character_name']
    gold = values['gold']
    silver = values['silver']
    copper = values['copper']
    items = values['items']
    
    print(f"Player: {player_name}, Character: {character_name}, Gold: {gold}, Silver: {silver}, Copper: {copper}, Items: {items}")

# Define the layout for the window
layout = [
    [sg.Text('Player Name:', size=(15, 1)), sg.InputText(key='player_name')],
    [sg.Text('Character Name:', size=(15, 1)), sg.InputText(key='character_name')],
    [sg.Text('Gold:', size=(15, 1)), sg.InputText(key='gold', size=(10, 1))],
    [sg.Text('Silver:', size=(15, 1)), sg.InputText(key='silver', size=(10, 1))],
    [sg.Text('Copper:', size=(15, 1)), sg.InputText(key='copper', size=(10, 1))],
    [sg.Text('Items (comma separated):', size=(15, 1)), sg.InputText(key='items')],
    [sg.Button('Submit'), sg.Button('Cancel')]
]

# Create the window
window = sg.Window('Player Check-in/Check-out', layout)

# Event loop to process events and capture the input values
while True:
    event, values = window.read()
    
    # Close the window if user clicks 'Cancel' or closes the window
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    
    # If user clicks 'Submit', call the submit function
    if event == 'Submit':
        submit(values)

# Close the window when the loop is finished
window.close()