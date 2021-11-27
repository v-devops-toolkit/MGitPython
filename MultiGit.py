#!/usr/bin/env python3

import fire
import subprocess
import yaml
import pprint
from jinja2 import Environment, BaseLoader
import os
import sys

class MultiGit(object):
    """
    MultiGit - processor for multiple git repos
    """

    def __init__(self, dir: str = '.'):
        self.__dir = dir
        self.__config = {}
        self.__config['repos'] = []
        filename = os.path.join(dir, "mgit.yaml")
        if (os.path.isfile(filename)):
            self.__load_config_file__(filename)
        else:
            self.__generate_config()

    def __set_config__(self, config):
        self.__config = config

    def __get_config__(self):
        return self.__config

    def __load_raw_config_file__(self, filename):
        with open(filename, "r") as stream:
            self.__set_config__(yaml.safe_load(stream))

    def __process_raw_config_file__(self):
        if (not self.__config.get('repos')):
            self.__config['repos'] = []
        if (not self.__config.get('baseUrl')):
            self.__config['baseUrl'] = ''
        if (not self.__config.get('dir')):
            self.__config['dir'] = ''
        if (self.__config['dir'] != ''):
            self.__config['dir'] = self.__config['dir'].rstrip('/') + '/'
        for item in self.__config['repos']:
            if (item.get('dir') == None):
                item['dir'] = self.__config['dir']
            if (item.get('url') == None):
                rtemplate = Environment(loader=BaseLoader).from_string(self.__config['baseUrl'])
                item['url'] = rtemplate.render(item)
            if (item.get('tags') == None):
                item['tags'] = []
            if (not 'all' in item['tags']):
                item['tags'].append('all')

    def __load_config_file__(self, filename):
        self.__load_raw_config_file__(filename)
        self.__process_raw_config_file__()

    def __generate_config(self):
        self.__config['repos'] = []
        for file in os.listdir(self.__dir):
            current = os.path.join(self.__dir, file)
            current_dot_git = os.path.join(current, '.git')
            if (os.path.isdir(current) and os.path.isdir(current_dot_git)):
                item = {}
                item['name'] = file
                item['dir'] = self.__dir
                item['tags'] = ['all']
                self.__config['repos'].append(item)
        self.__config['repos'] = sorted(self.__config['repos'], key=lambda x: x['name'])
        self.__process_raw_config_file__()

    def __run_commands__(self, commands, tag: str = 'all'):
        for item in self.__config['repos']:
            if (tag in item['tags']):
                print("========================================")
                print(f"REPO: {item['name']}")
                for command in commands:
                    process = subprocess.run(command, cwd=os.path.join(item['dir'], item['name']))

    def debug(self):
        """
        debug command
        """
        pprint.pprint(self.__config)

    def dump_config(self, filename: str = 'mgit.yaml'):
        """
        dump_config command
        """
        self._save_config_as_yaml(os.path.join(self.__dir, filename))

    def _get_config_yaml(self):
        return yaml.dump(self.__config)

    def _save_config_as_yaml(self, filename):
        with open(filename, "w") as text_file:
            text_file.write(self._get_config_yaml())

    def version(self):
        """
        version command
        """
        print('mgit ver. 0.4.0')

    def status(self, params: str = '-sb', tag: str = 'all'):
        """
        git status command
        :param params: command parameters
        :param tag: tag to filter repos
        """
        self.__run_commands__([
            ["git", "status", params]
        ], tag)

    def describe(self, params: str = '--tags', tag: str = 'all'):
        """
        git describe command
        :param params: command parameters
        :param tag: tag to filter repos
        """
        self.__run_commands__([
            ["git", "describe", params]
        ], tag)

    def checkout(self, params: str = 'master', tag: str = 'all'):
        """
        git checkout command
        :param params: command parameters
        :param tag: tag to filter repos
        """
        self.__run_commands__([
            ["git", "checkout", params]
        ], tag)

    def git(self, params: str = '', tag: str = 'all'):
        """
        generic git command
        :param params: command parameters
        :param tag: tag to filter repos
        """
        parts = params.split(' ')
        parts.insert(0, 'git')
        self.__run_commands__([
            parts
        ], tag)

    def info(self, tag: str = 'all'):
        """
        git status, git describe commands
        :param tag: tag to filter repos
        """
        self.__run_commands__([
            ["git", "status", "-sb"],
            ["git", "rev-parse", "--short=8", "HEAD"],
            ["git", "describe", "--tags"],
        ], tag)

    def update(self, tag: str = 'all'):
        """
        git update command
        :param tag: tag to filter repos
        """
        self.__run_commands__([
            ["git", "fetch"],
            ["git", "reset", "--hard"],
            ["git", "clean", "-df"],
            ["git", "rebase",],
        ], tag)

    def cleanup(self, tag: str = 'all'):
        """
        git cleanup command
        :param tag: tag to filter repos
        """
        self.__run_commands__([
            ["git", "fetch", "--prune"],
            ["git", "reflog", "expire", "--all", "--expire=now"],
            ["git", "prune"],
            ["git", "fsck", "--unreachable"],
            ["git", "gc"],
        ], tag)

    def clone(self, tag: str = 'all'):
        """
        git clone command
        :param tag: tag to filter repos
        """
        for item in self.__config['repos']:
            if (tag in item['tags']):
                print("========================================")
                print(f"REPO: {item['name']}")
                process = subprocess.run(["git", "clone", f"{item['url']}"], cwd=f"{item['dir']}")

def main():
    fire.Fire(MultiGit)

if __name__ == '__main__':
    main()