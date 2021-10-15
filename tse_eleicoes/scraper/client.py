from dataclasses import dataclass
import httpx
from bs4 import BeautifulSoup
from .models.candidates import CandidatesURIs
from .models.electoral_parties import ElectoralParties


@dataclass(frozen=True)
class Response:
    year: int
    candidates: CandidatesURIs


class Client:
    BASE_URL = 'https://www.tse.jus.br/hotsites/pesquisas-eleitorais'
    CANDIDATES_URI = BASE_URL + '/candidatos.html'

    async def summary(self) -> tuple[ElectoralParties, list[Response]]:
        candidates = await self._get_candidates()
        electoral_parties = await self._get_electoral_parties()

        response = []
        years = sorted(candidates)
        for year in years:
            r = Response(
                year=year,
                candidates=candidates.get(year),
            )
            response.append(r)

        return electoral_parties, response

    async def _get_candidates(self) -> dict[int, CandidatesURIs]:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(Client.CANDIDATES_URI)

            links = {}
            for li in BeautifulSoup(r.content, 'html.parser').find(id='conteudo').find_all('li'):
                year_id = li['id']
                if not year_id.startswith('ano_'):
                    continue

                a = li.find('a')
                year = int(a.text)

                uris = CandidatesURIs(
                    candidates=f'https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_{year}.zip',
                    removal=f'https://cdn.tse.jus.br/estatistica/sead/odsele/motivo_cassacao/motivo_cassacao_{year}.zip',
                )

                links[year] = uris

        return links

    async def _get_electoral_parties(self) -> ElectoralParties:
        links = ElectoralParties(
            party_delegates='https://cdn.tse.jus.br/estatistica/sead/odsele/delegado_partidario/delegado_partidario.zip',
            party_bodies='https://cdn.tse.jus.br/estatistica/sead/odsele/orgao_partidario/orgao_partidario.zip',
        )
        return links
