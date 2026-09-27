import os
import re
import webbrowser
import urllib.parse
import tempfile
import time

import pyautogui

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from ai import ask_ai
from speech import transcribe_audio


app = Flask(__name__)
CORS(app)


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)


# ==========================================
# FRONTEND
# ==========================================

@app.route("/")
def home():
    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(
        FRONTEND_DIR,
        filename
    )


# ==========================================
# OPEN WEBSITE
# ==========================================

def open_website(url):
    webbrowser.open_new_tab(url)
    time.sleep(1)


# ==========================================
# CLOSE CURRENT BROWSER TAB
# ==========================================

def close_current_tab():

    try:

        # Make sure the browser is active
        pyautogui.hotkey("ctrl", "w")

        time.sleep(1)

        return True

    except Exception as e:

        print("CLOSE ERROR:", e)

        return False


# ==========================================
# SEARCH QUERY CLEANER
# ==========================================

def clean_search_query(text, website):

    query = text.lower().strip()


    # Remove common commands
    remove_words = [
        "search",
        "search karo",
        "search kar do",
        "search karna",
        "dhoondo",
        "dhoondho",
        "find",
        "find karo",
        "play",
        "chalao",
        "chala do",
        "karo",
        "kar do"
    ]


    for word in remove_words:

        query = query.replace(
            word,
            " "
        )


    # Remove website name
    query = query.replace(
        website,
        " "
    )


    # Remove common Roman Urdu connectors
    connectors = [
        "par",
        "pe",
        "per",
        "mein",
        "me",
        "py",
        "pr"
    ]


    for word in connectors:

        query = re.sub(
            r"\b" + re.escape(word) + r"\b",
            " ",
            query
        )


    # Clean extra spaces
    query = re.sub(
        r"\s+",
        " ",
        query
    ).strip()


    return query


# ==========================================
# COMMAND HANDLER
# ==========================================

def handle_command(message):

    text = message.lower().strip()

    print("VOICE COMMAND:", text)


    # ======================================
    # GOOGLE SEARCH
    # ======================================

    if "google" in text:

        close_words = [
            "close",
            "band",
            "band karo",
            "band kar do",
            "close karo",
            "close kar do"
        ]

        if any(word in text for word in close_words):

            if close_current_tab():

                return "Google tab band kar diya."

            return "Google tab band nahi ho saka."


        search_words = [
            "search",
            "dhoondo",
            "dhoondho",
            "find"
        ]


        if any(
            word in text
            for word in search_words
        ):

            query = clean_search_query(
                text,
                "google"
            )


            if query:

                url = (
                    "https://www.google.com/search?q="
                    + urllib.parse.quote(query)
                )

                open_website(url)

                return (
                    f"Google par {query} "
                    "search kar diya."
                )


        # Google open
        if any(
            word in text
            for word in [
                "open",
                "khol",
                "kholo",
                "khol do"
            ]
        ):

            open_website(
                "https://www.google.com"
            )

            return "Google khol diya hai."


    # ======================================
    # YOUTUBE
    # ======================================

    if "youtube" in text:

        close_words = [
            "close",
            "band",
            "band karo",
            "band kar do",
            "close karo",
            "close kar do"
        ]


        if any(
            word in text
            for word in close_words
        ):

            if close_current_tab():

                return "YouTube tab band kar diya."

            return "YouTube tab band nahi ho saka."


        search_words = [
            "search",
            "dhoondo",
            "dhoondho",
            "find",
            "play",
            "chalao",
            "chala do"
        ]


        if any(
            word in text
            for word in search_words
        ):

            query = clean_search_query(
                text,
                "youtube"
            )


            if query:

                url = (
                    "https://www.youtube.com/results?search_query="
                    + urllib.parse.quote(query)
                )

                open_website(url)

                return (
                    f"YouTube par {query} "
                    "search kar diya."
                )


        # YouTube open
        if any(
            word in text
            for word in [
                "open",
                "khol",
                "kholo",
                "khol do"
            ]
        ):

            open_website(
                "https://www.youtube.com"
            )

            return "YouTube khol diya hai."


    # ======================================
    # WHATSAPP
    # ======================================

    if "whatsapp" in text:

        if any(
            word in text
            for word in [
                "open",
                "khol",
                "kholo",
                "khol do"
            ]
        ):

            open_website(
                "https://web.whatsapp.com"
            )

            return "WhatsApp Web khol diya hai."


    # ======================================
    # GMAIL
    # ======================================

    if "gmail" in text:

        if any(
            word in text
            for word in [
                "open",
                "khol",
                "kholo",
                "khol do"
            ]
        ):

            open_website(
                "https://mail.google.com"
            )

            return "Gmail khol diya hai."


    # ======================================
    # INSTAGRAM
    # ======================================

    if "instagram" in text:

        if any(
            word in text
            for word in [
                "open",
                "khol",
                "kholo",
                "khol do"
            ]
        ):

            open_website(
                "https://www.instagram.com"
            )

            return "Instagram khol diya hai."


    # ======================================
    # FACEBOOK
    # ======================================

    if "facebook" in text:

        if any(
            word in text
            for word in [
                "open",
                "khol",
                "kholo",
                "khol do"
            ]
        ):

            open_website(
                "https://www.facebook.com"
            )

            return "Facebook khol diya hai."


    # ======================================
    # GITHUB
    # ======================================

    if "github" in text:

        if any(
            word in text
            for word in [
                "open",
                "khol",
                "kholo",
                "khol do"
            ]
        ):

            open_website(
                "https://github.com"
            )

            return "GitHub khol diya hai."


    # ======================================
    # GOOGLE MAPS
    # ======================================

    if "maps" in text:

        if any(
            word in text
            for word in [
                "open",
                "khol",
                "kholo",
                "khol do"
            ]
        ):

            open_website(
                "https://maps.google.com"
            )

            return "Google Maps khol diya hai."


    # ======================================
    # CALCULATOR
    # ======================================

    if "calculator" in text:

        if any(
            word in text
            for word in [
                "open",
                "khol",
                "kholo",
                "khol do"
            ]
        ):

            open_website(
                "https://www.google.com/search?q=calculator"
            )

            return "Calculator khol diya hai."


    return None


# ==========================================
# CHAT API
# ==========================================

@app.route(
    "/api/chat",
    methods=["POST"]
)
def chat():

    try:

        data = request.get_json()

        message = data.get(
            "message",
            ""
        ).strip()


        if not message:

            return jsonify({
                "error": "Message is empty."
            }), 400


        command_result = handle_command(
            message
        )


        if command_result:

            return jsonify({
                "reply": command_result,
                "command": True
            })


        # Normal AI question
        answer = ask_ai(message)


        return jsonify({
            "reply": answer,
            "command": False
        })


    except Exception as e:

        print("CHAT ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# VOICE TRANSCRIPTION
# ==========================================

@app.route(
    "/api/transcribe",
    methods=["POST"]
)
def transcribe():

    try:

        if "audio" not in request.files:

            return jsonify({
                "error": "No audio file received."
            }), 400


        audio = request.files["audio"]


        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".webm"
        )


        audio.save(
            temp_file.name
        )

        temp_file.close()


        text = transcribe_audio(
            temp_file.name
        )


        os.remove(
            temp_file.name
        )


        return jsonify({
            "text": text
        })


    except Exception as e:

        print(
            "TRANSCRIPTION ERROR:",
            e
        )

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# START
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )