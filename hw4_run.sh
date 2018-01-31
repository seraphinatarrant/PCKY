#!/bin/sh

#hw4_run.sh
treebank_filename=$1 #data/parses.train
output_PCFG_file=$2 #hw4_trained.pcfg
test_sentence_filename=$3 #data/sentences.txt
baseline_parse_output_filename=$4 #parses_base.out
input_PCFG_file=$5 #PCKY/hw4_improved.pcfg  -output of improved process, second input to parser
improved_parse_output_filename=$6
baseline_eval=$7
improved_eval=$8

#without improvement 
sh hw4_topcfg.sh $treebank_filename $output_PCFG_file

#cky on non-improved - hw4parser calls example_cky.py
sh hw4_parser.sh $output_PCFG_file $test_sentence_filename $baseline_parse_output_filename

#with improvement 
sh hw4_improved_induction.sh $treebank_filename $input_PCFG_file

#cky on non-improved
sh hw4_parser.sh $input_PCFG_file $test_sentence_filename $improved_parse_output_filename

#run evalb on non-improved
#dropbox/17-18/571/hw4/tools/evalb -p dropbox/17-18/571/hw4/tools/COLLINS.prm dropbox/17-18/571/hw4/data/parses.gold $baseline_parse_output_filename

#run evalb on improved
#dropbox/17-18/571/hw4/tools/evalb -p dropbox/17-18/571/hw4/tools/COLLINS.prm dropbox/17-18/571/hw4/data/parses.gold $improved_parse_output_filename

#./hw4_run.sh data/parses.train PCKY/hw4_trained.pcfg data/sentences.txt PCKY/parses_base.out PCKY/hw4_improved.pcfg PCKY/parses_improved.out PCKY/parses_base.eval PCKY/parses_improved.eval
