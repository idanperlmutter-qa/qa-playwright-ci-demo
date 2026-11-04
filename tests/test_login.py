
from playwright.sync_api import Page, expect


def test_successful_login(page: Page):
    page.goto("http://127.0.0.1:5000/login")

    page.get_by_label("Email").fill("test@example.com")
    page.get_by_label("Password").fill("123456")

    page.get_by_role("button", name="Log in").click()

    expect(page).to_have_url("http://127.0.0.1:5000/dashboard")
    expect(page.get_by_role("heading", name="Welcome back")).to_be_visible()


def test_invalid_login(page: Page):
    page.goto("http://127.0.0.1:5000/login")

    page.get_by_label("Email").fill("test@example.com")
    page.get_by_label("Password").fill("wrong123")

    page.get_by_role("button", name="Log in").click()

    expect(page).to_have_url("http://127.0.0.1:5000/login")
    expect(page.get_by_role("alert")).to_have_text(
        "Invalid email or password"
    )


def test_login_with_empty_password(page: Page):
    page.goto("http://127.0.0.1:5000/login")

    page.get_by_label("Email").fill("test@example.com")
    password = page.get_by_label("Password")
    password.fill("")

    login_posts = []
    page.on(
        "request",
        lambda request: login_posts.append(request)
        if request.method == "POST"
        and request.url == "http://127.0.0.1:5000/login"
        else None,
    )

    page.get_by_role("button", name="Log in").click()

    expect(page).to_have_url("http://127.0.0.1:5000/login")
    expect(password).to_have_value("")
    assert password.evaluate("element => element.validity.valueMissing")
    expect(page.get_by_role("alert")).to_have_count(0)
    assert login_posts == []


def test_login_with_empty_email(page: Page):
    page.goto("http://127.0.0.1:5000/login")

    email = page.get_by_label("Email")
    email.fill("")
    page.get_by_label("Password").fill("123456")

    login_posts = []
    page.on(
        "request",
        lambda request: login_posts.append(request)
        if request.method == "POST"
        and request.url == "http://127.0.0.1:5000/login"
        else None,
    )

    page.get_by_role("button", name="Log in").click()

    expect(page).to_have_url("http://127.0.0.1:5000/login")
    expect(email).to_have_value("")
    assert email.evaluate("element => element.validity.valueMissing")
    assert not email.evaluate("element => element.validity.valid")
    expect(page.get_by_role("alert")).to_have_count(0)
    assert login_posts == []


