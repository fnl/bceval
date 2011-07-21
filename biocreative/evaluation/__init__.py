import logging

from biocreative.configuration import Configuration
from biocreative.evaluation.settings import Defaults

def class_loader(class_name):
    CONFIG = Configuration(Defaults.CONFIG_FILE)
    return __load__(CONFIG.class_path(class_name), class_name)

def __load__(qualified_name, klass):
    logging.debug("dynamically loading %s from %s" % (klass, qualified_name))
    module = __import__(qualified_name)
    components = qualified_name.split('.')
    
    for component in components[1:]:
        module = getattr(module, component)
    
    return getattr(module, klass)
