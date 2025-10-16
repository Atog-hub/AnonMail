from flask import Flask, request, render_template_string
import smtplib , os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

#CONFIG
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

#FLASK APP
app = Flask(__name__)

#HELPER FUNCTION
def send_email(recipient, user_message):
    """Send an email via Gmail SMTP with error handling."""
    if not recipient or not user_message:
        print("❌ Recipient or message is empty!")
        return False

    try:
        msg = MIMEText(user_message, "plain", "utf-8")
        msg["Subject"] = "📩 Your AnonMail Message"
        msg["From"] = EMAIL_USER
        msg["To"] = recipient

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        print(f"✅ Email sent to {recipient}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed: check your email or app password.")
        return False
    except smtplib.SMTPRecipientsRefused:
        print("❌ Recipient refused. Check the email address.")
        return False
    except smtplib.SMTPException as e:
        print("❌ SMTP error:", e)
        return False
    except Exception as e:
        print("❌ Unknown error:", e)
        return False


#ROUTES
@app.route("/", methods=["GET", "POST"])
def index():
    message_sent = False  # flag to show success message
    error_message = None

    if request.method == "POST":
        recipient = request.form.get("recipient")
        msg = request.form.get("message")

        success = send_email(recipient, msg)
        if success:
            message_sent = True
        else:
            error_message = "❌ Failed to send email. Check console logs."

    return render_template_string(
        """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AnonMail</title>
        <style>
            body { font-family: Arial; text-align: center; margin-top: 50px; background-color: #f5f5f5; }
            input, textarea { padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
            button { padding: 10px 20px; border-radius: 5px; background-color: #10069c; color: white; border: none; font-size: 16px; cursor: pointer; }
            button:hover { background-color: #070247; }
            .success { color: green; margin-top: 10px; font-weight: bold; }
            .error { color: red; margin-top: 10px; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🤫 AnonMail</h1>
        <form method="post">
            <p><input type="email" name="recipient" placeholder="Recipient Email" required style="width: 300px;"></p>
            <p><textarea name="message" placeholder="Your message..." rows="5" cols="40" required></textarea></p>
            <button type="submit">📤 Send Mail</button>
        </form>

        {% if message_sent %}
            <div id="success-msg" class="success">✅ Message sent successfully!</div>
            <script>
                setTimeout(function() {
                    var msg = document.getElementById("success-msg");
                    if(msg) msg.style.display = "none";
                }, 3000);
            </script>
        {% elif error_message %}
            <div class="error">{{ error_message }}</div>
        {% endif %}
    </body>
    </html>
    """,
        message_sent=message_sent,
        error_message=error_message,
    )


#MAIN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
