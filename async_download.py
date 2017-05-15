import asyncio
import os
import requests as req

async def download(url):
    res = req.get(url)
    filename = os.path.basename('./a')

    with open(filename,"wb") as fp:
        fp.write(res.content)
        msg = "{filename} OK!".format(filename = filename)
        return msg

async def main(urls):
    coroutines = [download(url) for url in urls]
    completed,pending = await asyncio.wait(coroutines)
    for item in completed:
        print(item.result())

if __name__ == "__main__":
    urls = ["http://www.huawei.com/"]
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(urls))
    finally:
        event_loop.close()
