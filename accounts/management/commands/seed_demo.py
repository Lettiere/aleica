import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import PerfilUsuario
from clientes.models import Cliente
from empresas.models import Empresa
from inteligencia.models import SnapshotInteligencia
from inteligencia.services import (
    calcular_dias_sem_retorno,
    calcular_probabilidade_perda,
    calcular_risco,
    calcular_score_aleica,
    calcular_valor_potencial,
    gerar_motivo_alerta,
    gerar_oportunidades,
)
from oportunidades.models import Oportunidade
from relacionamento.models import HistoricoContato


class Command(BaseCommand):
    help = "Cria usuarios e dados ficticios para demonstracao da Aleica Gestao."

    def handle(self, *args, **options):
        self.criar_usuarios()
        self.criar_dados()
        self.stdout.write(self.style.SUCCESS("Seed demo concluido."))

    def criar_usuarios(self):
        users = [
            ("aleixa.master", "Aleica", "Master", "aleixa@master.com.br", "eunaosei", PerfilUsuario.Perfil.MASTER),
            ("carina.fernandes", "Carina", "Fernandes", "carina@master.com.br", "aleica2026", PerfilUsuario.Perfil.GESTORA_RELACIONAMENTO),
        ]
        for username, first_name, last_name, email, password, perfil in users:
            user, created = User.objects.get_or_create(username=username, defaults={"email": email, "first_name": first_name, "last_name": last_name, "is_staff": True, "is_superuser": perfil == PerfilUsuario.Perfil.MASTER})
            if created:
                user.set_password(password)
                user.save()
            PerfilUsuario.objects.update_or_create(usuario=user, defaults={"perfil": perfil})

    def criar_dados(self):
        segmentos = [
            "Clinica Odontologica",
            "Clinica de Estetica",
            "Escritorio de Advocacia",
            "Imobiliaria",
            "Salao de Beleza",
            "Contabilidade",
        ]
        empresas = []
        for i, segmento in enumerate(segmentos, start=1):
            empresa, _ = Empresa.objects.get_or_create(
                nome_fantasia=f"{segmento} Aleica {i}",
                defaults={
                    "razao_social": f"{segmento} Aleica {i} LTDA",
                    "cnpj": f"00.000.00{i}/0001-0{i}",
                    "segmento": segmento,
                    "telefone": f"(11) 400{i}-20{i}0",
                    "email": f"contato{i}@empresa.com.br",
                    "cidade": "Sao Paulo",
                    "estado": "SP",
                    "status": Empresa.Status.ATIVA,
                },
            )
            empresas.append(empresa)

        nomes = ["Ana", "Bruno", "Camila", "Diego", "Elisa", "Fabio", "Gisele", "Henrique", "Isabela", "Joao", "Larissa", "Marcos"]
        sobrenomes = ["Silva", "Santos", "Oliveira", "Costa", "Pereira", "Lima", "Rocha", "Moura", "Alves", "Cardoso"]
        statuses = [
            Cliente.Status.ATIVO,
            Cliente.Status.VIP,
            Cliente.Status.RECORRENTE,
            Cliente.Status.INATIVO,
            Cliente.Status.PERDIDO,
            Cliente.Status.ORCAMENTO_ABANDONADO,
            Cliente.Status.POS_VENDA_PENDENTE,
        ]
        dias = [18, 42, 67, 91, 126, 178, 213, 248, 305, 372, 446, 590]
        carina = User.objects.get(username="carina.fernandes")

        for i in range(120):
            empresa = empresas[i % len(empresas)]
            nome = f"{random.choice(nomes)} {random.choice(sobrenomes)} {i + 1}"
            compras = random.randint(1, 12)
            valor = Decimal(random.randint(350, 16000))
            if i % 10 == 0:
                valor = Decimal(random.randint(8500, 22000))
            status = statuses[i % len(statuses)]
            ultimo = timezone.localdate() - timedelta(days=dias[i % len(dias)])
            cliente, _ = Cliente.objects.update_or_create(
                email=f"cliente{i + 1}@demo.com.br",
                defaults={
                    "empresa": empresa,
                    "nome": nome,
                    "telefone": f"1198{i:07d}"[:11],
                    "whatsapp": f"1199{i:07d}"[:11],
                    "origem": random.choice(["Indicacao", "Instagram", "Google", "WhatsApp", "Evento"]),
                    "ultimo_atendimento": ultimo,
                    "valor_total_gasto": valor,
                    "quantidade_compras": compras,
                    "status": status,
                    "observacoes": "Cliente ficticio criado para demonstracao da Aleica Gestao.",
                },
            )
            oportunidade = gerar_oportunidades(cliente)
            SnapshotInteligencia.objects.create(
                cliente=cliente,
                score_aleica=calcular_score_aleica(cliente),
                risco=calcular_risco(cliente),
                probabilidade_perda=calcular_probabilidade_perda(cliente),
                dias_sem_retorno=calcular_dias_sem_retorno(cliente),
                valor_potencial=calcular_valor_potencial(cliente),
                motivo_alerta=gerar_motivo_alerta(cliente),
            )
            if i % 3 == 0:
                HistoricoContato.objects.create(
                    cliente=cliente,
                    usuario=carina,
                    oportunidade=oportunidade,
                    data_contato=timezone.now() - timedelta(days=random.randint(3, 85)),
                    tipo_contato=random.choice(["WhatsApp", "Telefone", "E-mail"]),
                    resultado=random.choice(["Contato realizado", "Sem resposta", "Retorno agendado", "Interesse identificado"]),
                    observacao="Historico demonstrativo para simular a atuacao da Carine.",
                    proxima_acao="Acompanhar retorno",
                    data_proxima_acao=timezone.localdate() + timedelta(days=random.randint(1, 18)),
                )

        self.stdout.write(f"Empresas: {Empresa.objects.count()} | Clientes: {Cliente.objects.count()} | Oportunidades: {Oportunidade.objects.count()}")
