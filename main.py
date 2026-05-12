import httpx
import asyncio

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}

async def main():
    async with httpx.AsyncClient(headers=HEADERS) as client:
        
        # Hit endpoint yang set cookie
        response = await client.get("https://httpbin.org/cookies/set?bot_session=abc123&user_id=42")
        
        print("=== COOKIES TERSIMPAN ===")
        print(dict(client.cookies))

asyncio.run(main())