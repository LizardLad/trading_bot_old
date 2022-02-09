import os
import sys
import time
import asset
import config
import logging
import argparse
import multiprocessing
import tensorflow as tf

from training import train_main, eval_main

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d [%(levelname)-8s] [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')

def main():
	argument_help_message = """Put description here"""
	parser = argparse.ArgumentParser(description=argument_help_message)
	parser.add_argument('-m', '--mode', help='Program mode expecting one of [train, (eval, evaluate), (sim_files, simulate_files), (sim_live, simulate_live), trade_live]')
	parser.add_argument('-i', '--input', help='Input file to pass to program mode (train, eval)')
	parser.add_argument('-d', '--dir', help='Input files in directory')
	parser.add_argument('-n', '--new_model', help='Create a new model to train')
	parser.add_argument('-o', '--output', help='Model filepath for output. If not set uses model filepath in config.json')
	args = parser.parse_args()

	multiprocessing.set_start_method('spawn')

	if(args.mode):
		#There are several modes this program can run in
			#Train model
			#Perform model evaluation
			#Simulate trading on test files
			#Simulate trading on live data
			#Trade on live data
		program_mode = str(args.mode).lower()
		if(program_mode == 'train'):
			logging.info('Training model from files')
			train_main(args)
		elif(program_mode == 'eval' or program_mode == 'evaluate'):
			logging.info('Evaluating model from test files')
			eval_main(args)
		elif(program_mode == 'sim_files' or program_mode == 'simulate_files'):
			logging.warning('Simulate files is not fully implemented yet')
			time.sleep(1)
			sys.exit(2)
		elif(program_mode == 'sim_live' or program_mode == 'simulate_live'):
			logging.error('Simulate live is not implemented yet')
			sys.exit(2)
		elif(program_mode == 'trade_live'):
			logging.error('Trade live is not implemented yet')
			sys.exit(2)
		else:
			logging.error('Invalid program mode provided: {}. Expected one of [train, (eval, evaluate), (sim_files, simulate_files), (sim_live, simulate_live), trade_live]'.format(program_mode))
			sys.exit(1)
	else:
		logging.error('No program mode provided. Exiting...')
		sys.exit(1)

if __name__ == '__main__':
	main()
