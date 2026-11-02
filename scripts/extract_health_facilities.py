import osmium, json, sys, collections
src, dst = sys.argv[1], sys.argv[2]
AM = {"hospital","clinic","doctors","health_post"}
feats=[]; cnt=collections.Counter()
class H(osmium.SimpleHandler):
    def keep(self,t):
        a=t.get("amenity"); h=t.get("healthcare")
        return (a in AM) or (h is not None and h!="")
    def props(self,t,kind):
        return {"name":t.get("name") or t.get("name:fr"),"amenity":t.get("amenity"),"healthcare":t.get("healthcare"),"operator":t.get("operator"),"osm":kind}
    def node(self,n):
        if self.keep(n.tags) and n.location.valid():
            feats.append({"type":"Feature","properties":self.props(n.tags,"node/%d"%n.id),"geometry":{"type":"Point","coordinates":[round(n.location.lon,6),round(n.location.lat,6)]}})
    def way(self,w):
        if self.keep(w.tags):
            pts=[(n.lon,n.lat) for n in w.nodes if n.location.valid()]
            if pts:
                x=sum(p[0] for p in pts)/len(pts); y=sum(p[1] for p in pts)/len(pts)
                feats.append({"type":"Feature","properties":self.props(w.tags,"way/%d"%w.id),"geometry":{"type":"Point","coordinates":[round(x,6),round(y,6)]}})
H().apply_file(src, locations=True)
for f in feats: cnt[(f["properties"]["amenity"],f["properties"]["healthcare"])]+=1
json.dump({"type":"FeatureCollection","attribution":"Health facilities: © OpenStreetMap contributors, ODbL 1.0 (Geofabrik extract 2026-10-30).","features":feats},open(dst,"w"),separators=(",",":"))
print("features",len(feats)); 
for k,v in cnt.most_common(15): print(k,v)
