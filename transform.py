import json

import argparse

from transformer import Transformer
import os
from os import listdir
from os.path import isfile, join


class Main:
    def __init__(self, target_schema, output_folder, prefix=''):
        self.target_schema = target_schema
        self.source_iterator = None
        self.output_folder = output_folder
        self.prefix = prefix

    def transform(self):
        target_schema = self.read_file(self.target_schema)
        for source_path, source_content in self.source_iterator:
            result = Transformer(source_content, target_schema).transform()
            self.write_file(
                '{}/{}{}'.format(self.output_folder, self.prefix, source_path),
                result
            )

    def source_from_file(self, source_file):
        yield source_file.split('/')[-1], self.read_file(source_file)

    def source_from_directory(self, source_directory):
        for source_file in self.folder_iterator(source_directory):
            yield source_file.split('/')[-1], self.read_file(source_file)

    @staticmethod
    def folder_iterator(path):
        return ('{}{}'.format(path, f) for f in listdir(path) if
                isfile(join(path, f)))

    @staticmethod
    def read_file(source_path):
        with open(source_path) as sf:
            return json.load(sf)

    @staticmethod
    def write_file(target_path, content):
        with open(target_path, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(content, ensure_ascii=False))


def arg_parse():
    parser = argparse.ArgumentParser(description='Data transformer')
    parser.add_argument('target_schema',
                        help='schema that will be applied to source')
    parser.add_argument('-f', '--file', help='source file to transform')
    parser.add_argument('-d', '--directory', help='source folder to transform')

    parser.add_argument('-p', '--prefix', default='',
                        help='prefix to rename new files')

    default_output = '{}/transformed'.format(
        os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument('-t', '--to', default=default_output,
                        help='target folder to save the output')

    return parser.parse_args()


if __name__ == '__main__':
    args = arg_parse()

    t = Main(args.target_schema, args.to, args.prefix)

    if args.file:
        t.source_iterator = t.source_from_file(args.file)

    if args.directory:
        t.source_iterator = t.source_from_directory(args.directory)

    t.transform()
