import sys, os, re, math

dir = sys.argv[1]
i = 0
subtot = {}
counts = {}
for d in os.listdir(dir)[0:15]:
    print d
    m = re.match('wiki_[A-Z]{2}',d) 
    if not m: continue
    text = open(dir + '/' + d)
    f = text.read()
    text.close()
    for line in f.lower().split('\n'):
        ns = re.match('(nsubj[a-z]*)\((.+)\-[0-9]*,\s*(.+)-[0-9]\)',line)
        if ns: 
        #    print line
            rel = ns.group(1)
            head = ns.group(2)
            if rel == 'nsubjpass': head = head + '_P'
            arg = ns.group(3)
            if not counts.has_key(arg): counts[arg] = {}
            if not counts[arg].has_key(head):
                counts[arg][head] = 1
            else: counts[arg][head] += 1
            if not subtot.has_key(arg): subtot[arg] = 1
            else: subtot[arg] += 1

ents = {}
for sub,vbs in counts.items():
    ents[sub] = 0
    highprob = 0
    for vb,ct in vbs.items():
        prob = float(ct)/subtot[sub]
        term = prob * math.log((1/float(prob)),2)
        ents[sub] += term
        if prob > 0.5 and subtot[sub] > 5:
            print sub + ', ' + vb + ', ' + str(prob)
            highprob = 1
    if highprob == 1:
        print sub + ' ent: ' + str(ents[sub]) + ', subcount: ' + str(subtot[sub])
        print counts[sub]
