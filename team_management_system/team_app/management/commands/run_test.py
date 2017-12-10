import os
import sys

import copy
from coverage.cmdline import main
from django.core.management.commands.test import Command as TestCommand


class Command(TestCommand):
    help = 'Runs all the tests and computes coverage. Similar to test.'

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        self._validate_current_directory()

        # Default exit code is Error
        exit_code = 1
        try:
            # Rename all migrations folders to migrations_temp
            self._rename_sub_directories('migrations', 'migrations_temp')
            # Coverage run for running tests
            exit_code = main(argv=['run', 'manage.py', 'test', '-v2'] + self._get_input_arguments())
        finally:
            # Undo rename of all migrations folders
            self._rename_sub_directories('migrations_temp', 'migrations')

        sys.exit(exit_code)


    # Renames all the folders matching the from_directory_name to the to_directory_name in one level below the current folder
    def _rename_sub_directories(self, from_directory_name, to_directory_name):
        for directory in os.listdir('.'):
            from_dir = os.path.join(directory, from_directory_name)
            if os.path.exists(from_dir):
                to_dir = os.path.join(directory, to_directory_name)
                print("Moving %s to %s" % (from_dir, to_dir))
                os.rename(from_dir, to_dir)

    def _validate_current_directory(self):
        if not os.path.exists('manage.py'):
            print('Run this command from the same directory as manage.py')
            sys.exit(1)

    def _get_input_arguments(self):
        input_args = copy.copy(sys.argv)
        input_args.remove('manage.py')
        input_args.remove('run_test')
        return input_args