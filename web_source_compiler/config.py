import yaml
from dataclasses import dataclass
import shutil
import os
import logging
from dataclasses_json import dataclass_json
import sys

PACKAGES_DIR = ".wsc-packages"
LOCAL_KEYWORD = "local"

DEPENDENCIES_KEYWORD = 'dependencies'
PROJECT_DIR_KEYWORD = 'project_dir'
DIST_DIR_KEYWORD = 'dist_dir'
STATIC_DIR_KEYWORD = 'static_dir'

def add_git_dependency(self, dep Dependency) -> None:
    pass
    
def add_http_depdency(self, dep Dependency) -> None:
    pass

def add_file_dependency(dep Dependency) -> None:
    pass

PROTOCOLS = {
    'git': add_git_dependency,
    'http': add_http_depdency,
    'file': add_file_dependency
}

@dataclass_json
@dataclass
class Dependency:
    remote_path: str
    username: str
    password: str
    install_path: str

@dataclass_json
@dataclass
class Config:
    project_dir: str
    dist_dir: str
    static_dir: str
    dependencies: dict[str, Dependency]

        
    def add_dependency(self, name: str, path: str, username: str, password: str) -> None:
        package_dir = f'{self.project_dir}/{PACKAGES_DIR}/{name}'
        os.makedirs(package_dir, exist_ok=True)

        parts = path.split('::')
        protocol = parts[0]
        url: parts[1]

        if os.path.exists(package_dir):
            logging.debug(f'Removing existing package directory at {package_dir}')
            shutil.rmtree(package_dir)
        
        if protocol in PROTOCOLS:
            pass
        else:
            logging.error(f'Invalid remote protocol: {protocol}. Valid protcols are {", ".join(PROTOCOLS)}')
            sys.exit(1)
        logging.debug(f'Copying package from {path} to {package_dir}...')
        shutil.copytree(path, package_dir)
        logging.debug('Done!')

        dep = Dependency(path, username, password, package_dir)

        self.dependencies[name] = package_dir

        logging.info(f'{name} successfully added at {package_dir}!')

    def remove_dependency(self, name: str) -> None:
        package_dir = f'{self.project_dir}/{PACKAGES_DIR}/{name}'
        if os.path.exists(package_dir):
            shutil.rmtree(package_dir)
        
        del self.dependencies[name]

        logging.info(f'{name} successfully removed from {package_dir}!')

    def read_config(self) -> None:
        config = {}

        logging.debug('Reading configuration...')
        with open(f'.wsc.yaml', 'r', encoding='utf-8') as config_file:
            config = yaml.safe_load(config_file)

        logging.debug(f'Found dependencies {config[DEPENDENCIES_KEYWORD]}')
        self.dependencies = config[DEPENDENCIES_KEYWORD]
        self.project_dir = config[PROJECT_DIR_KEYWORD]
        self.dist_dir = config[DIST_DIR_KEYWORD]
        self.static_dir = config[STATIC_DIR_KEYWORD]
        
        logging.debug('Done!')

    def write_config(self) -> None:
        output = {
            PROJECT_DIR_KEYWORD: self.project_dir,
            DIST_DIR_KEYWORD: self.dist_dir,
            STATIC_DIR_KEYWORD: self.static_dir,
            DEPENDENCIES_KEYWORD: self.dependencies
        }
        
        logging.debug(f'Writing out config {output}...')
        with open(f'{self.project_dir}/.wsc.yaml', 'w', encoding='utf-8') as config_file:
            yaml.safe_dump(output, config_file)

        logging.debug('Done!')
