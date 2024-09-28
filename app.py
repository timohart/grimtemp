from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          # Replace with your MySQL user
            password="HellBorn",  # Replace with your MySQL password
            database="larp_db"    # Your database name
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Route to display all players
@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM players')
            players = cursor.fetchall()
            return render_template('index.html', players=players)
        except Error as e:
            flash(f"Error fetching players: {e}", "error")
            return render_template('index.html', players=[])
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Error connecting to the database.", "error")
        return render_template('index.html', players=[])

# Route to add a new player
@app.route('/add', methods=['POST'])
def add_player():
    player_name = request.form.get('player_name', '').strip()
    character_name = request.form.get('character_name', '').strip()
    gold = request.form.get('gold', '0').strip()
    silver = request.form.get('silver', '0').strip()
    copper = request.form.get('copper', '0').strip()
    items = request.form.get('items', '').strip()

    if not player_name or not character_name:
        flash("Player Name and Character Name are required!", "error")
        return redirect(url_for('index'))

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = '''
                INSERT INTO players (player_name, character_name, gold, silver, copper, items)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (player_name, character_name, gold, silver, copper, items))
            conn.commit()
            flash(f"Player '{player_name}' added successfully!", "success")
        except Error as e:
            flash(f"Error adding player: {e}", "error")
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Failed to connect to the database.", "error")

    return redirect(url_for('index'))

# Route to check in a player
@app.route('/checkin/<int:id>', methods=['GET', 'POST'])
def checkin_player(id):
    conn = get_db_connection()
    if not conn:
        flash("Failed to connect to the database.", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        gold = request.form.get('gold', '0').strip()
        silver = request.form.get('silver', '0').strip()
        copper = request.form.get('copper', '0').strip()
        items = request.form.get('items', '').strip()
        check_in_time = datetime.now()

        try:
            cursor = conn.cursor()
            update_query = '''
                UPDATE players
                SET gold = %s, silver = %s, copper = %s, items = %s, check_in_time = %s, check_out_time = NULL
                WHERE id = %s
            '''
            cursor.execute(update_query, (gold, silver, copper, items, check_in_time, id))
            conn.commit()
            flash("Player checked in successfully!", "success")
        except Error as e:
            flash(f"Error checking in player: {e}", "error")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('index'))

    # GET request: Fetch player data to pre-fill the form
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM players WHERE id = %s', (id,))
        player = cursor.fetchone()
        if not player:
            flash("Player not found.", "error")
            return redirect(url_for('index'))
        return render_template('checkin.html', player=player)
    except Error as e:
        flash(f"Error fetching player data: {e}", "error")
        return redirect(url_for('index'))
    finally:
        cursor.close()
        conn.close()

# Route to check out a player
@app.route('/checkout/<int:id>', methods=['GET', 'POST'])
def checkout_player(id):
    conn = get_db_connection()
    if not conn:
        flash("Failed to connect to the database.", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        gold = request.form.get('gold', '0').strip()
        silver = request.form.get('silver', '0').strip()
        copper = request.form.get('copper', '0').strip()
        items = request.form.get('items', '').strip()
        check_out_time = datetime.now()

        try:
            cursor = conn.cursor()
            update_query = '''
                UPDATE players
                SET gold = %s, silver = %s, copper = %s, items = %s, check_out_time = %s
                WHERE id = %s
            '''
            cursor.execute(update_query, (gold, silver, copper, items, check_out_time, id))
            conn.commit()
            flash("Player checked out successfully!", "success")
        except Error as e:
            flash(f"Error checking out player: {e}", "error")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('index'))

    # GET request: Fetch player data to pre-fill the form
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM players WHERE id = %s', (id,))
        player = cursor.fetchone()
        if not player:
            flash("Player not found.", "error")
            return redirect(url_for('index'))
        return render_template('checkout.html', player=player)
    except Error as e:
        flash(f"Error fetching player data: {e}", "error")
        return redirect(url_for('index'))
    finally:
        cursor.close()
        conn.close()

# Route to delete a player
@app.route('/delete/<int:id>')
def delete_player(id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM players WHERE id = %s', (id,))
            conn.commit()
            flash("Player deleted successfully!", "success")
        except Error as e:
            flash(f"Error deleting player: {e}", "error")
        finally:
            cursor.close()
            conn.close()
    else:
        flash("Failed to connect to the database.", "error")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
