import json,sys,gzip
src,dst=sys.argv[1],sys.argv[2]; TOL=float(sys.argv[3]); MINA=float(sys.argv[4])
def area(r):
    a=0
    for i in range(len(r)-1): a+=r[i][0]*r[i+1][1]-r[i+1][0]*r[i][1]
    return abs(a)/2
def dp(pts,tol):
    n=len(pts); keep=[False]*n; keep[0]=keep[-1]=True; st=[(0,n-1)]
    while st:
        i,j=st.pop()
        if j<=i+1: continue
        x1,y1=pts[i]; x2,y2=pts[j]; dx,dy=x2-x1,y2-y1; L=dx*dx+dy*dy; md=-1; mi=i
        for k in range(i+1,j):
            x,y=pts[k]
            if L==0: d=(x-x1)**2+(y-y1)**2
            else:
                t=max(0,min(1,((x-x1)*dx+(y-y1)*dy)/L)); d=(x-x1-t*dx)**2+(y-y1-t*dy)**2
            if d>md: md=d; mi=k
        if md>tol*tol: keep[mi]=True; st+=[(i,mi),(mi,j)]
    return [p for p,k in zip(pts,keep) if k]
d=json.load(open(src)); before=after=0
for f in d["features"]:
    out=[]
    for poly in f["geometry"]["coordinates"]:
        if area(poly[0])<MINA: continue
        rings=[]
        for i,r in enumerate(poly):
            before+=len(r)
            if i>0 and area(r)<MINA: continue
            s=dp(r,TOL)
            if len(s)<4: 
                if i==0: rings=None; break
                continue
            s=[[round(x,4),round(y,4)] for x,y in s]; s[-1]=s[0]; rings.append(s); after+=len(s)
        if rings: out.append(rings)
    f["geometry"]["coordinates"]=out
    f["properties"].pop("attribution",None)
json.dump(d,open(dst,"w"),separators=(",",":"))
print("vertices",before,"->",after,"| bytes",len(open(dst,"rb").read()),"| gz",len(gzip.compress(open(dst,"rb").read(),9)))
