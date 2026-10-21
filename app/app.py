
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)

LOGIN_PAGE = """
<h1>Login</h1>

<form method="POST">
    <label for="email">Email</label>
    <input id="email" name="email" type="email" required>

    <label for="password">Password</label>
    <input id="password" name="password" type="password" required>

    <button type="submit">Log in</button>
</form>

{% if error %}
<p role="alert">{{ error }}</p>
{% endif %}
"""


@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == "test@example.com" and password == "123456":
            return redirect("/dashboard")

        return render_template_string(
            LOGIN_PAGE, error="Invalid email or password"
        )

    return render_template_string(LOGIN_PAGE, error=None)


@app.route("/dashboard")
def dashboard():
    return "<h1>Welcome back</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
