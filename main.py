import httpx
import asyncio
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
}

async def fetch(client, url, label):
    response = await client.get(url)
    body = response.json()
    print(f"[{label}] Status: {response.status_code} | User-Agent: {body['headers']['User-Agent'][:40]}")

async def main():
    urls = [
        ("https://httpbin.org/get", "Request-1"),
        ("https://httpbin.org/get", "Request-2"),
        ("https://httpbin.org/get", "Request-3"),
    ]

    async with httpx.AsyncClient(headers=HEADERS) as client:
        start = time.time()
        await asyncio.gather(*[fetch(client, url, label) for url, label in urls])
        print(f"\nSelesai dalam: {time.time() - start:.2f} detik")

asyncio.run(main())