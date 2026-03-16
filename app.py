from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect("campus_energy.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT room, temperature, power, status FROM energy_data ORDER BY id DESC LIMIT 10"
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_waste_data():

    conn = sqlite3.connect("campus_energy.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT room, COUNT(*)
    FROM energy_data
    WHERE status='ENERGY WASTE'
    GROUP BY room
    """)

    result = cursor.fetchall()
    conn.close()

    waste_rooms = [row[0] for row in result]
    waste_counts = [row[1] for row in result]

    return waste_rooms, waste_counts


@app.route("/")
def dashboard():

    data = get_data()

    rooms = [row[0] for row in data]
    temps = [row[1] for row in data]
    power = [row[2] for row in data]

    waste_rooms, waste_counts = get_waste_data()

    return render_template(
        "dashboard.html",
        data=data,
        rooms=rooms,
        temps=temps,
        power=power,
        waste_rooms=waste_rooms,
        waste_counts=waste_counts
    )


if __name__ == "__main__":
    app.run(debug=True)