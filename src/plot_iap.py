import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Diretórios
PROCESSED_DIR = Path("data/processed")
FIGS_DIR = PROCESSED_DIR / "figs"
FIGS_DIR.mkdir(parents=True, exist_ok=True)

# Carrega dataset consolidado e limpo
df = pd.read_csv(PROCESSED_DIR / "consolidado_despesas_limpo.csv")

# ======================================================
# Gráfico 1 — Top 5 Operadoras por Média Trimestral
# ======================================================
def plot_top5_bar(df: pd.DataFrame):
    top5 = (
        df.groupby(["cnpj", "razao_social"])["valor_despesas"]
        .mean()
        .reset_index()
        .sort_values("valor_despesas", ascending=False)
        .head(5)
    )

    # Nome curto para visualização
    top5["label"] = top5["razao_social"].str.slice(0, 30) + "..."

    plt.figure(figsize=(10, 6))
    plt.barh(top5["label"], top5["valor_despesas"])
    plt.xlabel("Média Trimestral do Indicador de Despesas (ANS)")
    plt.title("Top 5 Operadoras por Média Trimestral de Despesas")
    plt.gca().invert_yaxis()
    plt.tight_layout()

    plt.savefig(FIGS_DIR / "top5_operadoras_bar.png")
    plt.close()


# ======================================================
# Gráfico 2 — Evolução Trimestral das Top 5 Operadoras
# ======================================================
def plot_evolucao_top5(df: pd.DataFrame):
    # Seleciona top 5 operadoras por média
    top5_cnpjs = (
        df.groupby("cnpj")["valor_despesas"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .index
    )

    df_top5 = df[df["cnpj"].isin(top5_cnpjs)].copy()

    # Cria coluna de ordenação temporal
    df_top5["periodo"] = (
        df_top5["ano"].astype(str) + " Q" + df_top5["trimestre"].astype(str)
    )
    df_top5["ordem"] = df_top5["ano"] * 10 + df_top5["trimestre"]
    df_top5 = df_top5.sort_values("ordem")

    plt.figure(figsize=(12, 7))

    for nome, grupo in df_top5.groupby("razao_social"):
        plt.plot(
            grupo["periodo"],
            grupo["valor_despesas"],
            marker="o",
            label=nome[:30] + "..."
        )

    plt.xlabel("Ano / Trimestre")
    plt.ylabel("Indicador de Despesas (ANS – valor agregado trimestral)")
    plt.title("Evolução Trimestral das Despesas — Top 5 Operadoras")
    plt.legend(title="Operadora", fontsize=9)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(FIGS_DIR / "evolucao_top5.png")
    plt.close()


# ======================================================
# Execução
# ======================================================
if __name__ == "__main__":
    plot_top5_bar(df)
    plot_evolucao_top5(df)
    print(f"Gráficos gerados em: {FIGS_DIR}")
