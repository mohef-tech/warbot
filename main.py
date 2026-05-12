import httpx
import asyncio

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}

async def main():
    async with httpx.AsyncClient(headers=HEADERS) as client:
        
        # Simulasi Login -> dapat cookies
        print("=== Step 1: LOGIN, dapat cookies===")
        await client.get("https://httpbin.org/cookies/set?bot_session=mohef123&user_id=99")
        print(f"Cookies tersimpan: {dict(client.cookies)}")

        # Simulasi: request berikutnya -> cookies otomatis terkirim
        print("\n=== Step 2 : Request berikutnya, cookies otomatis terkirim ===")
        response = await client.get("https://httpbin.org/cookies")
        body = response.json()
        print(f"Cookie yang diterima server: {body['cookies']}")

        print("\n=== Step 3 Verifikasi ===")
        if body['cookies'].get('bot_session') == 'mohef123':
            print("✅ session aktif - bot siap eksekusi")
        else:
            print("❌ Session hilang!")

        # # Hit endpoint yang set cookie
        # response = await client.get("https://httpbin.org/cookies/set?bot_session=abc123&user_id=42")
        
        # print("=== COOKIES TERSIMPAN ===")
        # print(dict(client.cookies))

asyncio.run(main())