import httpx
import asyncio
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}

async def save_session(client, filename="session.json"):
    cookies = dict(client.cookies)
    with open(filename, "w") as f:
        json.dump(cookies, f)
    print(f"session disimpan ke {filename}: {cookies}")

async def load_session(client, filename="session.json"):
    try:
        with open(filename, "r") as f:
            cookies = json.load(f)
        for key, value in cookies.items():
            client.cookies.set(key, value)
        print(f"session di-load dari {filename}: {cookies}")
        return True
    except FileNotFoundError:
        print(f" Belum ada session tersimpan, perlu login dulu!")
        return false

async def main():
    async with httpx.AsyncClient(headers=HEADERS) as client:
        
        # Simulasi Login -> dapat cookies
        print("=== Step 1: LOGIN, dapat cookies===")
        await client.get("https://httpbin.org/cookies/set?bot_session=mohef123&user_id=99")
        await save_session(client)

    # simulasi bot restart, buat client baru, session kosong
    print("\n=== Step 2: BOT RESTART, buat client baru, session kosong ===")
    async with httpx.AsyncClient(headers=HEADERS) as client2:

        # load session dari file
        loaded = await load_session(client2)

        if loaded:
            #verifikasi session masih valid
            response = await client2.get("https://httpbin.org/cookies")
            body = response.json()
            print(f"\nCookie yang diterima server: {body['cookies']}")

            if body['cookies'].get('bot_session'):
                print("Session berhasil dipulihkan - siap war tanpa login ulang!")
                
asyncio.run(main())