import os
import yaml
from dataclasses import dataclass
import logging
import re
from typing import Any
from web_source_compiler.config import Config
from copy import deepcopy
import shutil
import sys
from dataclasses_json import dataclass_json

REQUIRE_KEYWORD = "require "
IMPORT_KEYWORD = "import "

PY_KEYWORD = 'py'
YAML_KEYWORD = 'yaml'
JS_KEYWORD = 'js'
HTML_KEYWORD = 'html'
CSS_KEYWORD = 'css'

@dataclass_json
@dataclass
class WSCObject:
    name: str
    props: dict
    imports: list[str]
    js: str
    html: str
    css: str
    required: list[str]
    default_js: str
    default_html: str
    default_css: str
    default_props: dict = None

    def replace_refs(self) -> None:
        pattern = r'\$\{\{\s?\S*\s?\}\}'
        for obj in [JS_KEYWORD, HTML_KEYWORD, CSS_KEYWORD]:
            logging.debug(f'Replacing values in {obj} block...')

            if obj == JS_KEYWORD:
                contents = self.default_js
            elif obj == HTML_KEYWORD:
                contents = self.default_html
            elif obj == CSS_KEYWORD:
                contents = self.default_css

            if not contents:
                continue
            matches = re.findall(pattern, contents)
            for match in matches:
                name = match[3:-2].strip()
                logging.debug(f'Found replacement {name}')
                value = self.get_prop(name, self.props)
                
                logging.debug(f'Replacing {match} with "{value}"')
                contents = contents.replace(match, value)
            
            if obj == JS_KEYWORD:
                self.js = contents
            elif obj == HTML_KEYWORD:
                self.html = contents
            elif obj == CSS_KEYWORD:
                self.css = contents
            logging.debug('Done!')
    
    def load_defaults(self) -> Any:
        self.props = deepcopy(self.default_props)
        self.js = self.default_js
        self.html = self.default_html
        self.css = self.default_css
        
    def get_prop(self, path: str, props: dict, full_path: str = '') -> Any:
        if not full_path:
            full_path = path
        parts = path.split('.')
        
        if len(parts) > 1:
            return self.get_prop('.'.join(parts[1:]), props[parts[0]], path)
        else:
            if not parts[0] in props:
                raise KeyError(f'Property {parts[0]} is not present in WSC object properties (.{full_path})')
            return props[parts[0]]
        
    def set_props(self, old_props: dict, new_props: dict) -> None:
        if not new_props:
            return
        for key in new_props:
            if not key in old_props:
                raise KeyError(f'Cannot set property {key}, key does not exist')
            if isinstance(old_props[key], dict):
                self.set_props(old_props[key], new_props[key])
            old_props[key] = new_props[key]
    
    def __str__(self) -> str:
        return f'{self.to_json()}'
    
    def __repr__(self) -> str:
        return f"WSCObject({self.to_json()[1:-1]})"

class Compiler:
    def __init__(self) -> None:
        self.objs = {}

    def do_compile(self, config: Config) -> None:
        files = [f for f in os.listdir(config.project_dir) if f.endswith('.wsc')]
        names = [f[:-4] for f in files]

        for idx, filename in enumerate(files):
            self.load_object(filename, names[idx], config)

        for name in names:
            self.replace_modules(self.objs[name], config)
            for required in self.objs[name].required:
                if not required in names:
                    logging.critical(f'Required module {required} has not been imported, bailing out')
                    sys.exit(1)

        if os.path.exists(config.dist_dir):
            logging.debug(f'Removing existing build at {config.dist_dir}')
            shutil.rmtree(config.dist_dir)
        os.makedirs(config.dist_dir, exist_ok=True)

        if os.path.exists(config.static_dir):
            shutil.copytree(config.static_dir, f'{config.dist_dir}/static')

        os.makedirs(f'{config.dist_dir}/templates', exist_ok=True)
        os.makedirs(f'{config.dist_dir}/static/js', exist_ok=True)
        os.makedirs(f'{config.dist_dir}/static/css', exist_ok=True)
        os.makedirs(f'{config.dist_dir}/static/img', exist_ok=True)
        
        for name in names:
            with open(f'{config.dist_dir}/templates/{name}.html', 'w', encoding='utf-8') as out_file:
                out_file.write(self.objs[name].html)
            with open(f'{config.dist_dir}/static/js/{name}.js', 'w', encoding='utf-8') as out_file:
                out_file.write(self.objs[name].js)
            with open(f'{config.dist_dir}/static/css/{name}.css', 'w', encoding='utf-8') as out_file:
                out_file.write(self.objs[name].css)

    def load_object(self, path: str, name: str, config: Config):
        props = {}
        js = ''
        html = ''
        css = ''
        imports = []

        with open(path, 'r', encoding='utf-8') as wsc_file:
            lines = wsc_file.read().split('\n')

        js = self.get_block(lines, JS_KEYWORD)
        html = self.get_block(lines, HTML_KEYWORD)
        css = self.get_block(lines, CSS_KEYWORD)

        props = {}
        props_str = self.get_block(lines, YAML_KEYWORD)
        if props_str:
            props = yaml.safe_load(props_str)

        imports = []
        required = []
        imports_str = self.get_block(lines, PY_KEYWORD)
        if imports_str:
            lines = imports_str.split('\n')
            for line in lines:
                line = line.strip()
                # if the line is empty then skip it
                if not line:
                    continue

                if line.startswith(REQUIRE_KEYWORD):
                    if len(line) < len(REQUIRE_KEYWORD):
                        logging.error(f'Require line "{line}" is malformed, skipping requirement')
                        continue
                    required.append(line[len(REQUIRE_KEYWORD):])
                elif line.startswith(IMPORT_KEYWORD):
                    if len(line) < len(IMPORT_KEYWORD):
                        logging.error(f'Import line "{line}" is malformed, skipping import')
                        continue
                    imports.append(line[len(IMPORT_KEYWORD):])

        obj = WSCObject(name, props, imports, js, html, css, required, js, html, css, deepcopy(props))
        self.objs[name] = obj

        for import_name in imports:
            parts = import_name.split('.')
            module_name = parts[0]
            if not module_name in config.dependencies:
                raise KeyError(f'module {import_name} does not exist in project, add it using "wsc add ..."')
            module_path = config.dependencies[module_name]
            module_subpath = "/".join(parts[1:])
            self.load_object(f'{module_path}/{module_subpath}.wsc', import_name, config)

    def replace_modules(self, obj: WSCObject, config: Config) -> None:
        obj.replace_refs()
        out = []
        lines = obj.html.split('\n')

        replacement_data = ''
        in_replacement = False
        replacement_module = ''

        for line in lines:
            should_continue = False
            if not in_replacement:
                for module in config.dependencies:
                    if line.strip().startswith(f'<{module}'):
                        replacement_data = ''
                        replacement_module = line.strip()[1:line.find('>')].strip()
                        if replacement_module.endswith('>'):
                            replacement_module = replacement_module[:-1]
                        in_replacement = True
                        should_continue = True
                        continue

                if should_continue:
                    should_continue = False
                    continue

            if in_replacement:
                if line.strip().startswith(f'</{replacement_module}'):
                    logging.debug(f'Found {replacement_module} submodule, rendering')
                    data = yaml.safe_load(replacement_data)
                    self.objs[replacement_module].load_defaults()
                    self.objs[replacement_module].set_props(self.objs[replacement_module].props, data)
                    self.objs[replacement_module].replace_refs()
                    self.replace_modules(self.objs[replacement_module], config)

                    out += self.objs[replacement_module].html.split('\n')

                    obj.js += f"\n\n// imported from {replacement_module}\n\n{self.objs[replacement_module].js}"
                    obj.css += f"\n\n/* imported from {replacement_module} */\n\n{self.objs[replacement_module].css}"

                    replacement_module = ''
                    replacement_data = ''
                    in_replacement = False
                    continue
                replacement_data += f'{line}\n'
            else:
                out.append(line)

        obj.html = '\n'.join(out)

    def get_block(self, lines: str, block_type: str) -> str:
        value_lines = []
        in_value = False
        for line in lines:
            # get beginning of properties block
            if line.strip() == f'```{block_type}':
                in_value = True
                continue
            if line.strip() == '```':
                in_value = False
                continue
            if in_value:
                value_lines.append(line)
        values = '\n'.join(value_lines)
        return values
