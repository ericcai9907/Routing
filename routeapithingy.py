import argparse
import json_pathfinder as j_path 
import sys
import json



parser = argparse.ArgumentParser()
parser.add_argument('-i', "--input", 
	type = str, default = '33.63,-117.84,33.65,-117.81',
	help = 'Input: string in format lat1,lon1,lat2,lon2', required = True )


def Router(inpt):
	coords = inpt.split(',')
	coords_list = [(float(coords[0]), float(coords[1])), (float(coords[2]), float(coords[3]))]
	route = j_path.pathfinder(coords_list)

	return route


if (__name__ == '__main__'):
	args, unknown = parser.parse_known_args()
	input = args.input
	output = Router(input)
	print (output)
	sys.stdout.flush()


