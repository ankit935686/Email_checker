import httpx
import re

async def etsy(email, client, out):
    name = "etsy"
    domain = "etsy.com"
    method = "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Origin': 'https://www.etsy.com',
        'Referer': 'https://www.etsy.com/',
    }

    try:
        # Check if email exists on Etsy by attempting to register
        url = "https://www.etsy.com/api/v3/ajax/member/register"
        data = {
            "email": email,
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = await client.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            response_data = response.json()
            if "email" in response_data.get("error", {}).get("message", "").lower():
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                            "rateLimit": False,
                            "exists": True,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
            else:
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                            "rateLimit": False,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
        else:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": f"HTTP {response.status_code}"})
    except Exception as e:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": str(e)}) 