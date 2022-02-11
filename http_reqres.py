import asyncio
import json


async def request_menu(url: str = ''):
    data = ''
    if url == '':
        print("mocking menu.json from URL")
        await asyncio.sleep(1)
        with open('examples/menu.json', 'r') as f:
            data = json.load(f)
            return data
    else:
        pass #real API request

if __name__ == "__main__":
    menu = asyncio.run(request_menu())
    print(menu)

