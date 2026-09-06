import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from .scanner import find_generations
from .pipeline import run_pipeline
from .voiceover import VOICE_PROFILES

from pathlib import Path

app = typer.Typer(name='flow-compose')
import os

FINAL_VIDEO_DIR = os.environ.get('FINAL_VIDEO_DIR', str(Path.home() / 'Downloads' / 'comics en ingles'))


_VOICE_HELP = 'Voz de Edge-TTS (aleatoria por video si no se especifica). Disponibles: ' + ', '.join(VOICE_PROFILES)


@app.callback(invoke_without_command=True)
def main(
    input_dir: str = typer.Option(None, '--input', '-i', help='Ruta a Flow_Generations o a una generación específica'),
    voice: str = typer.Option(None, '--voice', '-v', help=_VOICE_HELP),
    rate: float = typer.Option(None, '--rate', '-r', help='Velocidad de la voz (0.88-1.08, usa la del perfil si no se especifica)'),
    output: str = typer.Option(None, '--output', '-o', help='Nombre del video de salida (sin extensión)'),
    output_dir: str = typer.Option('output', '--output-dir', help='Directorio de salida'),
    width: int = typer.Option(1080, '--width', '-w', help='Ancho del video final'),
    height: int = typer.Option(1920, '--height', '-h', help='Alto del video final'),
):
    generations = find_generations(input_dir)

    if not generations:
        console.print('[red]No se encontraron generaciones con script.json y videos.[/]')
        console.print('Busca en: ~/Downloads/Flow_Generations/')
        raise typer.Exit(1)

    if len(generations) == 1:
        gen = generations[0]
        console.print(f'[green]Usando única generación:[/] {gen["name"]}')
    else:
        table = Table(title='Generaciones disponibles')
        table.add_column('#', style='cyan')
        table.add_column('Carpeta', style='green')
        table.add_column('Escenas', justify='right')
        table.add_column('Título')

        for i, g in enumerate(generations, 1):
            meta = g['script'].get('metadata', {})
            title = meta.get('title', '')
            table.add_row(str(i), g['name'], str(g['scene_count']), title)

        console.print(table)
        choice = Prompt.ask('Selecciona el número', default='1')
        try:
            idx = int(choice) - 1
            gen = generations[idx]
        except (ValueError, IndexError):
            console.print('[red]Selección inválida[/]')
            raise typer.Exit(1)

    console.print(f'\n[bold]Procesando:[/] {gen["name"]}')
    console.print(f'[bold]Escenas:[/] {gen["scene_count"]}')
    console.print(f'[bold]Voz:[/] {voice or "aleatoria"}')
    console.print(f'[bold]Rate:[/] {rate or "del perfil de la voz"}')
    console.print(f'[bold]Resolución:[/] {width}x{height}')

    final = run_pipeline(gen, output, voice, rate, output_dir, width, height, final_video_dir=FINAL_VIDEO_DIR)
    print(f'\nOK - Video final: {final}')


if __name__ == '__main__':
    app()
