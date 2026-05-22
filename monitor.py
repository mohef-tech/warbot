from playwright.sync_api import sync_playwright
import httpx
import asyncio
import json
from datetime import datetime

EVENT_ID = "eykcbxuv3djucy1ty"
POLLING_INTERVAL = 5  # cek tiap 5 detik
TARGET_TICKET = None  # None = monitor semua, atau isi nama tiket spesifik

tokens = {
    "vwar_token": None,
    "room_code": None,
    "widget_code": EVENT_ID
}

def on_request(req):
    if "rest.loket.com" in req.url:
        headers = req.headers
        if headers.get("vwar-token"):
            tokens["vwar_token"] = headers.get("vwar-token")
        if headers.get("room-code"):
            tokens["room_code"] = headers.get("room-code")
        
        # Tambah ini — print SEMUA headers ke /tickets
        if "tickets" in req.url:
            print(f"\n🔍 SEMUA HEADERS KE /tickets:")
            for key, value in headers.items():
                print(f"   {key}: {value}")

def get_tokens():
    print("🌐 Ambil token dari loket...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # ← ganti True ke False dulu untuk test
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        )
        page = context.new_page()
        page.on("request", on_request)
        page.goto(f"https://orion.loket.com/order/{EVENT_ID}",
                  timeout=0, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)
        browser.close()
    
    if tokens["vwar_token"] and tokens["room_code"]:
        print(f"✅ Token siap!")
        return True
    return False

async def fetch_tickets():
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
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()["results"]
        elif response.status_code == 401:
            print(f"⚠️  Token expired: {response.text}")
            return None
        return None

async def polling():
    prev_status = {}  # simpan status sebelumnya
    
    print(f"\n🔄 Mulai polling tiap {POLLING_INTERVAL} detik...")
    print("=" * 50)

    while True:
        now = datetime.now().strftime("%H:%M:%S")
        tickets = await fetch_tickets()

        if tickets is None:
            print(f"[{now}] ❌ Gagal fetch, coba lagi...")
            await asyncio.sleep(POLLING_INTERVAL)
            continue

        # Cek perubahan
        for ticket in tickets:
            name = ticket["ticket_type"]
            status = ticket["status_ticket_name"]
            qty = ticket["available_quantity"]

            # Deteksi perubahan status
            if name in prev_status:
                old_status = prev_status[name]["status"]
                if old_status != status:
                    print(f"\n🚨 [{now}] PERUBAHAN TERDETEKSI!")
                    print(f"   {name}")
                    print(f"   {old_status} → {status} ({qty} tiket)")
                    
                    if status == "Available":
                        print(f"   ✅ TIKET TERSEDIA — TRIGGER CHECKOUT!")
                        # Nanti di sini kita tambah auto-checkout
            
            prev_status[name] = {"status": status, "qty": qty}

        # Print status semua tiket
        print(f"\n[{now}] Status tiket:")
        for ticket in tickets:
            icon = "✅" if ticket["status_ticket_name"] == "Available" else "❌"
            print(f"  {icon} {ticket['ticket_type']:<40} {ticket['status_ticket_name']} ({ticket['available_quantity']} tiket)")

        await asyncio.sleep(POLLING_INTERVAL)

# Main
if get_tokens():
    asyncio.run(polling())
else:
    print("❌ Gagal dapat token")