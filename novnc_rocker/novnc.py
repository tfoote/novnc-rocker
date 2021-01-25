import em
import pkgutil
import sys
from rocker.extensions import RockerExtension, name_to_argument


class NoVNC(RockerExtension):
    @staticmethod
    def get_name():
        return 'novnc'

    def __init__(self):
        self._env_subs = {}
        self.name = NoVNC.get_name()

    def precondition_environment(self, cli_args):
        pass

    def validate_environment(self, cli_args):
        pass

    def get_preamble(self, cli_args):
        return ''

    def get_files(self, cli_args):
        file_list = ['supervisor.conf']
        files = {}
        for f in file_list:
            files['%s' % f] = pkgutil.get_data(
                'novnc_rocker',
                'templates/%s' % f).decode('utf-8')
        template_list = ['novnc.conf']
        for f in template_list:
            files['%s' % f] = em.expand(
                pkgutil.get_data(
                'novnc_rocker',
                'templates/%s.em' % f).decode('utf-8'),
                cli_args)
        return files

    def get_snippet(self, cli_args):
        snippet = pkgutil.get_data(
            'novnc_rocker',
            'templates/%s_snippet.Dockerfile.em' % self.name).decode('utf-8')
        return em.expand(snippet, self._env_subs)

    def get_docker_args(self, cli_args):
        return '-p %s:%s' % (cli_args['novnc_port'], cli_args['novnc_port'])

    @staticmethod
    def register_arguments(parser, defaults={}):
        parser.add_argument(name_to_argument(NoVNC.get_name()),
            action='store_true',
            default=defaults.get(NoVNC.get_name(), None),
            help="enable noVNC")
        parser.add_argument('--novnc-port',
            action='store',
            type=int,
            default=defaults.get('novnc-port', 6080),
            help="what port to use for novnc")