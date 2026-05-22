from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto("https://orion.loket.com/order/eykcbxuv3djucy1ty")
    page.wait_for_load_state("networkidle")
    
    print("✅ Halaman berhasil dibuka!")
    print(f"Title: {page.title()}")
    
    browser.close()