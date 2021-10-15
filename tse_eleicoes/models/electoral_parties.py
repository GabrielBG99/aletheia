import uuid
from django.db import models
from psqlextra.models import PostgresModel


class Party(PostgresModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    initials = models.TextField(help_text='Sigla do Partido Político')  # SG_PARTIDO
    number = models.TextField(help_text='Número do Partido Político', unique=True)  # NR_PARTIDO
    name = models.TextField(help_text='Nome do Partido Político')  # NM_PARTIDO

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['initials']),
            models.Index(fields=['name']),
        ]


class Delegate(PostgresModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    party = models.ForeignKey(Party, on_delete=models.CASCADE, help_text='Partido')
    number = models.TextField(help_text='Número sequencial do delegado do partido político gerado internamente pelos sistemas eleitorais')  # SQ_DELEGADO
    name = models.TextField(help_text='Nome do delegado do partido político')  # NM_DELEGADO
    accreditation_date = models.DateField(help_text='Data de credenciamento como delegado')  # DT_CREDENCIAMENTO
    deaccreditation_date = models.DateField(null=True, help_text='Data de descredenciamento como delegado')  # DT_DESCREDENCIAMENTO
    generation_date = models.DateTimeField(null=True, help_text='Data e hora de geração do arquivo')  # DT_GERACAO & HH_GERACAO
    coverage_type_code = models.TextField(help_text='Código do tipo da abrangência do partido político que o delegado faz parte')  # CD_TIPO_ABRANGENCIA
    coverage_type_description = models.TextField(help_text='Descrição da abrangência do partido político que o delegado faz parte')  # DS_TIPO_ABRANGENCIA
    federative_unit = models.TextField(help_text='Sigla da Unidade da Federação ao qual partido político que o delegado faz parte')  # SG_UF
    electoral_unit = models.TextField(help_text='Sigla da Unidade Eleitoral')  # SG_UE
    electoral_unit_name = models.TextField(help_text='Nome da Unidade Eleitoral')  # NM_UE

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['number']),
            models.Index(fields=['name']),
            models.Index(fields=['accreditation_date']),
            models.Index(fields=['deaccreditation_date']),
            models.Index(fields=['coverage_type_code']),
            models.Index(fields=['federative_unit']),
            models.Index(fields=['electoral_unit']),
        ]
        constraints = [
            models.UniqueConstraint(
                name='unique_tse_eleicoes_delegate',
                fields=[
                    'number',
                    'name',
                    'accreditation_date',
                    'party',
                    'federative_unit',
                    'electoral_unit',
                ],
            )
        ]


class Member(PostgresModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    party = models.ForeignKey(Party, on_delete=models.CASCADE, help_text='Partido')
    generation_date = models.DateTimeField(help_text='Data e hora de geração do arquivo')  # DT_GERACAO & HH_GERACAO
    situation = models.TextField(help_text='Nome da situação do Órgão Partidário')  # NM_SIT_ORGAO_PARTIDARIO
    federative_unit = models.TextField(help_text='Sigla da Unidade da Federação do Órgão Político')  # SG_UF
    electoral_unit_initials = models.TextField(help_text='Sigla da Unidade Eleitoral')  # SG_UE
    electoral_unit_name = models.TextField(help_text='Nome da Unidade Eleitoral')  # NM_UE
    county_code = models.TextField(help_text='Código do município')  # CD_MUNICIPIO
    county_name = models.TextField(help_text='Nome do município')  # NM_MUNICIPIO
    address_description = models.TextField(help_text='Descrição do endereço do órgão partidário')  # DS_ENDERECO_ORGAO
    zip_code = models.TextField(help_text='CEP do endereço do Órgão Partidário')  # NR_CEP_ORGAO
    phone_number = models.TextField(help_text='Número do telefone fixo do Órgão Partidário')  # NR_FONE_FIXO_ORGAO
    cellphone_number = models.TextField(help_text='Número do telefone celular do Órgão Partidário')  # NR_FONE_CEL_ORGAO
    commercial_phone_number = models.TextField(help_text='Número do telefone comercial do Órgão Partidário')  # NR_FONE_COMERCIAL_ORGAO
    fax_number = models.TextField(help_text='Número do fax do Órgão Partidário')  # NR_FAX_ORGAO
    effective_date = models.DateField(null=True, help_text='Data de início de vigência do Órgão Político')  # DT_INICIO_VIGENCIA_ORGAO
    end_date = models.DateField(null=True, help_text='Data fim de vigência do Órgão Político')  # DT_FIM_VIGENCIA_ORGAO
    covegare_type_code = models.TextField(help_text='Código do tipo da abrangência do órgão político')  # CD_TIPO_ABRANGENCIA
    covegare_type_description = models.TextField(help_text='Descrição da abrangência do partido político que o delegado faz parte')  # DS_TIPO_ABRANGENCIA
    type_code = models.TextField(help_text='Código do tipo de órgão partidário')  # CD_TIPO_ORGAO_PARTIDARIO
    type_name = models.TextField(help_text='Nome do Tipo de Órgão Partidário')  # NM_TIPO_ORGAO_PARTIDARIO
    electoral_system_number = models.TextField(help_text='Número sequencial do órgão partidário gerado internamente pelos sistemas eleitorais')  # SQ_ORGAO_PARTIDARIO
    email = models.TextField(help_text='Descrição do e-mail do Órgão Partidário')  # TX_EMAIL_ORGAO
    position_number = models.TextField(help_text='Número sequencial do cargo do membro do órgão partidário')  # SQ_CARGO_MEMBRO
    position_description = models.TextField(help_text='Descrição do cargo do membro do Órgão Partidário')  # DS_CARGO_MEMBRO
    member_number = models.TextField(help_text='Número sequencial do membro gerado internamente pelos sistemas eleitorais')  # SQ_MEMBRO
    member_name = models.TextField(help_text='Nome do membro do Órgão Partidário')  # NM_MEMBRO
    assignment_start_date = models.DateField(null=True, help_text='Data de início de exercício do membro')  # DT_INICIO_EXERCICIO_MEMBRO
    assignment_end_date = models.DateField(null=True, help_text='Data fim do exercício do membro')  # DT_FIM_EXERCICIO_MEMBRO
    status = models.TextField(help_text='Status do Membro')  # ST_MEMBRO

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['email']),
            models.Index(fields=['member_name']),
            models.Index(fields=['status']),
        ]
        constraints = [
            models.UniqueConstraint(
                name='unique_tse_eleicoes_member',
                fields=[
                    'party',
                    'member_number',
                    'member_name',
                ]
            ),
        ]
