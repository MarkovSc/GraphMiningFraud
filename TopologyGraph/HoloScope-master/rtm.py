#!/usr/bin/env python
# encoding: utf-8

import sys
import os

def runProduct(fin,fout,generator,n):
	for line in fin:
		vals = line.split()
		for term in generator:
			for i in range(0,3):
				v = int(term[i]) * int(n[i]) + int(vals[i])
				fout.write(str(v) + "\t")
			fout.write("\n")

	fin.close()
	fout.close()

def makeMinSize(fn,g,nx,ny,nz,mx,my,mz):

	temp = fn.split(".")
	fnt = temp[0]
	na = fnt.split("_")
	print(na)

	while ( int(na[0]) <= mx or int(na[1]) <= my or int(na[2]) <= mz ):
		fin = open(fn, 'r')

		fn = str(int(na[0])*nx) + "_" + str(int(na[1])*ny) + "_" + str(int(na[2])*nz) + ".txt" 
		fout = open(fn, 'w')

		runProduct(fin,fout,g,na)

		temp = fn.split(".")
		fnt = temp[0]
		na = fnt.split("_")
		print(na)


def runOnce(fn,g,nx,ny,nz):
	fin = open(fn, 'r')

	temp = fn.split(".")
	fn = temp[0]
	na = fn.split("_")
	print(na)

	fn_out = str(int(na[0])*nx) + "_" + str(int(na[1])*ny) + "_" + str(int(na[2])*nz) + ".txt"
	fout = open(fn_out, 'w')

	runProduct(fin,fout,g,na)


def main():

	nx = 12
	ny = 10
	nz = 14
	generator = [ ]

	generator.append([0,1,3])
	generator.append([0,7,6])

	generator.append([1,4,0])
	generator.append([1,9,7])

	generator.append([2,0,5])

	generator.append([3,6,13])
	generator.append([3,2,2])

	generator.append([4,3,4])

	generator.append([5,1,8])
	generator.append([5,6,11])

	generator.append([6,0,1])

	generator.append([7,5,9])

	generator.append([8,3,10])
	generator.append([8,2,3])

	generator.append([9,5,6])

	generator.append([10,7,0])

	generator.append([11,8,12])


	print(sys.argv)
	if len(sys.argv) > 1:
		fn = sys.argv[1]
	else:
		print("No file specified")
		return

	#runOnce(fn,generator,nx,ny,nz)
	makeMinSize(fn,generator,nx,ny,nz,10000,10000,5)




if __name__ == '__main__':
	main()

