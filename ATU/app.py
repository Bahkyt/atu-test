import os
from datetime import date
from dotenv import load_dotenv
from flask import request, render_template, redirect, Flask, jsonify, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import time

DB_NAME = "participant.db"
DB_WINNERS = "winner.db"

def init_participant():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL,
            track TEXT NOT NULL,

            captain_name TEXT NOT NULL,
            captain_email TEXT NOT NULL,
            captain_phone TEXT NOT NULL,
            captain_city TEXT NOT NULL,

            participant_1 TEXT,
            participant_city_1 TEXT,

            participant_2 TEXT,
            participant_city_2 TEXT,

            participant_3 TEXT,
            participant_city_3 TEXT,

            participant_4 TEXT,
            participant_city_4 TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def init_admin():
    conn = sqlite3.connect("admin.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login text UNIQUE,
            password text,
            login_version integer default 1
        )
    """)

    conn.commit()
    conn.close()

def init_winners():
    conn = sqlite3.connect(DB_WINNERS)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS winners (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            year TEXT,               
            team_name TEXT,
            team_place TEXT,

            participant_1 TEXT,           
            participant_2 TEXT,
            participant_3 TEXT,
            participant_4 TEXT,
            captain_name TEXT,
            captain_email TEXT,
            captain_phone TEXT
        )
    """)

    conn.commit()
    conn.close()

    def init_winners():
        conn = sqlite3.connect(DB_WINNERS)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS winners (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                year TEXT,               
                team_name TEXT,
                team_place TEXT,

                participant_1 TEXT,           
                participant_2 TEXT,
                participant_3 TEXT,
                participant_4 TEXT,
                captain_name TEXT,
                captain_email TEXT,
                captain_phone TEXT
            )
        """)

        conn.commit()
        conn.close()

def init_settings():
    conn = sqlite3.connect("settings.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS setting (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            year_from TEXT,
            month_from integer,           
            day_from integer,           
            year_to TEXT,
            month_to integer,           
            day_to integer          
        )
    """)

    conn.commit()
    conn.close()

def get_participants_info():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM participants")
    rows = cursor.fetchall()

    info = []

    for row in rows:
        info.append({
            "id": row[0],
            "team_name": row[1],
            "track": row[2],

            "captain_name": row[3],
            "captain_email": row[4],
            "captain_phone": row[5],
            "captain_city": row[6],

            "participant_1": row[7],
            "participant_city_1": row[8],

            "participant_2": row[9],
            "participant_city_2": row[10],

            "participant_3": row[11],
            "participant_city_3": row[12],

            "participant_4": row[13],
            "participant_city_4": row[14],
            "created_at": row[15],
        })

    conn.close()
    return info

def get_admin_info():
    conn = sqlite3.connect("admin.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM admin_users")
    rows = cursor.fetchall()

    info = []

    for row in rows:
        info.append({
            "id": row[0],
            "login": row[1],
            "password": row[2],
            "login_version": row[3],
        })

    conn.close()
    return info

def get_winners_info():
    conn = sqlite3.connect(DB_WINNERS)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM winners")
    rows = cursor.fetchall()

    info = []

    for row in rows:
        info.append({
            "id": row[0],
            "year": row[1],
            "team_name": row[2],
            "team_place": row[3],

            "participant_1": row[4],
            "participant_2": row[5],
            "participant_3": row[6],
            "participant_4": row[7],
            "captain_name": row[8],
            "captain_email": row[9],
            "captain_phone": row[10],
        })

    conn.close()
    return info

def get_settings_info():
    conn = sqlite3.connect("settings.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM setting")
    rows = cursor.fetchall()

    info = []

    for row in rows:
        info.append({
            "id": row[0],
            "year_from": row[1],
            "month_from": row[2],
            "day_from": row[3],

            "year_to": row[4],
            "month_to": row[5],
            "day_to": row[6]
        })

    conn.close()
    return info

def is_registration_open():
    info = get_settings_info()

    if not info:
        return False

    item = info[0]

    date_from = date(
        int(item["year_from"]),
        int(item["month_from"]),
        int(item["day_from"])
    )

    date_to = date(
        int(item["year_to"]),
        int(item["month_to"]),
        int(item["day_to"])
    )

    today = date.today()

    return date_from <= today <= date_to

init_participant()
init_winners()
init_admin()
init_settings()
load_dotenv("SECRET_KEY.env")

def save_participant(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO participants (
            team_name, track,
            captain_name, captain_email, captain_phone, captain_city,
            participant_1, participant_city_1,
            participant_2, participant_city_2,
            participant_3, participant_city_3,
            participant_4, participant_city_4
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("team_name"),
        data.get("track"),

        data.get("captain_full_name"),
        data.get("captain_email"),
        data.get("captain_phone"),
        data.get("captain_city"),

        data.get("participant_1"),
        data.get("participant_city_1"),

        data.get("participant_2"),
        data.get("participant_city_2"),

        data.get("participant_3"),
        data.get("participant_city_3"),

        data.get("participant_4"),
        data.get("participant_city_4"),
    ))

    conn.commit()
    conn.close()

def is_winners_empty():
    conn = sqlite3.connect(DB_WINNERS)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM winners")
    count = cursor.fetchone()[0]

    conn.close()

    return count >= 3

def add_winner(year, team_name, team_place,
               participant_1="", participant_2="", participant_3="",
               participant_4="", captain_name="", captain_email="", captain_phone=""):
    conn = sqlite3.connect(DB_WINNERS)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO winners (
            year,
            team_name,
            team_place,
            participant_1,
            participant_2,
            participant_3,
            participant_4,
            captain_name,
            captain_email,
            captain_phone
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        year,
        team_name,
        team_place,
        participant_1,
        participant_2,
        participant_3,
        participant_4,
        captain_name,
        captain_email,
        captain_phone
    ))

    conn.commit()
    conn.close()

def delete_winner_by_team_name(team_name):
    conn = sqlite3.connect(DB_WINNERS)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM winners
        WHERE LOWER(id) = LOWER(?)
    """, (team_name.strip(),))

    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()

    return deleted_rows

def delete_dashboard_by_team_name(team_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM participants
        WHERE LOWER(id) = LOWER(?)
    """, (team_name.strip(),))

    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()

    return deleted_rows

def clear_participants():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM participants")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='participants'")

    conn.commit()
    conn.close()

app = Flask("__name__")
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

@app.route("/")
def main():
    time_info = get_settings_info()
    winner = None
    is_winners = False
    info = []

    if not is_winners_empty():
        is_winners = False
        info.append({"team_name": ""})
        info.append({"team_name": ""})
        info.append({"team_name": ""})
    else:
        is_winners = True

        conn = sqlite3.connect(DB_WINNERS)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM winners
            ORDER BY id DESC
            LIMIT 3
        """)
        rows = cursor.fetchall()


        for row in rows:
            info.append({
                "id": row[0],
                "year": row[1],
                "team_name": row[2],
                "team_place": row[3],

                "participant_1": row[4],
                "participant_2": row[5],
                "participant_3": row[6],
                "participant_4": row[7],
                "captain_name": row[8],
                "captain_email": row[9],
                "captain_phone": row[10],
            })

        conn.close()

    dateFrom = f'{time_info[0]["day_from"]}.{time_info[0]["month_from"]}.{time_info[0]["year_from"]}'
    dateTo = f'{time_info[0]["day_to"]}.{time_info[0]["month_to"]}.{time_info[0]["year_to"]}'
    return render_template("index_2.html", is_winners=is_winners,
                           winner_1=info[0]["team_name"],
                           winner_2=info[1]["team_name"],
                           winner_3=info[2]["team_name"],
                           dateFrom=dateFrom, dateTo=dateTo)

@app.route("/register", methods=["GET", "POST"])
def register():
    if not is_registration_open():
        return redirect("/")

    if request.method == "POST":
        data = request.get_json()

        try:
            if not data:
                return jsonify({"status": "error", "message": "Пустой JSON"}), 400

            if not data.get("team_name"):
                return jsonify({"status": "error", "message": "Не указано название команды"}), 400

            info = get_participants_info()
            for item in info:
                if str(item["team_name"]).strip().lower() == str(data["team_name"]).strip().lower():
                    return jsonify({
                        "status": "error",
                        "message": "Команда с таким названием уже зарегистрирована"
                    }), 400

            save_participant(data)
            return jsonify({"status": "ok", "message": "Данные сохранены"})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    return render_template("register_team.html")

@app.route("/control-room-7x/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        login_input = request.form.get("login")
        password_input = request.form.get("password")
        admin_info = get_admin_info()
        if login_input == admin_info[0]["login"]:
            if check_password_hash(admin_info[0]["password"], password_input):
                session["role"] = "admin"
                return redirect("/control-room-7x/dashboard")
            else:
                return "<script>alert('Неправильный пароль'); window.location = '/control-room-7x/login';</script>"
        else:
            return "<script>alert('Неправильный логин'); window.location = '/control-room-7x/login';</script>"

    return render_template("login.html")

@app.route("/control-room-7x/dashboard")
def admin():
    if not session.get("role"):
        return redirect("/")

    info = get_participants_info()
    for item in info:
        count = 0

        if item["participant_1"]:
            count += 1
        if item["participant_2"]:
            count += 1
        if item["participant_3"]:
            count += 1
        if item["participant_4"]:
            count += 1

        if item["captain_name"]:
            count += 1

        item["members_count"] = count
    return render_template("admin.html", info=info)

@app.route("/control-room-7x/winners")
def winners():
    if not session.get("role"):
        return redirect("/")

    info = get_winners_info()
    for item in info:
        count = 0

        if item["participant_1"]:
            count += 1
        if item["participant_2"]:
            count += 1
        if item["participant_3"]:
            count += 1
        if item["participant_4"]:
            count += 1

        if item["captain_name"]:
            count += 1

        item["members_count"] = count

    return render_template("winners.html", info=info)

@app.route("/control-room-7x/dashboard/<team_info>")
def team_site(team_info):
    if not session.get("role"):
        return redirect("/")

    info = get_participants_info()

    for item in info:
        count = 0

        if item["participant_1"]:
            count += 1
        if item["participant_2"]:
            count += 1
        if item["participant_3"]:
            count += 1
        if item["participant_4"]:
            count += 1
        if item["captain_name"]:
            count += 1

        item["members_count"] = count

    team = None
    for item in info:
        if item["team_name"] == team_info:
            team = item
            break

    if team is None:
        return "Команда не найдена", 404

    return render_template("team.html", team=team)

@app.route("/control-room-7x/dashboard/give-place/<path:user>", methods=["POST"])
def give_place(user):
    if not session.get("role"):
        return redirect("/")

    data = request.get_json()
    admin_info = get_admin_info()
    team = None

    try:
        if check_password_hash(admin_info[0]["password"], data["password"]):
            info = get_participants_info()

            for item in info:
                if item["team_name"] == user:
                    team = item
                    break

            if team is None:
                return jsonify({"status": "error", "message": "Команда не найдена"}), 404

            add_winner(
                year=str(time.localtime().tm_year),
                team_name=user,
                team_place=data["place"],
                captain_name=team["captain_name"],
                captain_email=team["captain_email"],
                captain_phone=team["captain_phone"],
                participant_1=team["participant_1"],
                participant_2=team["participant_2"],
                participant_3=team["participant_3"],
                participant_4=team["participant_4"]
            )

            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "password-error", "message": "password-error"}), 403

    except Exception as e:
        print("give_place error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/control-room-7x/winners/<team_info>")
def team_winner(team_info):
    if not session.get("role"):
        return redirect("/")

    info = get_winners_info()

    for item in info:
        count = 0

        if item["participant_1"]:
            count += 1
        if item["participant_2"]:
            count += 1
        if item["participant_3"]:
            count += 1
        if item["participant_4"]:
            count += 1
        if item["captain_name"]:
            count += 1

        item["members_count"] = count

    team = None
    for item in info:
        if item["team_name"] == team_info:
            team = item
            break

    if team is None:
        return "Команда не найдена", 404

    return render_template("team_winner.html", team=team)

@app.route("/control-room-7x/time")
def time_site():
    if not session.get("role"):
        return redirect("/")

    info = get_settings_info()

    if not info:
        return render_template("time.html", timeFrom="", timeTo="")

    item = info[0]

    timeFrom = f'{item["year_from"]}-{int(item["month_from"]):02d}-{int(item["day_from"]):02d}'
    timeTo = f'{item["year_to"]}-{int(item["month_to"]):02d}-{int(item["day_to"]):02d}'

    return render_template("time.html", timeFrom=timeFrom, timeTo=timeTo)

@app.route("/control-room-7x/set-time", methods=["POST"])
def set_time():
    if not session.get("role"):
        return redirect("/")

    dateFrom = request.form.get("dateFrom")
    dateTo = request.form.get("dateTo")
    password = request.form.get("password")

    if not dateFrom or not dateTo:
        return "Нет даты", 400
    admin_info = get_admin_info()

    if check_password_hash(admin_info[0]["password"], password):
        year_from, month_from, day_from = dateFrom.split("-")
        year_to, month_to, day_to = dateTo.split("-")

        conn = sqlite3.connect("settings.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE setting
            SET 
                year_from = ?, 
                month_from = ?, 
                day_from = ?,
                year_to = ?, 
                month_to = ?, 
                day_to = ?
            WHERE id = 1
        """, (
            year_from,
            month_from,
            day_from,
            year_to,
            month_to,
            day_to
        ))

        conn.commit()
        conn.close()

    return redirect("/control-room-7x/time")

@app.route("/control-room-7x/winners/delete/<team_info>", methods=["POST"])
def winners_delete(team_info):
    try:
        data = request.get_json()
        admin_info = get_admin_info()

        if check_password_hash(admin_info[0]["password"], data["password"]):
            delete_winner_by_team_name(team_info)
            return jsonify({"status": "ok"})
        else:
            return jsonify({
                "status": "password-error",
                "message": "Неверный пароль"
            }), 401
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": "Неверный пароль"})

@app.route("/control-room-7x/dashboard/delete/<team_info>", methods=["POST"])
def dashboard_delete(team_info):
    try:
        data = request.get_json()
        admin_info = get_admin_info()

        if check_password_hash(admin_info[0]["password"], data["password"]):
            delete_dashboard_by_team_name(team_info)
            return jsonify({"status": "ok"})
        else:
            return jsonify({
                "status": "password-error",
                "message": "Неверный пароль"
            }), 401
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": "Неверный пароль"})

@app.route("/control-room-7x/participants/clear", methods=["POST"])
def clear_participants_route():
    if not session.get("role"):
        return redirect("/")
    try:
        data = request.get_json()
        admin_info = get_admin_info()

        if check_password_hash(admin_info[0]["password"], data["password"]):
            clear_participants()
            return jsonify({"status": "ok"})
        else:
            return jsonify({
                "status": "password-error",
                "message": "Неверный пароль"
            }), 401
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": "Неверный пароль"})

@app.route("/control-room-7x/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
