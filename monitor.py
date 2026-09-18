import os
import re
import json
import requests

STATE_FILE = "state.json"

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

TARGET_URL = "https://www.passo.com.tr"


def normalize(text: str) -> str:
    text = text.lower()
    replacements = {
        "ı": "i", "ş": "s", "ğ": "g",
        "ö": "o", "ü": "u", "ç": "c",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def has_both_teams(text: str) -> bool:
    """'amed' ve 'besiktas' kelimelerinin TAM kelime olarak geçtiğini kontrol eder.
    Bu sayede 'Samed Behrengi' gibi içinde 'amed' harfleri geçen ama
    ilgisiz sonuçlar yanlışlıkla eşleşme yaratmaz."""
    has_amed = re.search(r"\bamed\b", text) is not None
    has_besiktas = "besiktas" in text
    return has_amed and has_besiktas


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"found": False}


def save_state(state: dict) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def send_telegram(message: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    resp = requests.post(
        url,
        data={"chat_id": TELEGRAM_CHAT_ID, "text": message},
        timeout=15,
    )
    print("Telegram response:", resp.status_code, resp.text[:200])


def check_duckduckgo() -> tuple[bool, str | None]:
    """DuckDuckGo HTML aramasında iki takımın adı ve passo.com.tr birlikte geçiyor mu diye bakar."""
    query = "amedspor besiktas bilet passo"
    url = "https://html.duckduckgo.com/html/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        resp = requests.post(url, data={"q": query}, headers=headers, timeout=20)
        text = normalize(resp.text)
        if has_both_teams(text) and "passo.com.tr" in text:
            return True, "DuckDuckGo arama sonucu"
    except Exception as exc:
        print("DuckDuckGo kontrolü başarısız:", exc)
    return False, None


def check_passo_playwright() -> tuple[bool, str | None]:
    """Passo'nun kendi arama sayfasını gerçek bir tarayıcı ile (JS render ederek) kontrol eder."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright kurulu değil, bu kontrol atlanıyor.")
        return False, None

    search_url = "https://www.passo.com.tr/tr/arama?q=amedspor"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(search_url, timeout=30000)
            page.wait_for_timeout(5000)
            content = normalize(page.content())
            browser.close()
            if has_both_teams(content):
                return True, "Passo arama sayfası"
    except Exception as exc:
        print("Passo (Playwright) kontrolü başarısız:", exc)
    return False, None


def main() -> None:
    state = load_state()
    if state.get("found"):
        print("Daha önce bulunmuş ve bildirilmiş, tekrar kontrol edilmiyor.")
        return

    found_ddg, source_ddg = check_duckduckgo()
    found_passo, source_passo = check_passo_playwright()

    if found_ddg or found_passo:
        source = source_passo or source_ddg
        message = (
            "🎟️ Amedspor - Beşiktaş bileti görünüyor olabilir!\n"
            f"Kaynak: {source}\n"
            "Hemen kontrol et: https://www.passo.com.tr"
        )
        send_telegram(message)
        state["found"] = True
        save_state(state)
        print("Bildirim gönderildi, state.json güncellendi.")
    else:
        print("Henüz bulunamadı.")


if __name__ == "__main__":
    main()
