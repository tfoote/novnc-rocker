import em
import getpass
import os
import pkgutil
import sys
from rocker.extensions import RockerExtension, name_to_argument
from rocker.os_detector import detect_os


class TurboVNC(RockerExtension):
    @staticmethod
    def get_name():
        return 'turbovnc'

    def __init__(self):
        self._env_subs = {}
        self.name = TurboVNC.get_name()
        self.SUPPORTED_CODENAMES = ['focal']

    def compute_env_subs(self, cli_args):
        # TODO(tfoote) this caches cli_args implicitly
        if not self._env_subs:
            # default case
            # Todo evaluate elsewhere?
            self._env_subs['vnc_user'] = 'root'
            self._env_subs['vnc_user_home'] = '/root'
            if 'user' in cli_args:
                if cli_args['user']:
                    self._env_subs['vnc_user'] = cli_args['user_override_name'] if cli_args['user_override_name'] else getpass.getuser()
                    self._env_subs['vnc_user_home'] = os.path.join('/home/', cli_args['user_override_name']) if cli_args['user_override_name'] else os.path.expanduser('~')
        return self._env_subs

    def precondition_environment(self, cli_args):
        detected_os = detect_os(cli_args['base_image'], print, nocache=cli_args.get('nocache', False))
        if detected_os is None:
            print("WARNING unable to detect os for base image '%s', maybe the base image does not exist" % cliargs['base_image'])
            sys.exit(1)
        dist, ver, codename = detected_os
        if codename not in self.SUPPORTED_CODENAMES:
            print("ERROR: Unsupported codename for base image: %s not in %s" % (codename, self.SUPPORTED_CODENAMES))
            sys.exit(1)

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
        template_list = ['turbovnc.conf']
        self.compute_env_subs(cli_args)
        for f in template_list:
            try:
                files['%s' % f] = em.expand(
                    pkgutil.get_data(
                    'novnc_rocker',
                    'templates/%s.em' % f).decode('utf-8'),
                    self._env_subs)
            except (NameError, TypeError) as ex:
                raise NameError("Failed to evaluate template %s: %s \args are: %s" % (f, ex, self._env_subs))
        return files

    def get_snippet(self, cli_args):
        self.compute_env_subs(cli_args)
        snippet = pkgutil.get_data(
            'novnc_rocker',
            'templates/%s_snippet.Dockerfile.em' % self.name).decode('utf-8')
        try:
            result = em.expand(snippet, self._env_subs)
        except (NameError, TypeError) as ex:
            raise NameError("Failed to evaluate snippet for %s: %s. \nargs are: %s" % (self.name, ex, self._env_subs))
        return result

    def get_docker_args(self, cli_args):
        return ''

    @staticmethod
    def register_arguments(parser, defaults={}):
        parser.add_argument(name_to_argument(TurboVNC.get_name()),
            action='store_true',
            default=defaults.get(TurboVNC.get_name(), None),
            help="enable TurboVNC")
