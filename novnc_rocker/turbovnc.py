import em
import pkgutil
import sys
from rocker.extensions import RockerExtension, name_to_argument


class TurboVNC(RockerExtension):
    @staticmethod
    def get_name():
        return 'turbovnc'

    def __init__(self):
        self._env_subs = {}
        self.name = TurboVNC.get_name()

    def precondition_environment(self, cli_args):
        pass

    def validate_environment(self, cli_args):
        pass

    def get_preamble(self, cli_args):
        return ''

    def get_files(self, cli_args):
        file_list = ['supervisor.conf', 'turbovnc.conf']
        files = {}
        for f in file_list:
            files['%s' % f] = pkgutil.get_data(
                'novnc_rocker',
                'templates/%s' % f).decode('utf-8')
        return files

    def get_snippet(self, cli_args):
        snippet = pkgutil.get_data(
            'novnc_rocker',
            'templates/%s_snippet.Dockerfile.em' % self.name).decode('utf-8')
        return em.expand(snippet, self._env_subs)

    def get_docker_args(self, cli_args):
        return ''

    @staticmethod
    def register_arguments(parser, defaults={}):
        parser.add_argument(name_to_argument(TurboVNC.get_name()),
            action='store_true',
            default=defaults.get(TurboVNC.get_name(), None),
            help="enable TurboVNC")
