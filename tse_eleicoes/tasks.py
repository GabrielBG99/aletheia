import asyncio
from contextlib import suppress
from datetime import date
from pathlib import Path
from django.conf import settings
from django.db import IntegrityError
from .scraper.client import Client
from .models import Release, Download, Insert
from .engine.downloader.downloader import Downloader
from .engine.downloader.exceptions import FileNotAvailable


def insert(id: str) -> None:
    pass


def download(id: str) -> None:
    t: Download = Download.objects.get(pk=id)
    if t.finished:
        return

    folder = Path(t.release.folder) / str(t.type)
    d = Downloader(t.uri)

    try:
        file = asyncio.run(d.download(folder))
    except FileNotAvailable:
        t.finished = True
        t.save()
        return

    i = Insert.objects.create(release=t.release, file=file.as_posix())
    insert.s(id=i.pk).apply_async()

    t.finished = True
    t.save()


def sync() -> None:
    client = Client()
    electoral_parties, response = asyncio.run(client.summary())

    current_year = date.today().year
    folder: Path = settings.DOWNLOAD_ROOT / f'TSEELEICOES-{current_year}'

    with suppress(IntegrityError):
        r = Release.objects.create(year=current_year, folder=folder.as_posix())
        folder.mkdir(exist_ok=True)

        d = Download.objects.create(
            release=r,
            type=Download.Type.PARTY_MEMBER,
            uri=electoral_parties.party_bodies,
        )
        download.s(id=d.pk).apply_async()

        d = Download.objects.create(
            release=r,
            type=Download.Type.DELEGATE,
            uri=electoral_parties.party_delegates,
        )
        download.s(id=d.pk).apply_async()

    for r in response:
        if r.year == current_year:
            release = Release.objects.get(year=current_year)
        else:
            folder: Path = settings.DOWNLOAD_ROOT / f'TSEELEICOES-{r.year}'
            try:
                release = Release.objects.create(year=r.year, folder=folder.as_posix())
            except IntegrityError:
                continue
            else:
                folder.mkdir(exist_ok=True)

        d = Download.objects.create(
            release=release,
            type=Download.Type.CANDIDATE,
            uri=r.candidates.candidates,
        )
        download.s(id=d.pk).apply_async()

        d = Download.objects.create(
            release=release,
            type=Download.Type.REMOVAL,
            uri=r.candidates.removal,
        )
        download.s(id=d.pk).apply_async()
