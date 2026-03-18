from flask import Flask, jsonify, request
import subprocess
import json

from user_database import *

init_database()

app = Flask(__name__)


@app.route("/", methods=["GET"]) # stamm route erstellen
def index():
    return jsonify({
        "success": True,
        "message": "API ist Aktiv"
    })


@app.route("/auth", methods=["POST"]) # route für anmeldung und registrierung erstellen
def auth():
    try:
        body = request.get_json(silent=True) or {} # empfangene daten zwischenspeichern

        # daten auslesen
        username = body.get("username")
        password = body.get("password")
        action = body.get("action")

        print(body)

        # fehler behandlung
        if not username or not isinstance(username, str):
            return jsonify({
                "success": False,
                "error": "Username fehlt"
            }), 400

        if not password or not isinstance(password, str):
            return jsonify({
                "success": False,
                "error": "Passwort fehlt"
            }), 400

        if action not in ["login", "signup"]:
            return jsonify({
                "success": False,
                "error": "Ungültige aktion"
            }), 400

        # login verarbeiten
        if action == "login":
            if authenticate_user(username, password):
                xp = get_user_xp(username) # xp abfragen damit wir dies an den client weiter leiten können
                # daten an den client senden
                return jsonify({
                    "success": True,
                    "message": "login successful",
                    "username": username,
                    "xp": xp
                })
            else:
                return jsonify({
                    "success": False,
                    "message": "login failed"
                }), 401
        # registrierung verarbeiten (prozesse funktionieren wie beim login)
        if action == "signup":
            try:
                add_user(username, password)
                xp = get_user_xp(username)

                return jsonify({
                    "success": True,
                    "message": "signup successful",
                    "username": username,
                    "xp": xp
                })
            except Exception as e:
                return jsonify({
                    "success": False,
                    "message": f"signup failed: {str(e)}"
                }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# slotmaschienen route erstellen
@app.route("/SlotMaschineSpin", methods=["POST"])
def spin():
    try:
        body = request.get_json(silent=True) or {}

        print(body)
        # spiel für user starten
        username = body.get("username")
        bet = body.get("bet", 10)
        # java kommunikation
        try:
            bet = int(bet)
        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "error": "Ungültiger Einsatz"
            }), 400
        # fehler behandlung für netzwerk komunikation
        if not username or not isinstance(username, str):
            return jsonify({
                "success": False,
                "error": "Benutzername fehlt"
            }), 400

        if not user_exists(username):
            return jsonify({
                "success": False,
                "error": "Benutzer existiert nicht"
            }), 404

        if bet <= 0:
            return jsonify({
                "success": False,
                "error": "Ungültiger Einsatz"
            }), 400

        current_xp = get_user_xp(username)

        if current_xp is None:
            return jsonify({
                "success": False,
                "error": "XP konnten nicht geladen werden"
            }), 500

        if current_xp < bet:
            return jsonify({
                "success": False,
                "error": "Nicht genug XP"
            }), 400

        result = subprocess.run(
            ["java", "SLotmaschine.SlotsApi"],
            capture_output=True,
            text=True,
            check=True
        )

        output = result.stdout.strip()
        data = json.loads(output)

        payout = data["payout"]
        net = payout - bet

        add_xp(username, net)
        new_xp = get_user_xp(username)

        # daten an client zurücksenden
        win1 = data.get("slot1")
        win2 = data.get("slot2")
        win3 = data.get("slot3")

        wins = [win1, win2, win3]

        data["win1"] = win1
        data["win2"] = win2
        data["win3"] = win3
        data["wins"] = wins

     
        return jsonify({
            "success": True,
            "result": data
        })
    # fehler behandlung für java API
    except subprocess.CalledProcessError as e:
        return jsonify({
            "success": False,
            "error": "java prozes fehlgeschlagen",
            "details": e.stderr
        }), 500

    except json.JSONDecodeError:
        return jsonify({
            "success": False,
            "error": "kein gültiges JSON erhalten",
            "raw_output": result.stdout
        }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# app starten
if __name__ == "__main__":
    app.run(debug=True, port=8080)