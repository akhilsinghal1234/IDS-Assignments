import numpy as np

def not_in_var(vars_,v):
  for var in vars_:
    if var[0] == v:
      return False
  return True

def find_ts(id,tx_id,ts):
    for u,v in zip(tx_id,ts):
        if u == id:
            return v

def new_v(vars_,v):
    new_ver = 0
    for var in vars_:
        if var[0] == v and var[3] > new_ver:
            new_ver = var[3]
    return new_ver+1

def find_version(vars_, ts_, var, tx_id, ts,id):					# for read-only
    max_ts, val, version = 0,0,0
    for v in vars_:
        if v[0] == var and v[2] <= ts_ and v[2] >= max_ts:
            max_ts = v[2]
            version = v[3]

    for v in vars_:
        if v[0] == var and v[2] == max_ts and v[3] == version:
            v[1] = ts_
            print('var read:',v,' by t',id,sep='')

def find_version_w(vars_, ts_, var, tx_id, ts,id):					# for read-only
    max_ts, val, version, rts, wts = 0,0,0,0,0
    for v in vars_:
        if v[0] == var and v[2] <= ts_ and v[2] >= max_ts:
            max_ts = v[2]
            version = v[3]
            rts = v[1]

    wts = max_ts
    if ts_ < rts:
        print('Transaction t',id,' rolled back as timestamp ' ,ts_,' < rts ',rts,sep='')
        rolled_back.append(id)
        return

    if ts_ == wts:
        print('Transaction t',id,'overwrites',var,version)

    ver = new_v(vars_,var)
    print('var written:',[var,ts_,ts_,ver],' by t',id,sep='')
    vars_.append([var,ts_,ts_,ver])

rolled_back = []
tx_id,t,ts = [],0,[]
n = int(input('number of transactions\n'))
for i in range(n):
    t = input()
    tx_id.append(int(t[-1:]))
    ts.append(int(input()))

var = []     # var, rts, wts, version
op = input()
while(op != '0'):
    if op[0] == 'c' and op[1] not in rolled_back:
        print('Transaction',op[1],'committed')
        op = input()
        continue
    if op[1] not in rolled_back:
        if not_in_var(var,op[2]):
            var.append([op[-1:],1,0,0])

        if op[0] == 'r':                    # if write operation
            ts_ = find_ts(int(op[1]), tx_id, ts)
            find_version(var, ts_, op[-1:], tx_id, ts,op[1])

        if op[0] == 'w':                    # if write operation
            ts_ = find_ts(int(op[1]), tx_id, ts)        # ts of that tx
            find_version_w(var, ts_, op[-1:], tx_id, ts,op[1])
    op = input()
print(var)
