
# General python modules 
import os, sys 
import logging

# Luigi
import luigi
import sciluigi as sl
from subprocess import call

# Streamm
import simulation

log = logging.getLogger('sciluigi-interface')

# ------------------------------------------------------------------------
# Workflow class(es)
# ------------------------------------------------------------------------

class exgaussian(sl.WorkflowTask):

    def workflow(self):
        
        writecom = self.new_task('writecom', WRITEcom)
        rung09 = self.new_task('rung09', RUNg09)
        analyzelog = self.new_task('analyzelog', AnalyzeLOG)
        
        rung09.in_com = writecom.out_com
        analyzelog.in_log = rung09.out_log
        
        return analyzelog

class WRITEcom(sl.Task):
    
    def out_com(self):
        return sl.TargetInfo(self,'/scratch/tkemper/streamm_test1/thiopheneHF.com')
        
class RUNg09(sl.Task):
    in_com = None
    
    def out_log(self):
        return sl.TargetInfo(self,'/scratch/tkemper/streamm_test1/thiopheneHF_ex2.log')
    
    def run(self):
        cmd = 'g09 < ' + self.in_com().path + '  > ' + self.out_log().path 
        log.info("COMMAND TO EXECUTE: " + cmd)
        call(cmd, shell=True)

class AnalyzeLOG(sl.Task):
    in_log = None

    def out_dat(self):
        return sl.TargetInfo(self,'/scratch/tkemper/streamm_test1/thiopheneHF_ex2.dat')

    def run(self):
        sim_i = simulation.Gaussian("example2")
        sim_i.analyze_log(self.in_log().path)

        print " homo ",sim_i.alpha_energies[sim_i.N_alpha_occ-1]
        print " lumo ",sim_i.alpha_energies[sim_i.N_alpha_occ]

        sim_i.write_dat( self.out_dat().path )
        
        
# Run this file as script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    luigi.run(local_scheduler=True, main_task_cls=exgaussian)
