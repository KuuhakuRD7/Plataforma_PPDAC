from datetime import datetime
from dataclasses import dataclass, asdict
import pandas as pd
import json


class Utilidades:
    @staticmethod
    def salvar_instancias(inst):
        with open(
            f"inst/instancia_{inst.nome}.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                inst.to_dict(),
                f,
                ensure_ascii=False,
                indent=4,
                default=str
            )

    @staticmethod
    def carregar_instancias(caminho_inst) -> 'Dataset':
        with open(caminho_inst, "r", encoding="utf-8") as f:
            inst = json.loads(f)
        return Dataset.from_dict(inst)


# ---------------------------------------------------------
class DatasetHistorico:
    """
        Classe responsavel por guardar ações
        em função do dataset, tais como:
        - Modulo de ocorrência
        - Data de ocorrência
        - Operações executadas
        - Filtros Utilizados
    """

    def __init__(
        self,
        modulo,
        operacao,
        parametros
    ):
        self.modificado_em = datetime.now()
        self.modulo = modulo
        self.operacao = operacao
        self.parametros = parametros


# ---------------------------------------------------------
class DatasetFiguras:
    """
        Classe responsavel por guardar informações
        dos graficos gerados para o dataset, tais
        como:
        - Nome do Grafico
        - Tipo do Grafico
        - Objeto Figura
        - Parametros Utilizados
        - Data de Criação
    """

    def __init__(
        self,
        nome,
        tipo,
        figura,
        parametros,
        criado_em=None
    ):
        self.nome = nome
        self.tipo = tipo
        self.figura = figura
        self.parametros = parametros
        self.criado_em = criado_em or datetime.now()

    def to_dict(self):
        fig_json = None
        if hasattr(self.figura, "to_json"):
            fig_json = json.loads(self.figura.to_json())
        else:
            fig_json = str(self.figura)

        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "figura": fig_json,
            "parametros": self.parametros,
            "criado_em": str(self.criado_em)
        }
# ---------------------------------------------------------


class DatasetMetadata:
    """
        Classe responsavel por guardar informações
        sobre a criação do dataset, tais como:
        - Caminho/Link do Dataset
        - Codificação Utilizada
        - Separador Utilizado
        - Data de Criação
        - Data da Ultima Modificação
        - Número de Linhas
        - Número de Colunas
    """

    def __init__(self):
        self.encoding = None
        self.separador = None
        self.caminho = None

        self.criado_em = None
        self.atualizado_em = None

        self.linhas = 0
        self.colunas = 0


# ---------------------------------------------------------
@dataclass
class Dataset:
    """
        Classe responsavel por guardar informações
        do Dataset ao longo da sessão tais como:
        - Nome do Dataset
        - Dataframe
        - Caminho de Origem
        - Metadata do Dataset
        - Histórico de Operações em Função dele
        - Lista de Figuras/Gráficos Gerados
        - Lista das Variaçẽos do Dataframe
    """

    def __init__(
        self,
        nome,
        df,
        origem
    ):
        self.nome = nome
        self.df = df
        self.origem = origem

        self.metadata = DatasetMetadata()

        self.historico = []
        self.figuras = []
        self.variacoes = []

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "origem": self.origem,
            "df": self.df.to_dict() if isinstance(self.df, pd.DataFrame) else None,
            "metadata": vars(self.metadata),
            "historico": [vars(h) for h in self.historico],
            "figuras": [f.to_dict() if hasattr(f, 'to_dict') else vars(f) for f in self.figuras]
            # "variacoes": [vars]
        }

    @classmethod
    def from_dict(cls, dados: dict) -> 'Dataset':
        df_rec = pd.DataFrame.from_dict(dados.get("df", {}))

        instancia = cls(
            nome=dados.get("nome"),
            df=df_rec,
            origem=dados.get("origem")
        )

        meta_dados = dados.get("metadata", {})
        for chave, valor in meta_dados.items():
            if hasattr(instancia.metadata, chave):
                setattr(instancia.metadata, chave, valor)

        for item in dados.get("historico", []):
            hist = DatasetHistorico(
                modulo=item.get("modulo"),
                operacao=item.get("operacao"),
                parametros=item.get("parametros")
            )
            if "modificado_em" in item:
                hist.modificado_em = item["modificado_em"]
            instancia.historico.append(hist)

        for fig_data in dados.get("figuras", []):
            fig_obj = fig_data.get("figura")

            if isinstance(fig_obj, dict):
                fig_obj = pio.from_json(json.dumps(fig_obj))

            fig_instancia = DatasetFiguras(
                nome=fig_data.get("nome"),
                tipo=fig_data.get("tipo"),
                figura=fig_obj,
                parametros=fig_data.get("parametros"),
                criado_em=fig_data.get("criado_em")
            )
            instancia.figuras.append(fig_instancia)

        return instancia
