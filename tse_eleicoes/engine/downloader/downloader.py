from pathlib import Path
from httpx import HTTPStatusError, codes
from aletheia.scraper.downloader import DefaultDownloader
from .exceptions import FileNotAvailable


class Downloader(DefaultDownloader):
    async def download(self, output_folder: Path) -> Path:
        try:
            return await super().download(output_folder)
        except HTTPStatusError as e:
            if e.response.status_code == codes.NOT_FOUND:
                raise FileNotAvailable from e
            else:
                raise e
