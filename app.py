from flask import Flask, request, render_template, redirect, url_for
from instagrapi import Client
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def instagram_server():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")
        choice = request.form.get("choice")
        target_username = request.form.get("target_username")
        thread_id = request.form.get("thread_id")
        haters_name = request.form.get("haters_name")
        delay = int(request.form.get("delay"))
        
        # Handle uploaded file
        message_file = request.files["message_file"]
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], message_file.filename)
        message_file.save(file_path)

        # Read messages from file
        with open(file_path, "r") as file:
            messages = file.readlines()

        # Login to Instagram
        cl = Client()
        try:
            cl.login(username, password)
        except Exception as e:
            return f"Login failed: {e}"

        # Send messages
        try:
            for message in messages:
                message = message.strip()
                if choice == "inbox":
                    cl.direct_send(message, [target_username])
                elif choice == "group":
                    cl.direct_send(message, [], thread_id)
                time.sleep(delay)  # Delay between messages
        except Exception as e:
            return f"Error sending messages: {e}"
        finally:
            os.remove(file_path)  # Clean up uploaded file

        return "Messages sent successfully!"
    return render_template("form.html")  # Serve the HTML form

if __name__ == "__main__":
    app.run(debug=True)
