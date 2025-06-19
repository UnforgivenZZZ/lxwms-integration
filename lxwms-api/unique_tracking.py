labels = []
lb = input("scan label: ")
records = set()
uf = open("./dup.txt", 'w')
dups = set()

def parse_tracking(lb):
    lb = lb.replace('(', '').replace(')', '')[8:]
    formats = []
    i = 0
    for c in lb:
        formats.append(c)
        i+=1
        if i%4 == 0:
            formats.append(' ')
            i = 0
    return ''.join(formats)
            
while lb != str(-1):
    lb = parse_tracking(lb)
    print(lb)
    if lb in records:
        dups.add(lb)
        print(f"!!!!!!!!!! {lb} already existed !!!!!!!!!!")
    else:
        labels.append(str(lb))
        records.add(lb)
    lb = input("scan label: ")


for l in dups:
    uf.write(l+'\n')
