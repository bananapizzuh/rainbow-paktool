import rich_click as click
from paklib import pak_compiler, pak_decompiler


@click.group()
def cli():
    pass


@cli.command()
@click.argument("directory")
@click.argument("output_file")
def pak(directory, output_file):
    """
    Compile a directory into a .pak file.

    Args:
        directory_path (str): Path to the directory to compile.
        output_file (str): Path to the output .pak file.
    """
    compiler = pak_compiler.PAKCompiler()
    compiler.add_directory(directory)
    compiler.compile(output_file)


@cli.command()
@click.argument("archive_file")
@click.argument("output_directory")
def depak(archive_file, output_directory):
    """
    Decompile a .pak file into a directory.

    Args:
        input_file (str): Path to the input .pak file.
        output_directory (str): Path to the output directory.
    """
    decompiler = pak_decompiler.PAKDecompiler()
    decompiler.decompile(archive_file, output_directory)


if __name__ == "__main__":
    cli()
