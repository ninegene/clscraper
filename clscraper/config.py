from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError
import os
import logging
import logging.handlers
import codecs
from utils import mkdir, touch

APP_NAME = 'clscraper'
CRAIGSLIST = 'craigslist'

log = logging.getLogger(__name__)


def load_config():
    potential_dirs = [
        os.path.abspath(os.path.expanduser(os.curdir)),
        os.path.abspath(os.path.expanduser('~')),
        os.path.abspath(os.path.expanduser('~/.config')),
    ]

    potential_files = [d + '/' + APP_NAME + '.conf' for d in potential_dirs]
    conf_file = potential_files[0]

    found_files = SafeConfigParser().read(potential_files)
    parser = SafeConfigParser()

    print 'Potential config files: ', potential_files
    print 'Found config files: ', found_files

    if found_files and len(found_files) > 0:
        conf_file = found_files[0]
    else:
        touch(conf_file)

    base_dir = os.path.join(os.path.dirname(conf_file))
    with codecs.open(conf_file, 'r', encoding='utf-8') as f:
        parser.readfp(f)

    _set_default(parser, CRAIGSLIST, 'sites_url', 'http://www.craigslist.org/about/sites')
    _set_default(parser, APP_NAME, 'cache_dir', mkdir(os.path.join(base_dir, 'clscraper/cache')))
    _set_default(parser, APP_NAME, 'log_dir', mkdir(os.path.join(base_dir, 'clscraper/log')))

    with codecs.open(conf_file, 'w', encoding='utf-8') as f:
        parser.write(f)

    print 'conf: conf file is ', conf_file
    print 'conf: base dir is ', conf_file

    return parser


def _set_default(parser, section, key, default_value):
    try:
        value = parser.get(section, key)
        # print 'conf: get key:', key, value
        return value
    except NoSectionError:
        # print 'conf: add section', section
        # print 'conf: add key', section, key, default_value
        parser.add_section(section)
        parser.set(section, key, default_value)
        return default_value
    except NoOptionError:
        # print 'conf: add key', section, key, default_value
        parser.set(section, key, default_value)
        return default_value


def initialize_logger(log_dir=None, logfile_prefix='my_app'):
    log_dir = log_dir or '/var/log/'
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)  # NOTSET to log all levels messages

    details_formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)s %(message)s')
    simple_formatter = logging.Formatter("%(levelname)s: %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    error_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, logfile_prefix + ".error.log"),
        maxBytes=1024,
        backupCount=10)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(details_formatter)
    logger.addHandler(error_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, logfile_prefix + ".all.log"),
        maxBytes=1024,
        backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(details_formatter)
    logger.addHandler(file_handler)


config = load_config()
SITES_URL = config.get(CRAIGSLIST, 'sites_url')
CACHE_DIR = config.get(APP_NAME, 'cache_dir')
LOG_DIR = config.get(APP_NAME, 'log_dir')

initialize_logger(LOG_DIR, APP_NAME)
