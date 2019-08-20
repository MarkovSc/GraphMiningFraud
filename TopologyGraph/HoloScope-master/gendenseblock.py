import sys
import numpy as np
import random
import numpy.random as nr
import scipy.linalg as sla
from mytools.ioutil import *
from scipy.sparse import coo_matrix

def genEvenDenseBlock(A, B, p):
    m = []
    for i in range(A):
        a = np.random.binomial(1, p, B)
        m.append(a)
    return np.array(m)

def genHyperbolaDenseBlock(A, B, alpha, tau):
    'this is from hyperbolic paper: i^\alpha * j^\alpha > \tau'
    m = np.empty([A, B], dtype=int)
    for i in range(A):
        for j in range(B):
            if (i+1)**alpha * (j+1)**alpha > tau:
                m[i,j] = 1
            else:
                m[i,j] = 0
    return m

def genDiHyperRectBlocks(A1, B1, A2, B2, alpha=-0.5, tau=None, p=1):
    if tau is None:
        tau = A1**alpha * B1**alpha
    m1 = genEvenDenseBlock(A1, B1, p=p)
    m2 = genHyperbolaDenseBlock(A2, B2, alpha, tau)
    M = sla.block_diag(m1, m2)
    return M

def addnosie(M, A, B, p, black=True, A0=0, B0=0):
    v = 1 if black else 0
    for i in range(A-A0):
        a = np.random.binomial(1, p, B-B0)
        for j in a.nonzero()[0]:
            M[A0+i,B0+j]=v
    return M


def injectCliqueCamo(M, m0, n0, p, testIdx):
    (m,n) = M.shape
    M2 = M.copy().tolil()

    colSum = np.squeeze(M2.sum(axis = 0).A)
    colSumPart = colSum[n0:n]
    colSumPartPro = np.int_(colSumPart)
    colIdx = np.arange(n0, n, 1)
    population = np.repeat(colIdx, colSumPartPro, axis = 0)

    for i in range(m0):
        # inject clique
        for j in range(n0):
            if random.random() < p:
                M2[i,j] = 1
        # inject camo
        if testIdx == 1:
            thres = p * n0 / (n - n0)
            for j in range(n0, n):
                if random.random() < thres:
                    M2[i,j] = 1
        if testIdx == 2:
            thres = 2 * p * n0 / (n - n0)
            for j in range(n0, n):
                if random.random() < thres:
                    M2[i,j] = 1
        # biased camo           
        if testIdx == 3:
            print(population)
            colRplmt = random.sample(list(population), int(n0 * p))
            M2[i,colRplmt] = 1

    return M2.tocsc()


def generateProps(rates, times, k, s, t0, tsdiffcands, tsp):

    if len(rates) > 0:
        # rate just in 4 and 4.5 , why ?
        rs = np.random.choice([4, 4.5], size=s)
        if k in rates:
            for r in rs:
                rates[k].append(r)
        else:
            rates[k] = list(rs)
    if len(times) > 0:
        # rate time not fixed ? 
        ts = np.random.choice(tsdiffcands, size=s, p=tsp) + t0
        if k in times:
            for t in ts:
                times[k].append(t)
        else:
            times[k] = list(ts)
    return

def injectFraud2PropGraph(freqfile, ratefile, tsfile, acnt, bcnt, goal, popbd,
                          testIdx = 3, idstartzero=True, re=True, suffix=None,
                         weighted=True, output=True, inject_K=1):
    if not idstartzero:
        print('we do not handle id start 1 yet for ts and rate')
        ratefile, tsfile = None, None

    M = loadedge2sm(freqfile, coo_matrix, weighted=weighted,
                     idstartzero=idstartzero)
    'smax: the max # of multiedge'
    smax = M.data.max() #max freqency
    print(smax)
    print(M.shape)
    if acnt == 0 and re:
        return M, ([], [])
    M2 = M.tolil()
    (m, n) = M2.shape
    rates, times, tsdiffs, t0 = [], [], [], 0
    t0, tsdiffcands,tsp = 0, [], []
    if ratefile is not None:
        rates = loadDictListData(ratefile, ktype=str, vtype=float)
    if tsfile is not None:
        times = loadDictListData(tsfile, ktype=str, vtype=int)
        tsmin, tsmax = sys.maxsize,0
        tsdiffs = np.array([])
        #page[node_id] = [page_time]
        prodts={i:[] for i in range(n)}
        for k,v in times.items():
            k = k.split('-')
            pid = int(k[1])
            prodts[pid] += v
            
        #sort page time list [page_time]
        for pv in prodts.values():
            pv = sorted(pv)
            minv, maxv = pv[0], pv[-1]
            if tsmin > minv:
                tsmin = minv
            if tsmax < maxv:
                tsmax = maxv
            if len(pv)<=2:
                continue
            # cal the time delta with len([page_time]) -1
            vdiff = np.diff(pv)
            'concatenate with [] will change value to float'
            # the pv is sorted , so vdiff is to remove duplicates ts
            # the tsdiffs is all page time diff
            tsdiffs = np.concatenate((tsdiffs, vdiff[vdiff>0]))
        tsdiffs.sort()
        tsdiffs = tsdiffs.astype(int)
    # again remove duplicates and get top 20 page time diff
    tsdiffcands = np.unique(tsdiffs)[:20] #another choice is bincount
    print("ts sample list", tsdiffcands)
    tsp = np.arange(20,dtype=float)+1
    print("max tf time", tsp)
    tsp = 1.0/tsp
    # nomalization time diff nparray
    tsp = tsp/tsp.sum()
    print("tsp", tsp)
    t0 = np.random.randint(tsmin, tsmax,dtype=int)

    colSum = M2.sum(0).getA1()
    colids = np.arange(n, dtype=int)
    # < popbd , find unpopular page
    targetcands = np.argwhere(colSum < popbd).flatten()

    # add inject_K
    targets = [random.sample(list(targetcands), bcnt) for index in range(inject_K)]
    # return the sorted, unique values in ar1 that are not in ar2
    # not unpopular pages
    camocands = np.setdiff1d(colids, np.array(targets).flatten(), assume_unique=True)
    camoprobs = colSum[camocands]/float(colSum[camocands].sum())
    #population = np.repeat(camocands, colSum[camocands].astype(int), axis=0)
    fraudcands = np.arange(m,dtype=int) #users can be hacked( all user can be ?)

    # add inject_K
    fraudsters = [random.sample(list(fraudcands), acnt) for index in range(inject_K)]
    'rating times for one user to one product, multiedge'
    # rating time and rating probability ( just normal?, lognorm ?)
    scands = np.arange(1,smax+1,dtype=int)
    sprobs = []
    numedges = (M>0).sum()
    for s in scands:
        nums = (M==s).sum()
        sprobs.append(float(nums)/numedges)

    # inject near clique
    for index in range(inject_K):
        for j in targets[index]:
            # 2000 can be hacked, only 200 exe, and 200 unpopular page
            # first loop page
            exeusers = random.sample(list(fraudsters[index]), goal)
            for i in exeusers:
                s = np.random.choice(scands, size=1, p=sprobs)[0] if weighted else 1
                if (not weighted) and M2[i,j] > 0:
                    continue
                # why plus s not  = s , M2 ? adj matrix equal a weight number?
                M2[i,j] += s
                k = '{}-{}'.format(i,j)
                generateProps(rates, times, k, s, t0, tsdiffcands,tsp)

        # inject camo
        p = goal/float(acnt)
        for i in fraudsters[index]:
            if testIdx == 1:
                thres = p * bcnt / (n - bcnt)
                for j in camocands:
                    s = np.random.choice(scands, size=1, p=sprobs) if weighted else 1
                    if (not weighted) and M2[i,j] > 0:
                        continue
                    if random.random() < thres:
                        M2[i,j] += s
                        k = '{}-{}'.format(i,j)
                        generateProps(rates, times, k, s, t0, tsdiffcands, tsp)
            if testIdx == 2:
                thres = 2 * p * bcnt / (n - bcnt)
                for j in camocands:
                    s = np.random.choice(scands, size=1, p=sprobs) if weighted else 1
                    if (not weighted) and M2[i,j] > 0:
                        continue
                    if random.random() < thres:
                        M2[i,j] += s
                        k = '{}-{}'.format(i,j)
                        generateProps(rates, times, k, s, t0, tsdiffcands, tsp)
            # biased camo           
            if testIdx == 3:
                colRplmt = np.random.choice(camocands, size=int(bcnt*p),
                                            p=camoprobs)
                #M2[i,colRplmt] = 1
                s = np.random.choice(scands, size=1, p=sprobs) if weighted else 1
                for j in colRplmt:
                    if (not weighted) and M2[i,j] > 0:
                        continue
                    M2[i,j] += s
                    k = '{}-{}'.format(i,j)
                    generateProps(rates, times, k, s, t0, tsdiffcands, tsp)

    if suffix is not None:
        suffix = str(suffix)
    else:
        suffix =''
    if ratefile is not None and output is True:
        saveDictListData(rates, ratefile+'.inject'+suffix)
    if tsfile is not None and output is True:
        saveDictListData(times, tsfile+'.inject'+suffix)
    M2 = M2.tocoo()
    if not weighted:
        M2.data[0:] =1
    if output is True:
        savesm2edgelist(M2.astype(int), freqfile+'.inject'+suffix, idstartzero=idstartzero)
        saveSimpleListData(np.array(fraudsters).flatten(), freqfile+'.trueA'+suffix)
        saveSimpleListData(np.array(targets).flatten(), freqfile+'.trueB'+suffix)
    if re:
        return M2, (np.array(fraudsters).flatten(), np.array(targets).flatten())
    else:
        return

