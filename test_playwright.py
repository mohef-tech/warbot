from playwright.sync_api import sync_playwright
import httpx
import asyncio
import json

EVENT_ID = "eykcbxuv3djucy1ty"

tokens = {
    "vwar_token": None,
    "room_code": None,
    "widget_code": EVENT_ID
}

def on_request(req):
    if "rest.loket.com" in req.url:
        headers = req.headers
        
        # Tangkap vwar-token
        if headers.get("vwar-token"):
            tokens["vwar_token"] = headers.get("vwar-token")
            print(f"🔑 vwar-token: {tokens['vwar_token'][:30]}...")
        
        # Tangkap room-code
        if headers.get("room-code"):
            tokens["room_code"] = headers.get("room-code")
            print(f"🏠 room-code : {tokens['room_code']}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.on("request", on_request)

    print("🌐 Membuka halaman loket...")
    page.goto(f"https://orion.loket.com/order/{EVENT_ID}",
              timeout=0, wait_until="domcontentloaded")
    page.wait_for_timeout(5000)
    browser.close()

print(f"\n=== TOKEN TERKUMPUL ===")
print(f"vwar_token  : {tokens['vwar_token']}")
print(f"room_code   : {tokens['room_code']}")
print(f"widget_code : {tokens['widget_code']}")

# Hit endpoint tickets dengan token
if tokens["vwar_token"] and tokens["room_code"]:
    async def check_tickets():
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "accept-language": "EN",
            "referer": "https://orion.loket.com/",
            "vwar-token": tokens["vwar_token"],
            "room-code": tokens["room_code"],
            "widget-code": tokens["widget_code"],
        }
        url = f"https://rest.loket.com/orion/api/v1/orders/{EVENT_ID}/tickets"
        async with httpx.AsyncClient(headers=headers) as client:
            print(f"\n🎯 Hit endpoint tickets...")
            response = await client.get(url)
            print(f"📥 Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("\n=== DATA TIKET ===")
                print(json.dumps(data, indent=2))
            else:
                print(f"❌ Response: {response.text}")

    asyncio.run(check_tickets())
else:
    print("❌ Token belum lengkap")