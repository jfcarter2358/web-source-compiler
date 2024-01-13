from web_source_compiler.config import Config, PACKAGES_DIR, PROTOCOLS
from web_source_compiler.compiler import Compiler
import argparse
import logging
from rich.logging import RichHandler
import os
import shutil
import rich_click as click

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARN": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

# add_parser.add_argument('name', help='Name to store package as')
# add_parser.add_argument('source', help='Source of WSC package, must be a URL (git or http protocols) or a local path (file protocl)')
# add_parser.add_argument('protocol', help=f'Protocol to use to retrieve package. Valid protocols are {", ".join(PROTOCOLS)}. Defaults to git', choices=PROTOCOLS, default='git')
# add_parser.add_argument('-u', '--username', help='Basic auth username for retrieval. Use env.<ENV VAR NAME> to pull value from an environment variable')
# add_parser.add_argument('-p', '--password', help='Basic auth password for retrieval. Use env.<ENV VAR NAME> to pull value from an environment variable')
# add_parser.add_argument(f'-l', '--log-level', choices=list(LOG_LEVELS.keys()), default="INFO", help=f'Log level to use, valid levels are {",".join(list(LOG_LEVELS.keys()))}. Defaults to INFO')


@click.command()
@click.option("name", help="Name to use for package")
@click.option("source", help='Source of WSC package, must be a URL (git or http protocols) or a local path (file protocl)')
@click.option("--protocol", help=f'Protocol to use to retrieve package. Valid protocols are {", ".join(PROTOCOLS)}. Defaults to git')
@click.option("--username", help=f'Protocol to use to retrieve package. Valid protocols are {", ".join(PROTOCOLS)}. Defaults to git')
@click.option("--password", help=f'Protocol to use to retrieve package. Valid protocols are {", ".join(PROTOCOLS)}. Defaults to git')
@click.option("--log-level", help=f'Protocol to use to retrieve package. Valid protocols are {", ".join(PROTOCOLS)}. Defaults to git')

def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")
def do_add(args: argparse.Namespace) -> None:
    config = Config('', '', '', {})
    config.read_config()
    config.add_dependency(args.name, args.path, args.remote, args.username, args.password)
    config.write_config()
    logging.info('Done!')

def do_compile(args: argparse.Namespace) -> None:
    config = Config('', '', '', {})
    config.read_config()

    compiler = Compiler()
    compiler.do_compile(config)

def do_init(args: argparse.Namespace) -> None:
    pwd = os.getcwd()
    logging.info(f"Initializing WSC configuration at {pwd}/{args.path}/.wsc.yaml")

    config = Config(f'{pwd}/{args.path}', f'{pwd}/{args.dist_dir}', f'{pwd}/{args.static_dir}', {'local': '.'})
    config.write_config()
    logging.info('Done!')

def do_remove(args: argparse.Namespace) -> None:
    config = Config('', '', '', {})
    config.read_config()
    config.remove_dependency(args.name)
    config.write_config()
    logging.info('Done!')

def do_clean(args: argparse.Namespace) -> None:
    config = Config('', '', '', {})
    config.read_config()

    if os.path.exists(config.dist_dir):
        logging.debug(f'Removing existing dist directory at {config.dist_dir}')
        shutil.rmtree(config.dist_dir)
    
    if os.path.exists(f'{config.project_dir}/{PACKAGES_DIR}'):
        logging.debug(f'Removing existing packages directory at {config.project_dir}/{PACKAGES_DIR}')
        shutil.rmtree(f'{config.project_dir}/{PACKAGES_DIR}')

def main() -> None:

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands', help='', required=True)

    add_parser = subparsers.add_parser('add')
    add_parser.set_defaults(func=do_add)
    add_parser.add_argument('name', help='Name to store package as')
    add_parser.add_argument('source', help='Source of WSC package, must be a URL (git or http protocols) or a local path (file protocl)')
    add_parser.add_argument('protocol', help=f'Protocol to use to retrieve package. Valid protocols are {", ".join(PROTOCOLS)}. Defaults to git', choices=PROTOCOLS, default='git')
    add_parser.add_argument('-u', '--username', help='Basic auth username for retrieval. Use env.<ENV VAR NAME> to pull value from an environment variable')
    add_parser.add_argument('-p', '--password', help='Basic auth password for retrieval. Use env.<ENV VAR NAME> to pull value from an environment variable')
    add_parser.add_argument(f'-l', '--log-level', choices=list(LOG_LEVELS.keys()), default="INFO", help=f'Log level to use, valid levels are {",".join(list(LOG_LEVELS.keys()))}. Defaults to INFO')

    clean_parser = subparsers.add_parser('clean')
    clean_parser.set_defaults(func=do_clean)
    clean_parser.add_argument(f'-l', '--log-level', choices=list(LOG_LEVELS.keys()), default="INFO", help=f'Log level to use, valid levels are {",".join(list(LOG_LEVELS.keys()))}. Defaults to INFO')

    compile_parser = subparsers.add_parser('compile')
    compile_parser.set_defaults(func=do_compile)
    compile_parser.add_argument(f'-l', '--log-level', choices=list(LOG_LEVELS.keys()), default="INFO", help=f'Log level to use, valid levels are {",".join(list(LOG_LEVELS.keys()))}. Defaults to INFO')
    
    init_parser = subparsers.add_parser('init')
    init_parser.set_defaults(func=do_init)
    init_parser.add_argument('path', help='Path to initialize WSC at')
    init_parser.add_argument('-d', '--dist-dir', default='dist', help='Location to output rendered files')
    init_parser.add_argument('-s', '--static-dir', default='static', help='Relative path to static directory to copy over to dist')
    init_parser.add_argument(f'-l', '--log-level', choices=list(LOG_LEVELS.keys()), default="INFO", help=f'Log level to use, valid levels are {",".join(list(LOG_LEVELS.keys()))}. Defaults to INFO')

    remove_parser = subparsers.add_parser('remove')
    remove_parser.set_defaults(func=do_remove)
    remove_parser.add_argument('name', help='Name of the library to remove')
    remove_parser.add_argument(f'-l', '--log-level', choices=list(LOG_LEVELS.keys()), default="INFO", help=f'Log level to use, valid levels are {",".join(list(LOG_LEVELS.keys()))}. Defaults to INFO')

    args = parser.parse_args()
    logging.basicConfig(level=LOG_LEVELS[args.log_level], format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])

    args.func(args)

if __name__ == '__main__':
    main()
