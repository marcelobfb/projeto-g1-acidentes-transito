"""Modelo relacional e utilitários de persistência (SQLAlchemy + SQLite)."""

import os

import pandas as pd
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "dados", "simulacao_acidentes_transito_brasil.csv")
DB_PATH = os.path.join(BASE_DIR, "database", "acidentes.db")
DB_URL = f"sqlite:///{DB_PATH}"

Base = declarative_base()


class Acidente(Base):
    __tablename__ = "acidentes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    data = Column(String, nullable=False)
    regiao = Column(String, nullable=False)
    uf = Column(String, nullable=False)
    municipio = Column(String, nullable=False)
    rodovia = Column(String, nullable=False)
    tipo_acidente = Column(String, nullable=False)
    condicao_climatica = Column(String, nullable=False)
    periodo_dia = Column(String, nullable=False)
    acidentes = Column(Integer, nullable=False)
    feridos = Column(Integer, nullable=False)
    obitos = Column(Integer, nullable=False)
    veiculos_envolvidos = Column(Integer, nullable=False)
    nivel_gravidade = Column(String, nullable=False)


def get_engine():
    return create_engine(DB_URL)


def init_db(force: bool = False) -> str:
    """Cria o banco SQLite a partir do CSV bruto, se ainda não existir."""
    if os.path.exists(DB_PATH) and not force:
        return DB_PATH

    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    engine = get_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    df.to_sql("acidentes", engine, if_exists="append", index=False)
    return DB_PATH


def load_dataframe() -> pd.DataFrame:
    """Carrega os dados do SQLite; cria o banco automaticamente se necessário."""
    if not os.path.exists(DB_PATH):
        init_db()
    engine = get_engine()
    df = pd.read_sql_table("acidentes", engine)
    df["data"] = pd.to_datetime(df["data"])
    return df


if __name__ == "__main__":
    path = init_db(force=True)
    print(f"Banco de dados criado em: {path}")
