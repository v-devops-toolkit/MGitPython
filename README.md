# mgit

This script helps to run the same git commands
in multiple repositories.

For example, if you want to checkout `abc` branch in all the repos,
then all you need to run is

    mgit checkout abc

## Install

Install dependencies:

    pip3 install -r requirements.txt

and copy `mgit` script to some location which is included in your path.

## Configure

Create the file named `mgit.yaml` and fill it with information about
repositories that you want to work with, for example:

    # mgit.yaml
    dir: "../../tmp"
    baseUrl: git@github.com:PragmaticGuideToTheCloud/{{name}}.git

    repos:

      - name: mgit
        tags:
          - product

      - name: gitignore
        url: git@github.com:github/gitignore.git
        tags:
          - two

The file may be located anywhere on your filesystem.

The command `mgit` should be executed in the directory, where `mgit.yaml` file is located.

Verify the configuration with:

    mgit debug

The command dumps the configuration to stdout.

## Commands

Print help:

    mgit

Check status:

    mgit status

Change branches:

    mgit checkout master

Run generic git command or git alias:

    # l is an alias to git log --oneline
    mgit git "l -1"

## Unit tests

    pytest test*.py
