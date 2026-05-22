import httpx
import asyncio
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
    "Referer": "https://orion.loket.com/",
}

EVENT_ID = "eykcbxuv3djucy1ty"

async def check_event_info():
    url = f"https://rest.loket.com/orion/api/v1/events/{EVENT_ID}/info"
    
    async with httpx.AsyncClient(headers=HEADERS) as client:
        print(f"🎯 Hit endpoint: {url}")
        response = await client.get(url)
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n=== RESPONSE ===")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ Response: {response.text}")

asyncio.run(check_event_info())