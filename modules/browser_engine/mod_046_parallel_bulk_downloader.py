import asyncio
import os

import aiohttp


async def download_file(session: aiohttp.ClientSession, url: str, dest: str):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            resp.raise_for_status()
            content = await resp.read()
            os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
            with open(dest, "wb") as f:
                f.write(content)
            return (url, True, dest)
    except Exception as e:
        return (url, False, str(e))


async def bulk_download(urls: list[str], dest_dir: str = "downloads") -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(urls):
            filename = url.split("/")[-1] or f"file_{i}"
            dest = os.path.join(dest_dir, filename)
            tasks.append(download_file(session, url, dest))
        results = await asyncio.gather(*tasks)
    return [{"url": url, "success": ok, "path": msg} for url, ok, msg in results]


def download_all(urls: list[str], dest_dir: str = "downloads") -> list[dict]:
    return asyncio.run(bulk_download(urls, dest_dir))
