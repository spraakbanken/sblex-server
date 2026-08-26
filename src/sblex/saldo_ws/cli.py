import typer
from sblex_fjall_morphology import FjallMorphology

from sblex.saldo_ws import config

app = typer.Typer()


@app.command()
def main():
    print("saldo-ws")


@app.command("init-db")
def init_db(input_file: str):
    print(f"Building db from {input_file} ...")
    settings = config.read_settings_from_env()
    morph = FjallMorphology(settings.morphology_path)
    morph.build_from_path(input_file)
    print("  ... done!")
