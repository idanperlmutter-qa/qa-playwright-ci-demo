
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


