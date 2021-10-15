import uuid
from django.db import models
from psqlextra.models import PostgresModel
from .electoral_parties import Member, Party


class Candidate(PostgresModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    party = models.ForeignKey(Party, on_delete=models.CASCADE, help_text='Partido de origem do candidato')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, help_text='Dados do membro no partido')
    generation_date = models.TextField(help_text='Data e hora da extração dos dados para geração do arquivo')  # DT_GERACAO & HH_GERACAO
    year = models.IntegerField(help_text='Ano de referência da eleição para geração do arquivo')  # ANO_ELEICAO
    election_type_code = models.TextField(help_text='Código do tipo de eleição')  # CD_TIPO_ELEICAO
    election_type_name = models.TextField(help_text='Nome do tipo de eleição')  # NM_TIPO_ELEICAO
    electoral_round_number = models.TextField(help_text='Número do turno da eleição')  # NR_TURNO
    election_code = models.TextField(help_text='Código único da eleição no âmbito da Justiça Eleitoral')  # CD_ELEICAO
    election_description = models.TextField(help_text='Descrição da eleição')  # DS_ELEICAO
    election_date = models.TextField(help_text='Data em que ocorreu a eleição')  # DT_ELEICAO
    coverage = models.TextField(help_text='Abrangência da eleição')  # TP_ABRANGENCIA
    federative_unit = models.TextField(help_text='Sigla da Unidade da Federação em que ocorreu a eleição')  # SG_UF
    election_unit_initials = models.TextField(help_text='Sigla da Unidade Eleitoral em que o candidato concorre na eleição')  # SG_UE
    election_unit_name = models.TextField(help_text='Nome da Unidade Eleitoral do candidato')  # NM_UE
    position_code = models.TextField(help_text='Código do cargo ao qual o candidato concorre na eleição')  # CD_CARGO
    position = models.TextField(help_text='Cargo ao qual o candidato concorre na eleição')  # DS_CARGO
    tse_number = models.TextField(help_text='Número sequencial do candidato')  # SQ_CANDIDATO
    number = models.TextField(help_text='Número do candidato na urna')  # NR_CANDIDATO
    name = models.TextField(help_text='Nome completo do candidato')  # NM_CANDIDATO
    urna_name = models.TextField(help_text='Nome do candidato que aparece na urna')  # NM_URNA_CANDIDATO
    social_name = models.TextField(help_text='Nome social do candidato')  # NM_SOCIAL_CANDIDATO
    cpf = models.TextField(help_text='Número do CPF do candidato')  # NR_CPF_CANDIDATO
    email = models.TextField(help_text='Endereço de e-mail do candidato')  # NM_EMAIL
    candidature_status_code = models.TextField(help_text='Código da situação do registro de candidatura do candidato')  # CD_SITUACAO_CANDIDATURA
    candidature_status = models.TextField(help_text='Situação do registro da candidatura do candidato')  # DS_SITUACAO_CANDIDATURA
    candidature_detail_status_code = models.TextField(help_text='Código do detalhe da situação do registro de candidatura do candidato')  # CD_DETALHE_SITUACAO_CAND
    candidature_detail_status = models.TextField(help_text='Detalhe da situação do registro de candidatura do candidato')  # DS_DETALHE_SITUACAO_CAND
    association_type = models.TextField(help_text='Tipo de agremiação da candidatura do candidato')  # TP_AGREMIACAO
    coalition_number = models.TextField(help_text='Sequencial da coligação da qual o candidato pertence, gerado pela Justiça Eleitoral')  # SQ_COLIGACAO
    coalition_name = models.TextField(help_text='Nome da coligação da qual o candidato pertence')  # NM_COLIGACAO
    coalition_composition = models.TextField(help_text='Composição da coligação da qual o candidato pertence')  # DS_COMPOSICAO_COLIGACAO
    nationality_code = models.TextField(help_text='Código da nacionalidade do candidato')  # CD_NACIONALIDADE
    nationality = models.TextField(help_text='Nacionalidade do candidato')  # DS_NACIONALIDADE
    birth_federative_unit = models.TextField(help_text='Sigla da Unidade da Federação de nascimento do candidato')  # SG_UF_NASCIMENTO
    birth_county_code = models.TextField(help_text='Código de identificação do município de nascimento do candidato')  # CD_MUNICIPIO_NASCIMENTO
    birth_county = models.TextField(help_text='Nome do município de nascimento do candidato')  # NM_MUNICIPIO_NASCIMENTO
    birthdate = models.TextField(help_text='Data de nascimento do candidato')  # DT_NASCIMENTO
    age_at_possession = models.IntegerField(help_text='Idade do candidato na data da posse')  # NR_IDADE_DATA_POSSE
    voter_registration = models.TextField(help_text='Número do título eleitoral do candidato')  # NR_TITULO_ELEITORAL_CANDIDATO
    gender_code = models.TextField(help_text='Código do gênero do candidato')  # CD_GENERO
    gender = models.TextField(help_text='Gênero do candidato')  # DS_GENERO
    education_level_code = models.TextField(help_text='Código do grau de instrução do candidato')  # CD_GRAU_INSTRUCAO
    education_level = models.TextField(help_text='Grau de instrução do candidato')  # DS_GRAU_INSTRUCAO
    marital_status_code = models.TextField(help_text='Código do estado civil do candidato')  # CD_ESTADO_CIVIL
    marital_status = models.TextField(help_text='Estado civil do candidato')  # DS_ESTADO_CIVIL
    color_code = models.TextField(help_text='Código da cor/raça do candidato')  # CD_COR_RACA
    color = models.TextField(help_text='Cor/raça do candidato')  # DS_COR_RACA
    ocupation_code = models.TextField(help_text='Código da ocupação do candidato')  # CD_OCUPACAO
    ocupation = models.TextField(help_text='Ocupação do candidato')  # DS_OCUPACAO
    expense = models.BigIntegerField(help_text='Valor máximo, em reais, de despesas de campanha declarada pelo partido para aquele candidato')  # VR_DESPESA_MAX_CAMPANHA
    totalization_situation_code = models.TextField(help_text='Código da situação de totalização do candidato, naquele turno da eleição, após a totalização dos votos')  # CD_SIT_TOT_TURNO
    totalization_situation = models.TextField(help_text='Situação de totalização do candidato, naquele turno da eleição, após a totalização dos votos')  # DS_SIT_TOT_TURNO
    reelection = models.TextField(help_text='Indica se o candidato está concorrendo ou não à reeleição')  # ST_REELEICAO
    assets_declaration_status = models.TextField(help_text='Indica se o candidato tem ou não bens a declarar')  # ST_DECLARAR_BENS
    application_protocol = models.TextField(help_text='Número do protocolo de registro de candidatura do candidato')  # NR_PROTOCOLO_CANDIDATURA
    process_number = models.TextField(help_text='Número do processo de registro de candidatura do candidato')  # NR_PROCESSO
    election_day_application_status_code = models.TextField(help_text='Código da situação da candidatura no dia do Pleito')  # CD_SITUACAO_CANDIDATO_PLEITO
    election_day_application_status = models.TextField(help_text='Situação da candidatura no dia do Pleito')  # DS_SITUACAO_CANDIDATO_PLEITO
    urna_status_code = models.TextField(help_text='Código da situação da candidatura na urna')  # CD_SITUACAO_CANDIDATO_URNA
    urna_status = models.TextField(help_text='Situação da candidatura na urna.')  # DS_SITUACAO_CANDIDATO_URNA
    inserted_urna = models.BooleanField(null=True, help_text='Informa se o candidato foi inserido na urna eletrônica')  # ST_CANDIDATO_INSERIDO_URNA

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['year']),
            models.Index(fields=['number']),
            models.Index(fields=['name']),
            models.Index(fields=['urna_name']),
            models.Index(fields=['social_name']),
            models.Index(fields=['cpf']),
            models.Index(fields=['email']),
        ]
        constraints = [
            models.UniqueConstraint(
                name='unique_tse_eleicoes_candidate',
                fields=[
                    'year',
                    'election_type_code',
                    'election_code',
                    'federative_unit',
                    'election_unit_initials',
                    'tse_number',
                ],
            ),
        ]


class Removal(PostgresModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, help_text='Candidato')
    generation_date = models.TextField(help_text='Data e hora da extração dos dados para geração do arquivo')  # DT_GERACAO & HH_GERACAO
    year = models.TextField(help_text='Ano da eleição')  # ANO_ELEICAO
    election_type_code = models.TextField(help_text='Código do tipo de eleição')  # CD_TIPO_ELEICAO
    election_type = models.TextField(help_text='Tipo de eleição')  # NM_TIPO_ELEICAO
    election_code = models.TextField(help_text='Código da eleição')  # CD_ELEICAO
    election = models.TextField(help_text='Descrição da eleição')  # DS_ELEICAO
    federative_unit = models.TextField(help_text='Sigla da Unidade Federativa onde ocorreu a eleição')  # SG_UF
    election_unit_initials = models.TextField(help_text='Sigla da Unidade Eleitoral do candidato')  # SG_UE
    election_unit = models.TextField(help_text='Nome da Unidade Eleitoral do candidato')  # NM_UE
    tse_number = models.TextField(help_text='Número sequencial do candidato gerado internamente pelos sistemas eleitorais')  # SQ_CANDIDATO
    removal_description = models.TextField(help_text='Descrição do motivo da cassação')  # DS_MOTIVO_CASSACAO

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['year']),
            models.Index(fields=['election_type_code']),
            models.Index(fields=['election_code']),
            models.Index(fields=['federative_unit']),
            models.Index(fields=['election_unit_initials']),
            models.Index(fields=['tse_number']),
        ]
        constraints = [
            models.UniqueConstraint(
                name='unique_tse_eleicoes_removal',
                fields=[
                    'year',
                    'election_type_code',
                    'election_code',
                    'federative_unit',
                    'election_unit_initials',
                    'tse_number',
                ],
            ),
        ]
