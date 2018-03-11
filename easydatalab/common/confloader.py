#-*- coding: utf-8 -*-
from __future__ import print_function

import ConfigParser

from easydatalab.common.validator import PathValidator
from easydatalab.common.exceptions import ConfigurationError

class AppConfigurationLoader:
      def __init__(self):
            self.settings = None
            self.parameters = {}

      def load(self, path):
          cv = PathValidator()
          if  not cv.check_path_for_existence( path ):
              raise ConfigurationError('PATH', 'Config file not found at %s' % path)

          self.settings = ConfigParser.SafeConfigParser()
          self.settings.read(path)

          return self.settings