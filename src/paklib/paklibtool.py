import paklib, os, argparse
from rich.console import Console
    
def main():
    parser = argparse.ArgumentParser(description='paklib CLI')

    parser.add_argument("input_path", help="Compile or decompile given input.")

    subparsers = parser.add_subparsers(dest='command')
    compile_parser = subparsers.add_parser('compile', help='Compile a directory into a .pak file')
    compile_parser.add_argument('directory_path', help='Path to the directory')
    compile_parser.add_argument('--output', '-o', help='Output path for the .pak file', required=False)
    
    decompile_parser = subparsers.add_parser('decompile', help='Decompile a .pak file into a directory')
    decompile_parser.add_argument('pak_file_path', help='Path to the .pak file')
    decompile_parser.add_argument('--output', '-o', help='Output directory', required=False)

    args = parser.parse_args()

    console = Console()

    if args.command == 'compile' and os.path.isdir(args.directory_path):
        paklib.compile(args.directory_path, args.output)
        console.print("[bold green]Compilation completed successfully![/bold green]")
    elif args.command == 'decompile' and args.pak_file_path.endswith('.pak'):
        paklib.decompile(args.pak_file_path, args.output)
        console.print("[bold green]Decompilation completed successfully![/bold green]")
    elif args.input_path != None:
        if os.path.isdir(args.input_path):
            paklib.compile(args.input_path)
        elif args.input_path.endswith('.pak'):
            paklib.decompile(args.input_path) 
    else:        
        parser.print_help()

if __name__ == '__main__':
    main()
