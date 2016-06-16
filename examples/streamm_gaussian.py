import logging
import luigi
import sciluigi as sl
from subprocess import call


import os, sys 
import project, buildingblock, simulation

log = logging.getLogger('sciluigi-interface')

# ------------------------------------------------------------------------
# Workflow class(es)
# ------------------------------------------------------------------------

class MyWorkflow(sl.WorkflowTask):

    def workflow(self):
        rawdata = self.new_task('rawdata', RawData)
        atot = self.new_task('atot', AToT)

        atot.in_data = rawdata.out_rawdata

        return atot

# ------------------------------------------------------------------------
# Task classes
# ------------------------------------------------------------------------

class RawData(sl.ExternalTask):

    def out_rawdata(self):
        return sl.TargetInfo(self, '/scratch/tkemper/streamm_test1/thiopheneHF.com')


class AToT(sl.Task):
    in_data = None

    def out_replatot(self):
        return sl.TargetInfo(self, self.in_data().path + '.log')

    # ------------------------------------------------

    def run(self):
        cmd = 'g09 < ' + self.in_data().path + '  > ' + self.out_replatot().path
        log.info("COMMAND TO EXECUTE: " + cmd)
        call(cmd, shell=True)


# Run this file as script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    print " check import "
    luigi.run(local_scheduler=True, main_task_cls=MyWorkflow)
