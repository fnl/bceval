"""configuration

Loads configuration files and provides access to their options and values
in various ways.

Created by Florian Leitner on 2009-11-19.
Copyright (c) 2009 CNIO. All rights reserved.
"""

import logging
import re
import ConfigParser

class Singleton(type):
    "Singleton pattern impl."
    
    def __init__(mcs, name, bases, dic):
        super(Singleton, mcs).__init__(name, bases, dic)
        mcs.__instance = None
    
    def __call__(mcs, *args, **kw):
        if mcs.__instance is None:
            mcs.__instance = super(Singleton, mcs
                                   ).__call__(*args, **kw)
        return mcs.__instance
    

class Configuration(object):
    "Retrieve class and module names."
    
    __metaclass__ = Singleton
    
    # option names not specifying the class a module provides
    # all other "option: value" items have the format "module_name: ClassName"
    SPECIAL_OPTIONS = [
        'root', 'modules', 'spec_test', 'behaviour_tests'
    ]
    
    def __init__(self, configuration_file_path):
        self.configuration_file_path = configuration_file_path
        self.logger = logging.getLogger("Configuration")
        parser = ConfigParser.ConfigParser()
        self.logger.info(
            "loading configuration from '%s'" % configuration_file_path
        )
        parser.readfp(open(configuration_file_path))
        self.config = parser
        self._reverse_class_path = self._reverse_lookup_dict()
    
    def _reverse_lookup_dict(self):
        reverse = dict()
        self.logger.debug("creating a reverse lookup dictionary:")
        
        for package in self.config.sections():
            root_path = self._get_root(package)
            
            for module, class_name in self.config.items(package):
                if module in Configuration.SPECIAL_OPTIONS:
                    continue
                elif class_name.find(',') == -1:
                    class_names = [class_name]
                else:
                    class_names = re.split('\s*,\s*', class_name)
                
                for name in class_names:
                    reverse[name] = "%s.%s.%s" % (
                        root_path, package, module
                    )
                    self.logger.debug(
                        "%s => %s" % (name, reverse[name])
                    )
        
        return reverse
    
    def class_path(self, class_name):
        "Return the fully qualified module path for a class."
        try:
            return self._reverse_class_path[class_name]
        except KeyError:
            raise ValueError("unknown class %s" % class_name)
    
    def module_path(self, package, module):
        "Return the fully qualified path for a module."
        root_path = self._get_root(package)
        
        if self.config.has_option(package, module):
            return "%s.%s.%s" % (root_path, package, module)
        else:
            raise ValueError("unknown module %s for package %s" % (
                module, package
            ))
    
    def class_names(self, package, module):
        "Return a list of class names provided by that package's module."
        try:
            return self._get_list(package, module)
        except ConfigParser.NoSectionError:
            raise ValueError("unknown package %s" % package)
        except ConfigParser.NoOptionError:
            raise ValueError("unknown module %s for package %s" % (
                module, package
            ))
    
    def class_name(self, package, module):
        """Return the fully qualified name of the class provided by that
        package's module if that module provides only one class.
        """
        module_path = self.module_path(package, module)
        class_name = self.config.get(package, module)
        
        if class_name.find(',') > -1:
            raise ValueError("%s provides multiple classes" % (
                module_path
            ))
        
        root_path = self.config.get(package, 'root')
        return "%s.%s" % (module_path, class_name)
    
    def behaviour_test_names(self, *packages):
        """Return the fully qualified names of behaviour test classes for the
        given packages (or all).
        """
        return self._test_names_helper(self._get_behaviour_tests, *packages)
    
    def spec_test_names(self, *packages):
        """Return the fully qualfied names of the spec test classes for the
        given packages (or all).
        """
        return self._test_names_helper(self._get_spec_tests, *packages)
    
    def _test_names_helper(self, get_list, *packages):
        package_list = packages if packages else self.config.sections()
        names = list()
        
        for pack in package_list:
            if self.config.has_section(pack):
                names.extend(get_list(pack))
            else:
                raise ValueError("unknown package %s" % pack)
        
        return names
    
    def _get_module_classes(self, package):
        return self._get_qualified_names(
            package, 'modules', "%s.%s.%s.%s"
        )
    
    def _get_behaviour_tests(self, package):
        return self._get_qualified_names(
            package, 'behaviour_tests', "%s.%s.%s.tests.%sTests"
        )
    
    def _get_spec_tests(self, package):
        return self._get_qualified_names(
            package, 'spec_test', "%s.%s.tests.%s.%sTest"
        )
    
    def _get_qualified_names(self, package, option, format_path):
        qualified_names = list()
        
        if self.config.has_option(package, option):
            root = self._get_root(package)
            
            for module in self._get_list(package, option):
                for class_name in self.class_names(package, module):
                    qualified_names.append(
                        format_path % (root, package, module, class_name)
                    )
        else:
            self.logger.debug(
                "package %s has no option %s" % (package, option)
            )
        
        return qualified_names
    
    def _get_root(self, package):
        try:
            return self.config.get(package, 'root')
        except ConfigParser.NoSectionError:
            raise ValueError("unknown package %s" % package)
    
    def _get_list(self, section, option):
        option = self.config.get(section, option)
        
        if len(option) == 0:
            return []
        
        return re.split('\s*,\s*', option)
    
