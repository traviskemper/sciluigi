import logging
import luigi
import sciluigi as sl
from subprocess import call


import os, sys 

log = logging.getLogger('sciluigi-interface')

# ------------------------------------------------------------------------
# Workflow class(es)
# ------------------------------------------------------------------------

class exgaussian(sl.WorkflowTask):

    def workflow(self):
        
        writecom = self.new_task('writecom', WRITEcom)
        rung09 = self.new_task('rung09', RUNg09)
        
        rung09.in_com = writecom.out_com
        
        return rung09

class WRITEcom(sl.Task):
    
    def out_com(self):
        return sl.TargetInfo(self,'/scratch/tkemper/streamm_test1/thiopheneHF.com')
        
class RUNg09(sl.Task):
    in_com = None
    
    def out_log(self):
        return sl.TargetInfo(self,'/scratch/tkemper/streamm_test1/thiopheneHF_ex1.log')
    
    def run(self):
        cmd = 'g09 < ' + self.in_com().path + '  > ' + self.out_log().path 
        log.info("COMMAND TO EXECUTE: " + cmd)
        call(cmd, shell=True)


# Run this file as script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    luigi.run(local_scheduler=True, main_task_cls=exgaussian)
