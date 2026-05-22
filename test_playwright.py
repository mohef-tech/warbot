from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    captured = []

    def on_request(req):
        if any(x in req.url for x in ["api", "ticket", "order", "loket"]):
            captured.append(f"📤 {req.method} {req.url}")

    def on_response(res):
        if any(x in res.url for x in ["api", "ticket", "order", "loket"]):
            captured.append(f"📥 {res.status} {res.url}")

    page.on("request", on_request)
    page.on("response", on_response)

    page.goto("https://orion.loket.com/order/eykcbxuv3djucy1ty",
              timeout=0, wait_until="domcontentloaded")

    page.wait_for_timeout(3000)

    print("\n=== HASIL INTERCEPT ===")
    for item in captured:
        print(item)

    input("\nTekan Enter untuk close...")
    browser.close()