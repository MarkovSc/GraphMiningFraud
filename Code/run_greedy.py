# runs the greedy algorithm. first argument is path to data file. second argument is name to save 
# pickle containing results. 
import time
start_time = time.time()
from greedy import *
import sys
M = readData(sys.argv[1])
print("finished reading data: shape = ", M.shape, " @ ", time.time() - start_time)

# (m, n) = (500, 500)
# M = M[0:m, 0:n]
# M[0:20, 0:20] = 1
# M2 = M.toarray().astype(int)
# print np.transpose(np.nonzero(M2))
# np.savetxt('example.txt', np.transpose(np.nonzero(M2)), fmt='%d')

# M, rowFilter, colFilter = subsetAboveDegree(M, int(sys.argv[3]), int(sys.argv[4]))
# filter_name = "output/%s_%s_%s_filter.pickle" % (sys.argv[2], sys.argv[3], sys.argv[4])
# pickle.dump((rowFilter, colFilter), open(filter_name, "wb" ))
# print "finished subsetting: shape = ", M.shape, " @ ", time.time() - start_time
# subset_filepath = '%s_%s_%s.txt' % (sys.argv[2], sys.argv[3], sys.argv[4])
# pickle.dump(M, open(subset_filepath, "wb"))
# np.savetxt(subset_filepath, M.nonzero().transpose(), fmt='%i')

print("finished writing data", " @ ", time.time() - start_time)
lwRes = logWeightedAveDegree(M)
print(lwRes)
np.savetxt("%s.rows" % (sys.argv[2], ), np.array(list(lwRes[0][0])), fmt='%d')
np.savetxt("%s.cols" % (sys.argv[2], ), np.array(list(lwRes[0][1])), fmt='%d')
print("score obtained is ", lwRes[1])
print("done @ ", time.time() - start_time)
