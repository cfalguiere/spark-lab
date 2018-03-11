#-*- coding: utf-8 -*-
"""App commons"""
from __future__ import print_function


class AppContext:
    def __init__(self, name='App'):
        self.name = name
        self.status = -1
        self.attributes = {}
        self.configuration = None
        self.steps = []

    def __str__(self):
        return self.name


# -----------------

import datetime
import traceback
from sch.common.exceptions import ExecutionError
from sch.common.rutils import RScript
from sch.init.configuration import AppConfiguration

class XAppContext:
    def __init__(self):
        self.status = -1
        self.attributes = {}
        self.configuration = None
        self.steps = []

    def add_attribute(self, attributeName, attributeValue):
        self.attributes[attributeName]=attributeValue

    def get_attribute(self, attributeName):
        return self.attributes[attributeName]

    def get_configuration(self):
        return self.configuration

    def set_configuration(self, configuration):
        self.configuration = configuration

    def new_step(self, stepName):
        step = AppStep(stepName, self)
        self.steps.append(step)
        return step

    def new_configuration(self, cfgPath):
        self.configuration = AppConfiguration(cfgPath, self)
        return self.configuration

    def report(self):
        print( '===========================================================')
        print( '|')
        print( '| REPORT')
        print( '|')
        print( '| Number of steps: %s' % len(self.steps) )
        for step in self.steps:
            print( '| {0}'.format( step.report ) )
        print( '===========================================================')

    def set_status(self, aStatus):
        self.status = aStatus

    def get_status(self):
        return  self.status

    def __enter__(self):
        self.start = datetime.datetime.now()
        print( "INFO - Starting app"  )
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
       self.end = datetime.datetime.now()
       elapsed = self.end  - self.start
       if exc_type == None:
          self.status = "app Completed"
       else:
          traceback.print_exception(exc_type, exc_value, exc_traceback, 30)
          self.status = "Aborted"
       self.report()
       print( 'INFO - End of App')

    def __str__(self):
        return 'Job status is {0}'.format(self.status)


class XAppStep:
    def __init__(self, stepName, theAppContext):
        self.stepName = stepName
        self.theAppContext = theAppContext
        self.status = "Not Started"
        self.report = None

    def __enter__(self):
        self.start = datetime.datetime.now()
        self.status = "Started"
        print( '| ')
        print( '===========================================================')
        print( "| STEP %s is starting" % self.stepName )
        print( '-----------------------------------------------------------')
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
       print( '-----------------------------------------------------------')
       self.end = datetime.datetime.now()
       elapsed = self.end  - self.start
       if exc_type == None:
          self.status = "Completed"
       else:
          print( 'ERROR - in step %s' %  (self.stepName) )
          traceback.print_exception(exc_type, exc_value, exc_traceback, 30)
          self.status = "Aborted"
       print( "| STEP {0} - {1} in {2}.{3} seconds".format (self.stepName, self.status, elapsed.seconds, elapsed.microseconds))
       print( '===========================================================')
       print( '| ')

       #time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    def rscript(self):
        return  RScript(self.theAppContext, self)


    def get_status(self):
       return self.status

    def __del__(self):
        print("__del__")

    def __repr__(self):
        return self.stepName

    def __str__(self):
        return self.stepName


