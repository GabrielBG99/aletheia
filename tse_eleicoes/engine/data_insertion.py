import logging
from datetime import datetime
from pathlib import Path
import re
from typing import Any
from unidecode import unidecode
from file import ZipReader
# from ..models import Insert, Member, Party, Delegate, Candidate, Removal
# from ..models.release import Type


class Engine:
    # def __init__(self, task: Insert) -> None:
    #     priority_types = [Type.DELEGATE, Type.PARTY_MEMBER]
    #     if task.type not in priority_types:
    #         pending_tasks = task.release.insert_set.filter(
    #             type__in=priority_types,
    #             finished=False,
    #         )
    #         assert not pending_tasks.exists(), 'Priotity tasks not inserted'

    #     self._filepath = Path(task.file)
    #     self._release = task.release
    #     self._type = task.type

    def __init__(self) -> None:
        self._filepath = Path.home() / 'Downloads' / 'orgao_partidario.zip'

    def insert(self, batch_size: int = 5000) -> None:
        self._insert_member(batch_size)

    def _insert_member(self, batch_size: int) -> int:
        total = 0
        party_cache = {}

        test = set()
        with ZipReader(self._filepath, encoding='latin-1') as r:
            buffer = []
            for line in r:
                total += 1
                line = self._clean_fields(line)

                # party = party_cache.get(line['NR_PARTIDO'])
                # if not party:
                #     party = Party.objects.get_or_create(
                #         number=line['NR_PARTIDO'],
                #         defaults={
                #             'name': line['NM_PARTIDO'],
                #             'initials': line['SG_PARTIDO'],
                #         },
                #     )[0]
                #     party_cache[line['NR_PARTIDO']] = party

                member = dict(
                    # party=party,
                    generation_date=datetime.strptime(f"{line['DT_GERACAO']} {line['HH_GERACAO']}", '%d/%m/%Y %H:%M:%S'),
                    situation=unidecode(line['NM_SIT_ORGAO_PARTIDARIO']).upper(),
                    federative_unit=line['SG_UF'],
                    electoral_unit_initials=line['SG_UE'],
                    electoral_unit_name=line['NM_UE'],
                    county_code=line['CD_MUNICIPIO'],
                    county_name=line['NM_MUNICIPIO'],
                    address_description=line['DS_ENDERECO_ORGAO'],
                    zip_code=line['NR_CEP_ORGAO'],
                    phone_number=line['NR_FONE_FIXO_ORGAO'],
                    cellphone_number=line['NR_FONE_CEL_ORGAO'],
                    commercial_phone_number=line['NR_FONE_COMERCIAL_ORGAO'],
                    fax_number=line['NR_FAX_ORGAO'],
                    effective_date=(
                        datetime.strptime(line['DT_INICIO_VIGENCIA_ORGAO'], '%d/%m/%Y').date()
                        if line['DT_INICIO_VIGENCIA_ORGAO'] else None
                    ),
                    end_date=(
                        datetime.strptime(line['DT_FIM_VIGENCIA_ORGAO'], '%d/%m/%Y').date()
                        if line['DT_FIM_VIGENCIA_ORGAO'] else None
                    ),
                    covegare_type_code=line['CD_TIPO_ABRANGENCIA'],
                    covegare_type_description=line['DS_TIPO_ABRANGENCIA'],
                    type_code=line['CD_TIPO_ORGAO_PARTIDARIO'],
                    type_name=line['NM_TIPO_ORGAO_PARTIDARIO'],
                    electoral_system_number=line['SQ_ORGAO_PARTIDARIO'],
                    email=line['TX_EMAIL_ORGAO'].lower(),
                    position_number=line['SQ_CARGO_MEMBRO'],
                    position_description=line['DS_CARGO_MEMBRO'],
                    member_number=line['SQ_MEMBRO'],
                    member_name=unidecode(line['NM_MEMBRO']).upper(),
                    assignment_start_date=(
                        datetime.strptime(line['DT_INICIO_EXERCICIO_MEMBRO'], '%d/%m/%Y').date()
                        if line['DT_INICIO_EXERCICIO_MEMBRO'] else None
                    ),
                    assignment_end_date=(
                        datetime.strptime(line['DT_FIM_EXERCICIO_MEMBRO'], '%d/%m/%Y').date()
                        if line['DT_FIM_EXERCICIO_MEMBRO'] else None
                    ),
                    status=unidecode(line['ST_MEMBRO']).upper(),
                )
                test.add(''.join([
                    line['NR_PARTIDO'],
                    member['member_number'],
                    member['member_name'],
                ]))
                # buffer.append(member)

        #         if len(buffer) > batch_size:
        #             Member.objects.bulk_upsert(conflict_target=['party', 'member_number', 'member_name'], rows=buffer)
        #             buffer.clear()

        # if buffer:
        #     Member.objects.bulk_upsert(conflict_target=['party', 'member_number', 'member_name'], rows=buffer)
        #     buffer.clear()

        return total

    def _insert_delegate(self, batch_size: int) -> int:
        total = 0
        party_cache = {}

        with ZipReader(self._filepath, encoding='latin-1') as r:
            buffer = []
            for line in r:
                total += 1
                line = self._clean_fields(line)

                party = party_cache.get(line['NR_PARTIDO'])
                if not party:
                    party = Party.objects.get_or_create(
                        number=line['NR_PARTIDO'],
                        defaults={
                            'name': line['NM_PARTIDO'],
                            'initials': line['SG_PARTIDO'],
                        },
                    )[0]
                    party_cache[line['NR_PARTIDO']] = party

                delegate = dict(
                    party=party,
                    number=line['SQ_DELEGADO'],
                    name=unidecode(line['NM_DELEGADO']).upper(),
                    accreditation_date=(
                        datetime.strptime(line['DT_CREDENCIAMENTO'], '%d/%m/%Y').date()
                        if line['DT_CREDENCIAMENTO'] else None
                    ),
                    deaccreditation_date=(
                        datetime.strptime(line['DT_DESCREDENCIAMENTO'], '%d/%m/%Y').date()
                        if line['DT_DESCREDENCIAMENTO'] else None
                    ),
                    generation_date=datetime.strptime(f"{line['DT_GERACAO']} {line['HH_GERACAO']}", '%d/%m/%Y %H:%M:%S'),
                    coverage_type_code=line['CD_TIPO_ABRANGENCIA'],
                    coverage_type_description=line['DS_TIPO_ABRANGENCIA'],
                    federative_unit=line['SG_UF'],
                    electoral_unit=line['SG_UE'],
                    electoral_unit_name=line['NM_UE'],
                )
                buffer.append(delegate)

                if len(buffer) > batch_size:
                    Delegate.objects.bulk_upsert(
                        conflict_target=['number', 'name', 'accreditation_date', 'party', 'federative_unit', 'electoral_unit'],
                        rows=buffer,
                    )
                    buffer.clear()

        if buffer:
            Delegate.objects.bulk_upsert(
                conflict_target=['number', 'name', 'accreditation_date', 'party', 'federative_unit', 'electoral_unit'],
                rows=buffer,
            )
            buffer.clear()

        return total

    def _insert_candidates(self, batch_size: int) -> int:
        total = 0
        party_cache = {}

        with ZipReader(self._filepath, encoding='latin-1') as r:
            buffer = []
            for line in r:
                total += 1
                line = self._clean_fields(line)

                party = party_cache.get(line['NR_PARTIDO'])
                if not party:
                    party = Party.objects.get_or_create(
                        number=line['NR_PARTIDO'],
                        defaults={
                            'name': line['NM_PARTIDO'],
                            'initials': line['SG_PARTIDO'],
                        },
                    )[0]
                    party_cache[line['NR_PARTIDO']] = party

                candidate = dict(
                    party=party,
                    member=Member.objects.get(
                        party=party,
                        member_number=line['SQ_CANDIDATO'],
                        member_name=unidecode(line['NM_CANDIDATO']).upper(),
                    ),
                    generation_date=datetime.strptime(f"{line['DT_GERACAO']} {line['HH_GERACAO']}", '%d/%m/%Y %H:%M:%S'),
                    year=int(line['ANO_ELEICAO']),
                    election_type_code=line['CD_TIPO_ELEICAO'],
                    election_type_name=line['NM_TIPO_ELEICAO'],
                    electoral_round_number=line['NR_TURNO'],
                    election_code=line['CD_ELEICAO'],
                    election_description=line['DS_ELEICAO'],
                    election_date=(
                        datetime.strptime(line['DT_ELEICAO'], '%d/%m/%Y').date()
                        if line['DT_ELEICAO'] else None
                    ),
                    coverage=line['TP_ABRANGENCIA'],
                    federative_unit=line['SG_UF'],
                    election_unit_initials=line['SG_UE'],
                    election_unit_name=line['NM_UE'],
                    position_code=line['CD_CARGO'],
                    position=line['DS_CARGO'],
                    tse_number=line['SQ_CANDIDATO'],
                    number=line['NR_CANDIDATO'],
                    name=unidecode(line['NM_CANDIDATO']).upper(),
                    urna_name=line['NM_URNA_CANDIDATO'],
                    social_name=unidecode(line['NM_SOCIAL_CANDIDATO']).upper(),
                    cpf=re.sub(r'\D', '', line['NR_CPF_CANDIDATO']),
                    email=line['NM_EMAIL'].lower(),
                    candidature_status_code=line['CD_SITUACAO_CANDIDATURA'],
                    candidature_status=line['DS_SITUACAO_CANDIDATURA'],
                    candidature_detail_status_code=line['CD_DETALHE_SITUACAO_CAND'],
                    candidature_detail_status=line['DS_DETALHE_SITUACAO_CAND'],
                    association_type=line['TP_AGREMIACAO'],
                    coalition_number=line['SQ_COLIGACAO'],
                    coalition_name=line['NM_COLIGACAO'],
                    coalition_composition=line['DS_COMPOSICAO_COLIGACAO'],
                    nationality_code=line['CD_NACIONALIDADE'],
                    nationality=line['DS_NACIONALIDADE'],
                    birth_federative_unit=line['SG_UF_NASCIMENTO'],
                    birth_county_code=line['CD_MUNICIPIO_NASCIMENTO'],
                    birth_county=line['NM_MUNICIPIO_NASCIMENTO'],
                    birthdate=(
                        datetime.strptime(line['DT_NASCIMENTO'], '%d/%m/%Y').date()
                        if line['DT_NASCIMENTO'] else None
                    ),
                    age_at_possession=int(line['NR_IDADE_DATA_POSSE'] or 0),
                    voter_registration=line['NR_TITULO_ELEITORAL_CANDIDATO'],
                    gender_code=line['CD_GENERO'],
                    gender=line['DS_GENERO'],
                    education_level_code=line['CD_GRAU_INSTRUCAO'],
                    education_level=line['DS_GRAU_INSTRUCAO'],
                    marital_status_code=line['CD_ESTADO_CIVIL'],
                    marital_status=line['DS_ESTADO_CIVIL'],
                    color_code=line['CD_COR_RACA'],
                    color=line['DS_COR_RACA'],
                    ocupation_code=line['CD_OCUPACAO'],
                    ocupation=line['DS_OCUPACAO'],
                    expense=round(float(line['VR_DESPESA_MAX_CAMPANHA'] or 0) * 100),
                    totalization_situation_code=line['CD_SIT_TOT_TURNO'],
                    totalization_situation=line['DS_SIT_TOT_TURNO'],
                    reelection=line['ST_REELEICAO'],
                    assets_declaration_status=line['ST_DECLARAR_BENS'],
                    application_protocol=line['NR_PROTOCOLO_CANDIDATURA'],
                    process_number=line['NR_PROCESSO'],
                    election_day_application_status_code=line['CD_SITUACAO_CANDIDATO_PLEITO'],
                    election_day_application_status=line['DS_SITUACAO_CANDIDATO_PLEITO'],
                    urna_status_code=line['CD_SITUACAO_CANDIDATO_URNA'],
                    urna_status=line['DS_SITUACAO_CANDIDATO_URNA'],
                    inserted_urna=line['ST_CANDIDATO_INSERIDO_URNA'].upper() == 'SIM',
                )
                buffer.append(candidate)

                if len(buffer) > batch_size:
                    Candidate.objects.bulk_upsert(
                        conflict_target=['year', 'election_type_code', 'election_code', 'federative_unit', 'election_unit_initials', 'tse_number'],
                        rows=buffer,
                    )
                    buffer.clear()

        if buffer:
            Candidate.objects.bulk_upsert(
                conflict_target=['year', 'election_type_code', 'election_code', 'federative_unit', 'election_unit_initials', 'tse_number'],
                rows=buffer,
            )
            buffer.clear()
        
        return total

    def _insert_removals(self, batch_size: int) -> int:
        total = 0
        party_cache = {}

        with ZipReader(self._filepath, encoding='latin-1') as r:
            buffer = []
            for line in r:
                total += 1
                line = self._clean_fields(line)

                party = party_cache.get(line['NR_PARTIDO'])
                if not party:
                    party = Party.objects.get_or_create(
                        number=line['NR_PARTIDO'],
                        defaults={
                            'name': line['NM_PARTIDO'],
                            'initials': line['SG_PARTIDO'],
                        },
                    )[0]
                    party_cache[line['NR_PARTIDO']] = party

                removal = dict(
                    party=party,
                    candidate=Candidate.objects.get(
                        year=int(line['ANO_ELEICAO']),
                        election_type_code=line['CD_TIPO_ELEICAO'],
                        election_code=line['CD_ELEICAO'],
                        federative_unit=line['SG_UF'],
                        election_unit_initials=line['SG_UE'],
                        tse_number=line['SQ_CANDIDATO'],
                    ),
                    generation_date=datetime.strptime(f"{line['DT_GERACAO']} {line['HH_GERACAO']}", '%d/%m/%Y %H:%M:%S'),
                    year=int(line['ANO_ELEICAO']),
                    election_type_code=line['CD_TIPO_ELEICAO'],
                    election_type=line['NM_TIPO_ELEICAO'],
                    election_code=line['CD_ELEICAO'],
                    election=line['DS_ELEICAO'],
                    federative_unit=line['SG_UF'],
                    election_unit_initials=line['SG_UE'],
                    election_unit=line['NM_UE'],
                    tse_number=line['SQ_CANDIDATO'],
                    removal_description=line['DS_MOTIVO_CASSACAO'],
                )
                buffer.append(removal)

                if len(buffer) > batch_size:
                    Removal.objects.bulk_upsert(
                        conflict_target=['year', 'election_type_code', 'election_code', 'federative_unit', 'election_unit_initials', 'tse_number'],
                        rows=buffer,
                    )
                    buffer.clear()

        if buffer:
            Removal.objects.bulk_upsert(
                conflict_target=['year', 'election_type_code', 'election_code', 'federative_unit', 'election_unit_initials', 'tse_number'],
                rows=buffer,
            )
            buffer.clear()

        return total

    def _clean_fields(self, data: dict[str, Any]) -> dict[str, Any]:
        invalid_values = ['#NULO#']
        new = dict()
        for k, v in data.items():
            if isinstance(v, str) and v in invalid_values:
                v = ''

            new[k] = v

        return new


if __name__ == '__main__':
    Engine().insert()
