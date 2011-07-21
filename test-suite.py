#!/usr/bin/env python
# encoding: utf-8

# GNU GPL LICENSE
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; latest version thereof,
# available at: <http://www.gnu.org/licenses/gpl.txt>.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this module; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA

"""test-suite.py

Test suit accompanying the BioCreative evaluation script.

Created by Florian Leitner on 2009-10-14 at CNIO.
Copyright (c) 2009 Florian Leitner. All rights reserved.
License: GNU Public License, latest version.
"""

import unittest

from biocreative.configuration import Configuration
from biocreative.evaluation.settings import Defaults

def build_suite_for(names, suite=None):
    if suite is None:
        suite = unittest.TestSuite()
    
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromNames(names))
    return suite

def main():
    config = Configuration(Defaults.CONFIG_FILE)
    behaviour_suite = build_suite_for(config.behaviour_test_names())
    spec_suite = build_suite_for(config.spec_test_names())
    runner = unittest.TextTestRunner(verbosity=0)
    print "Unit Tests"
    runner.run(spec_suite)
    print "\nBehaviour Tests"
    runner.run(behaviour_suite)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())