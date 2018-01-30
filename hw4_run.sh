#!/bin/sh
#without improvement 
sh hw4_topcfg.sh data/parses.train hw4_trained.pcfg

#with improvement 
sh hw4_improved_induction.sh data/parses.train hw4_improved.pcfg