from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError
import os
import logging
import logging.handlers
import codecs
from utils import touch
from logconf import initialize_logger

APP_NAME = 'clscraper'

log = logging.getLogger(__name__)


def load_config():
    potential_dirs = [
        os.path.abspath(os.path.expanduser(os.curdir)),
        os.path.abspath(os.path.expanduser('~')),
        os.path.abspath(os.path.expanduser('~/.config/' + APP_NAME)),
        ]

    potential_files = [base + '/' + APP_NAME + '.conf' for base in potential_dirs]
    conf_file = potential_files[0]

    found_files = SafeConfigParser().read(potential_files)
    parser = SafeConfigParser()

    print 'Potential config files: ', potential_files
    print 'Found config files: ', found_files

    if found_files and len(found_files) > 0:
        conf_file = found_files[0]
    else:
        touch(conf_file)

    print 'conf file is ', conf_file

    _set_defaults(parser, conf_file)

    with codecs.open(conf_file, 'w', encoding='utf-8') as f:
        parser.write(f)

    return parser


def _set_defaults(parser, conf_file):
    base_dir = os.path.dirname(conf_file)
    print 'conf: base dir is ', base_dir

    with codecs.open(conf_file, 'r', encoding='utf-8') as f:
        parser.readfp(f)

    _set_default(parser, "craigslist", 'sites_url', 'http://www.craigslist.org/about/sites')

    _set_default(parser, APP_NAME, 'cache_dir', os.path.join(base_dir, APP_NAME, 'cache'))
    _set_default(parser, APP_NAME, 'log_dir', os.path.join(base_dir, APP_NAME, 'logs'))


def _set_default(parser, section, key, default_value):
    try:
        value = parser.get(section, key)
        print 'conf: get key:', key, value
        return value
    except NoSectionError:
        print 'conf: add section', section
        print 'conf: add key', section, key, default_value
        parser.add_section(section)
        parser.set(section, key, default_value)
        return default_value
    except NoOptionError:
        print 'conf: add key', section, key, default_value
        parser.set(section, key, default_value)
        return default_value


config = load_config()
CL_SITES_URL = config.get("craigslist", 'sites_url')

CACHE_DIR = config.get(APP_NAME, 'cache_dir')
LOG_DIR = config.get(APP_NAME, 'log_dir')

initialize_logger(LOG_DIR, APP_NAME)
