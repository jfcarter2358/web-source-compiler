import os
import re
import sys
import json
import shutil
from cartils.logger import Logger

def handle_imports(root, contents, file_type, patterns, prefixes, suffixes, logger):

    for match in re.finditer(patterns[file_type], contents):
        indent = match.group(1)
        path = match.group(2)
        logger.DEBUG(f'Found import for {path}')
        if not os.path.exists(f'{root}/{path}'):
            logger.ERROR(f'File {path} does not exist!')
            continue
        with open(f'{root}/{path}') as file_obj:
            replacement = handle_imports(root, file_obj.read(), file_type, patterns, prefixes, suffixes, logger)
            lines = replacement.split('\n')
            replacement = f'\n{indent}'.join(lines)
            contents = contents.replace(f'{prefixes[file_type]}{path}{suffixes[file_type]}', replacement)
    return contents

def main():
    if len(sys.argv) < 2:
        print('WSC requires a second argument of either `init`, `setup`, or `compile`')
        sys.exit(1)
    if sys.argv[1] == 'init':
        logger = Logger('INFO')
        logger.INFO('Starting initialization')
        data = {
            'log_level': 'INFO',
            'in': {
                'css': 'src/css',
                'html': 'src/html',
                'img': 'src/img',
                'js': 'src/js'
            },
            'out': {
                'css': 'build/css',
                'html': 'build/html',
                'img': 'build/img',
                'js': 'build/js'
            }
        }
        with open('.wsc', 'w') as f:
            json.dump(data, f, indent=4)
        logger.SUCCESS('Done!')
    elif sys.argv[1] == 'setup':
        if not os.path.exists('.wsc'):
            raise FileExistsError('.wsc file not found, run `wsc init` first')
        with open('.wsc') as f:
            data = json.load(f)
        logger = Logger(data['log_level'])
        logger.INFO('Starting setup')
        os.makedirs(f'{data["in"]["css"]}/main')
        os.makedirs(f'{data["in"]["css"]}/modules')
        os.makedirs(f'{data["in"]["html"]}/main')
        os.makedirs(f'{data["in"]["html"]}/modules')
        os.makedirs(f'{data["in"]["img"]}')
        os.makedirs(f'{data["in"]["js"]}/main')
        os.makedirs(f'{data["in"]["js"]}/modules')
        logger.SUCCESS('Done!')
    elif sys.argv[1] == 'compile':
        if not os.path.exists('.wsc'):
            raise FileExistsError('.wsc file not found, run `wsc init` and `wsc setup` first')
        in_css_path = ''
        in_html_path = ''
        in_img_path = ''
        in_js_path = ''

        out_css_path = ''
        out_html_path = ''
        out_img_path = ''
        out_js_path = ''

        with open('.wsc') as f:
            data = json.load(f)
        in_css_path = data['in']['css']
        in_html_path = data['in']['html']
        in_img_path = data['in']['img']
        in_js_path = data['in']['js']

        out_css_path = data['out']['css']
        out_html_path = data['out']['html']
        out_img_path = data['out']['img']
        out_js_path = data['out']['js']

        log_level = data['log_level']

        logger = Logger(log_level)
        logger.INFO('Starting compilation')

        patterns = {
            'css': r'([ \t]*)/\* import (\S*) \*/',
            'html': r'([ \t]*)<!-- import (\S*) -->',
            'js': r'([ \t]*)// import (\S*)'
        }

        prefixes = {
            'css': '/* import ',
            'html': '<!-- import ',
            'js': '// import '
        }

        suffixes = {
            'css': ' */',
            'html': ' -->',
            'js': ''
        }

        in_paths = {
            'css': in_css_path,
            'html': in_html_path,
            'img': in_img_path,
            'js': in_js_path
        }

        out_paths = {
            'css': out_css_path,
            'html': out_html_path,
            'img': out_img_path,
            'js': out_js_path
        }

        if os.path.exists(f'{out_html_path}'):
            shutil.rmtree(f'{out_html_path}')
        os.makedirs(f'{out_html_path}', exist_ok=True)
        if os.path.exists(f'{out_js_path}'):
            shutil.rmtree(f'{out_js_path}')
        os.makedirs(f'{out_js_path}', exist_ok=True)
        if os.path.exists(f'{out_css_path}'):
            shutil.rmtree(f'{out_css_path}')
        os.makedirs(f'{out_css_path}', exist_ok=True)
        if os.path.exists(f'{out_img_path}'):
            shutil.rmtree(f'{out_img_path}')
        else:
            os.makedirs(f'{out_img_path}', exist_ok=True)
            shutil.rmtree(f'{out_img_path}')
        shutil.copytree(f'{in_img_path}', f'{out_img_path}')

        for file_type in patterns:
            for file_name in os.listdir(f'{in_paths[file_type]}/main'):
                logger.INFO(f'Building {file_name}')
                with open(f'{in_paths[file_type]}/main/{file_name}') as file_obj:
                    contents = file_obj.read()
                    out = handle_imports(f'{in_paths[file_type]}/modules', contents, file_type, patterns, prefixes, suffixes, logger)
                with open(f'{out_paths[file_type]}/{file_name}', 'w') as f:
                    f.write(out)

        for file_name in os.listdir(out_paths["css"]):
            with open(f'{out_paths["css"]}/{file_name}') as file_obj:
                contents = file_obj.read()
            for match in re.finditer(r'([ \t]*)/\* use (\S*) \*/', contents):
                indent = match.group(1)
                class_name = match.group(2)
                # print(r'\.' + class_name + r'\s?{[^\}]*}')
                replacement = re.search(r'(?:\S*)?\.' + class_name + r'(?:\S*)?\s?{([^\}]*)}', contents).group(1)
                lines = replacement.split('\n')
                replacement = f'\n{indent}'.join(lines)
                contents = contents.replace(f'/* use {class_name} */', replacement)
            with open(f'{out_paths["css"]}/{file_name}', 'w') as file_obj:
                file_obj.write(contents)

        logger.SUCCESS('Done!')

if __name__ == '__main__':
    main()