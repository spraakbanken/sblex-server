import asyncio
import json

import httpx


async def main():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        print_response(await client.get("/fl/json/t"))
        print_response(await client.get("/lid/json/dväljas..vb.1"))
        # print_response(r)


def print_response(r):
    print()
    print(f"=== Response for {r._request.method} {r.url}")
    print(f"=> Status       : {r.status_code} {r.reason_phrase}")
    print("=> Headers      : ")
    for header, header_value in r.headers.items():
        print(f"   {header}: {header_value}")
    print("=> Response Body :")
    print(f"{json.dumps(r.json(),indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())
