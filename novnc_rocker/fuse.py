import em
import getpass
import os
import pkgutil
import sys
from rocker.extensions import RockerExtension, name_to_argument


class Fuse(RockerExtension):
    @staticmethod
    def get_name():
        return 'fuse'

    def __init__(self):
        self._env_subs = {}
        self.name = Fuse.get_name()

    def get_docker_args(self, cli_args):
        return ' --cap-add SYS_ADMIN --security-opt apparmor:unconfined --device /dev/fuse'

    @staticmethod
    def register_arguments(parser, defaults={}):
        parser.add_argument(name_to_argument(Fuse.get_name()),
            action='store_true',
            default=defaults.get(Fuse.get_name(), None),
            help="enable Fuse")
