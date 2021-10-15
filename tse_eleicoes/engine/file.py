from csv import DictReader
from pathlib import Path
from typing import Any
from zipfile import ZipFile


class StopFileIteration(Exception):
    pass


class ZipReader:
    def __init__(self, file: Path, encoding: str = 'UTF-8') -> None:
        self._file = file
        self._encoding = encoding

    def __enter__(self) -> 'ZipReader':
        self._fp = self._file.open(mode='rb')
        self._zp = ZipFile(self._fp)
        self._config()
        self._dict_reader = self._reader()
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self._fp.close()
        self._zp.close()

    def __iter__(self) -> 'ZipReader':
        return self

    def __next__(self) -> dict[str, Any]:
        try:
            return next(self._dict_reader)
        except StopIteration:
            self._i += 1
            self._dict_reader = self._reader()
            return self.__next__()
        except StopFileIteration as e:
            raise StopIteration from e

    def _config(self) -> None:
        self._filenames = [
            a
            for a in self._zp.namelist()
            if a.endswith('.csv') and not a.endswith('_BRASIL.csv')
        ]
        self._i = 0

        with self._zp.open(self._filenames[0]) as f:
            fieldnames = f.readline()\
                .decode(self._encoding)\
                .replace('"', '')\
                .replace('\n', '')\
                .split(';')

        self._fieldnames = fieldnames

    def _reader(self) -> dict[str, Any]:
        try:
            filename = self._filenames[self._i]
        except IndexError as e:
            raise StopFileIteration from e 

        with self._zp.open(filename) as f:
            f.readline()  # Skip header
            reader = DictReader(
                (line.decode(self._encoding) for line in f),
                fieldnames=self._fieldnames,
                delimiter=';',
                quotechar='"',
            )
            for line in reader:
                yield line
