# Generated by Django 3.2.5 on 2021-07-21 18:01

from django.db import migrations, models
import django.db.models.deletion
import psqlextra.manager.manager
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InsertionTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('finished', models.BooleanField(default=False)),
                ('type', models.IntegerField(choices=[(1, 'Trip'), (2, 'Trip Part'), (3, 'Ticket'), (4, 'Payment')])),
                ('start', models.PositiveBigIntegerField()),
                ('end', models.PositiveBigIntegerField()),
                ('filepath', models.TextField()),
            ],
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('proposal_number', models.TextField(help_text='Número da Proposta (PCDP)')),
                ('higher_agency_code', models.TextField(help_text='Código do Órgão Superior que custeou a despesa')),
                ('higher_agency', models.TextField(help_text='Nome do Órgão Superior')),
                ('paying_agency_code', models.TextField(help_text='Código do Órgão que pagou a despesa')),
                ('paying_agency', models.TextField(help_text='Nome do Órgão Pagador')),
                ('management_unit_code', models.TextField(help_text='Código da Unidade Gestora que pagou a despesa')),
                ('management_unit', models.TextField(help_text='Nome da Unidade Gestora')),
                ('type', models.TextField(help_text='Tipo da despesa paga pelo órgão')),
                ('value', models.BigIntegerField(help_text='Valor da despesa paga')),
            ],
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('year', models.PositiveIntegerField(unique=True)),
                ('finished', models.BooleanField(default=False)),
                ('folder', models.TextField()),
                ('uri', models.TextField()),
            ],
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('proposal_number', models.TextField(help_text='Número da Proposta (PCDP)')),
                ('vehicle', models.TextField(help_text='Meio de transporte da passagem')),
                ('outbound_country_origin', models.TextField(help_text='País de origem na ida')),
                ('outbound_uf_origin', models.TextField(help_text='UF de origem na ida')),
                ('outbound_city_origin', models.TextField(help_text='Cidade de origem na ida')),
                ('outbound_country_destiny', models.TextField(help_text='País de destino na ida')),
                ('outbound_uf_destiny', models.TextField(help_text='UF de destino na ida')),
                ('outbound_city_destiny', models.TextField(help_text='Cidade de destino na ida')),
                ('return_country_origin', models.TextField(help_text='País de origem na volta')),
                ('return_uf_origin', models.TextField(help_text='UF de origem na volta')),
                ('return_city_origin', models.TextField(help_text='Cidade de origem na volta')),
                ('return_country_destiny', models.TextField(help_text='País de destino na volta')),
                ('return_uf_destiny', models.TextField(help_text='UF de destino na volta')),
                ('return_city_destiny', models.TextField(help_text='Cidade de destino na volta')),
                ('value', models.BigIntegerField(help_text='Valor da passagem')),
                ('service_charge', models.BigIntegerField(help_text='Taxa de serviço da passagem')),
                ('buy_date', models.DateTimeField(help_text='Data de compra da passagem', null=True)),
            ],
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('trip_id', models.TextField(help_text='Número que identifica o processo de concessão da viagem', unique=True)),
                ('proposal_number', models.TextField(help_text='Número da Proposta (PCDP)')),
                ('situation', models.TextField(help_text='Situação da viagem')),
                ('urgent', models.BooleanField(help_text='É urgente?')),
                ('urgency_justification', models.TextField(help_text='Justificativa da urgência')),
                ('higher_agency_code', models.TextField(help_text='Código do Órgão Superior que custeou despesas da viagem')),
                ('higher_agency', models.TextField(help_text='Nome do Órgão Superior')),
                ('requesting_agency_code', models.TextField(help_text='Código do Órgão que solicitou a viagem')),
                ('requesting_agency', models.TextField(help_text='Nome do Órgão')),
                ('traveler_cpf', models.TextField(help_text='CPF da pessoa que realizou a viagem')),
                ('traveler_name', models.TextField(help_text='Nome do viajante')),
                ('traveler_position', models.TextField(help_text='Cargo do viajante')),
                ('traveler_occupation', models.TextField(help_text='Função do viajante')),
                ('traveler_occupation_description', models.TextField(help_text='Descrição da função do viajante')),
                ('start_date', models.DateField(help_text='Data de início de afastamento do servidor')),
                ('end_date', models.DateField(help_text='Data de fim de afastamento do servidor')),
                ('destinations', models.TextField(help_text='Locais pelos quais o viajante passará durante a viagem')),
                ('reason', models.TextField(help_text='Motivo da viagem')),
                ('dailys_value', models.BigIntegerField(help_text='Valor de diárias pagas pelo órgão')),
                ('tickets_value', models.BigIntegerField(help_text='Valor de passagens pagas pelo órgão')),
                ('other_value', models.BigIntegerField(help_text='Valor de outros gastos pagos pelo órgão')),
            ],
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.CreateModel(
            name='TripPart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('proposal_number', models.TextField()),
                ('order', models.BigIntegerField(help_text='Sequência do trecho na viagem')),
                ('origin_date', models.DateField(help_text='Data de saída da origem')),
                ('country_origin', models.TextField(help_text='País de origem')),
                ('uf_origin', models.TextField(help_text='UF de origem')),
                ('city_origin', models.TextField(help_text='Cidade de origem')),
                ('destiny_date', models.DateField(help_text='Data de chegada no destino')),
                ('country_destiny', models.TextField(help_text='País de destino')),
                ('uf_destiny', models.TextField(help_text='UF de destino')),
                ('city_destiny', models.TextField(help_text='Cidade de destino')),
                ('vehicle', models.TextField(help_text='Meio de transporte da origem para o destino')),
                ('daily_value', models.BigIntegerField(help_text='Número de diárias do trecho')),
                ('mission', models.BooleanField(help_text='Houve missão no trecho?')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cgu_viagens.trip')),
            ],
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['created_at'], name='cgu_viagens_created_02547c_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['updated_at'], name='cgu_viagens_updated_66dd9d_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['proposal_number'], name='cgu_viagens_proposa_31f2ca_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['urgent'], name='cgu_viagens_urgent_975e92_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['higher_agency_code'], name='cgu_viagens_higher__9187ba_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['requesting_agency_code'], name='cgu_viagens_request_36a0fb_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['traveler_cpf'], name='cgu_viagens_travele_a8eb24_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['traveler_name'], name='cgu_viagens_travele_15f697_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['start_date'], name='cgu_viagens_start_d_5d59c4_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['end_date'], name='cgu_viagens_end_dat_712eb6_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['reason'], name='cgu_viagens_reason_55c9b9_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['dailys_value'], name='cgu_viagens_dailys__aafbb3_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['tickets_value'], name='cgu_viagens_tickets_67d52d_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['other_value'], name='cgu_viagens_other_v_423807_idx'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cgu_viagens.trip'),
        ),
        migrations.AddIndex(
            model_name='release',
            index=models.Index(fields=['created_at'], name='cgu_viagens_created_701302_idx'),
        ),
        migrations.AddIndex(
            model_name='release',
            index=models.Index(fields=['updated_at'], name='cgu_viagens_updated_060231_idx'),
        ),
        migrations.AddIndex(
            model_name='release',
            index=models.Index(fields=['finished'], name='cgu_viagens_finishe_3b5e78_idx'),
        ),
        migrations.AddField(
            model_name='payment',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cgu_viagens.trip'),
        ),
        migrations.AddField(
            model_name='insertiontask',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cgu_viagens.release'),
        ),
        migrations.AddIndex(
            model_name='trippart',
            index=models.Index(fields=['created_at'], name='cgu_viagens_created_078140_idx'),
        ),
        migrations.AddIndex(
            model_name='trippart',
            index=models.Index(fields=['updated_at'], name='cgu_viagens_updated_a38d3f_idx'),
        ),
        migrations.AddConstraint(
            model_name='trippart',
            constraint=models.UniqueConstraint(fields=('trip', 'proposal_number', 'order', 'origin_date', 'country_origin', 'uf_origin', 'city_origin', 'destiny_date', 'country_destiny', 'uf_destiny', 'city_destiny', 'vehicle', 'daily_value', 'mission'), name='unique_cgu_viagens_trip_part'),
        ),
        migrations.AddIndex(
            model_name='ticket',
            index=models.Index(fields=['created_at'], name='cgu_viagens_created_30acff_idx'),
        ),
        migrations.AddIndex(
            model_name='ticket',
            index=models.Index(fields=['updated_at'], name='cgu_viagens_updated_641c0c_idx'),
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('trip', 'proposal_number', 'vehicle', 'outbound_country_origin', 'outbound_uf_origin', 'outbound_city_origin', 'outbound_country_destiny', 'outbound_uf_destiny', 'outbound_city_destiny', 'return_country_origin', 'return_uf_origin', 'return_city_origin', 'return_country_destiny', 'return_uf_destiny', 'return_city_destiny', 'value', 'service_charge', 'buy_date'), name='unique_cgu_viagens_ticket'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['created_at'], name='cgu_viagens_created_ef0b16_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['updated_at'], name='cgu_viagens_updated_5d465c_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['type'], name='cgu_viagens_type_6fb232_idx'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['value'], name='cgu_viagens_value_cd28b0_idx'),
        ),
        migrations.AddConstraint(
            model_name='payment',
            constraint=models.UniqueConstraint(fields=('trip', 'proposal_number', 'higher_agency_code', 'paying_agency_code', 'management_unit_code', 'type', 'value'), name='unique_cgu_viagens_payment'),
        ),
        migrations.AddIndex(
            model_name='insertiontask',
            index=models.Index(fields=['created_at'], name='cgu_viagens_created_f083d0_idx'),
        ),
        migrations.AddIndex(
            model_name='insertiontask',
            index=models.Index(fields=['updated_at'], name='cgu_viagens_updated_679032_idx'),
        ),
        migrations.AddIndex(
            model_name='insertiontask',
            index=models.Index(fields=['finished'], name='cgu_viagens_finishe_ebebb0_idx'),
        ),
    ]
