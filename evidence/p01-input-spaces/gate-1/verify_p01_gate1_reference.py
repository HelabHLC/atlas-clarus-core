#!/usr/bin/env python3
"""ATLAS Clarus P01 Gate-1 independent verifier (stdlib only)."""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path

METHOD_ID="ATLAS_CLARUS_P01_GATE1_REFERENCE_VERIFIER"
METHOD_VERSION="0.1.1"
MANIFEST_SHA="7a887316eac2aa1959459c4a6339502bf324ff3c2213a6e26650fac03bb061bf"
GAMUT="IN_DECLARED_SOURCE_RGB_GAMUT"
GAMUT_DEF=("The encoded uint8 RGB triplet is within the declared source encoding range; "
           "this is not destination, device, print, ICC-output, or production gamut evidence.")
SPACES={
"sRGB":{"case":"P01-A","route":"NORMATIVE","gate2":True,
"p":((.64,.33),(.30,.60),(.15,.06)),"w":(.3127,.3290),"wn":"D65","tol":5e-5,
"transfer":"sRGB inverse OETF: E<=0.04045 -> E/12.92; else ((E+0.055)/1.055)^2.4",
"ref":{"title":"ICC Three Component Color Encoding Registry — sRGB","definition":"IEC 61966-2-1:1999",
"section":"ENCODING CHARACTERISTICS: RGB primaries, component transfer function, D65 white point",
"url":"https://registry.color.org/rgb-registry/srgb"}},
"AdobeRGB(1998)":{"case":"P01-B","route":"SHADOW","gate2":False,
"p":((.64,.33),(.21,.71),(.15,.06)),"w":(.3127,.3290),"wn":"D65","tol":5e-6,
"transfer":"inverse encoding: E^2.19921875",
"ref":{"title":"Adobe RGB (1998) Color Image Encoding","definition":"Adobe RGB (1998)",
"section":"4.3.5.3 Converting RGB to normalized XYZ values; ICC registry transfer gamma 2.19921875",
"url":"https://www.adobe.com/digitalimag/pdfs/AdobeRGB1998.pdf"}},
"ROMM_RGB":{"case":"P01-C","route":"SHADOW","gate2":False,
"p":((.7347,.2653),(.1596,.8404),(.0366,.0001)),"w":(.3457,.3585),"wn":"D50","tol":5e-5,
"transfer":"inverse encoding: E<0.031248 -> E/16; else E^1.8",
"ref":{"title":"ICC ROMM RGB characterization","definition":"ISO 22028-2:2013",
"section":"ROMMRGB.pdf: primaries, D50 white, precise nonlinear encoding, normalized primary tristimulus values",
"url":"https://www.color.org/ROMMRGB.pdf"}}}
STEPS=["G1.0_VALIDATE_MANIFEST_INTEGRITY","G1.1_VALIDATE_CASE_AND_CHANNEL_ENCODING",
"G1.2_VALIDATE_DECLARED_INPUT_SPACE","G1.3_RESOLVE_CANONICAL_CONVERSION_PATH",
"G1.4_RECONSTRUCT_COLORIMETRIC_STATE","G1.5_RECORD_GAMUT_AND_CLIP_DIAGNOSTICS",
"G1.6_EMIT_GATE1_EVIDENCE","G1.7_DECIDE_GATE1_STATUS"]
FILES={"P01-A":"P01-A_Gate-1_Evidence_v0.1.json","P01-B":"P01-B_Gate-1_Evidence_v0.1.json",
"P01-C":"P01-C_Gate-1_Evidence_v0.1.json"}

def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(1<<20),b""): h.update(b)
 return h.hexdigest()

def inv(m):
 a,b,c=m[0];d,e,f=m[1];g,h,i=m[2]
 q=a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
 return [[(e*i-f*h)/q,(c*h-b*i)/q,(b*f-c*e)/q],
 [(f*g-d*i)/q,(a*i-c*g)/q,(c*d-a*f)/q],
 [(d*h-e*g)/q,(b*g-a*h)/q,(a*e-b*d)/q]]

def mv(m,v): return [sum(m[r][k]*v[k] for k in range(3)) for r in range(3)]

def matrix(p,w):
 cols=[(x/y,1,(1-x-y)/y) for x,y in p]
 P=[[cols[c][r] for c in range(3)] for r in range(3)]
 x,y=w; S=mv(inv(P),(x/y,1,(1-x-y)/y))
 return [[P[r][c]*S[c] for c in range(3)] for r in range(3)]

def dec(s,e):
 if s=="sRGB": return e/12.92 if e<=.04045 else ((e+.055)/1.055)**2.4
 if s=="AdobeRGB(1998)": return e**2.19921875
 if s=="ROMM_RGB": return e/16 if e<.031248 else e**1.8
 raise KeyError(s)

def reconstruct(s,rgb):
 e=[x/255 for x in rgb]; lin=[dec(s,x) for x in e]; M=matrix(SPACES[s]["p"],SPACES[s]["w"])
 xyz=mv(M,lin); sm=sum(xyz); xyy=(xyz[0]/sm,xyz[1]/sm,xyz[1])
 return e,lin,M,xyz,xyy

def close(a,b,t): return math.isfinite(float(a)) and abs(float(a)-b)<=t

def check_record(path,vsha):
 r=json.load(open(path,encoding="utf-8")); err=[]; s=r.get("input_space")
 if s not in SPACES: return r.get("case_id",path.stem),["unsupported input_space"],None
 c=SPACES[s]
 def req(ok,msg):
  if not ok: err.append(msg)
 req(r.get("case_id")==c["case"],"case_id"); req(r.get("route_class")==c["route"],"route_class")
 mb=r.get("manifest_binding",{}); req(mb.get("manifest_sha256")==MANIFEST_SHA and mb.get("manifest_status")=="FROZEN","manifest_binding")
 req(r.get("gate1_status")=="PASS","gate1_status")
 req(r.get("gamut_status")==GAMUT and r.get("gamut_status_definition")==GAMUT_DEF,"gamut_status")
 req(r.get("forward_contract",{}).get("may_enter_gate_2") is c["gate2"],"forward_contract")
 vm=r.get("verification_method",{})
 req(vm.get("method_id")==METHOD_ID and vm.get("method_version")==METHOD_VERSION and
     vm.get("filename")==Path(__file__).name and vm.get("sha256")==vsha and
     vm.get("third_party_colour_library")=="NONE","verification_method")
 sd=r.get("source_definition",{})
 req(sd.get("primaries_xy")==[list(x) for x in c["p"]] and sd.get("white_xy")==list(c["w"]) and
     sd.get("white_name")==c["wn"] and sd.get("transfer")==c["transfer"] and sd.get("reference")==c["ref"],"source_definition")
 try: enc,lin,M,xyz,xyy=reconstruct(s,r["rgb_u8"])
 except Exception as ex: return r.get("case_id",path.stem),err+[f"reconstruct:{ex}"],None
 st=r.get("reconstructed_colorimetric_state",{}); tol=c["tol"]
 req(all(close(a,b,1e-15) for a,b in zip(st.get("encoded_rgb_normalized",[]),enc)),"encoded_rgb")
 req(all(close(a,b,1e-12) for a,b in zip(st.get("linear_rgb",[]),lin)),"linear_rgb")
 X=st.get("cie_xyz_relative",{}); req(X.get("whitepoint")==c["wn"],"whitepoint")
 req(all(close(X.get(k,1e9),v,tol) for k,v in zip(("X","Y","Z"),xyz)),"XYZ")
 Y=st.get("cie_xyY",{}); req(all(close(Y.get(k,1e9),v,max(tol,5e-5)) for k,v in zip(("x","y","Y"),xyy)),"xyY")
 d=r.get("diagnostics",{})
 for k,v in {"atlas_matching":"NOT_EXECUTED","pkl_matching":"NOT_EXECUTED","delta_e":"NOT_EXECUTED",
 "delta_lambda":"NOT_EXECUTED","identity_freeze":"NOT_EXECUTED","production_feasibility":"NOT_EXECUTED",
 "icc_output":"NOT_EXECUTED","measured_qc_status":"NOT_MEASURED"}.items(): req(d.get(k)==v,f"boundary:{k}")
 req(d.get("source_atlas_row_id") is None and d.get("pre_conversion_clipping") is False and
     d.get("implicit_profile_substitution") is False,"boundary:source")
 gs=r.get("gate_step_results",[]); req([x.get("step") for x in gs]==STEPS and all(x.get("status")=="PASS" for x in gs),"steps")
 return r["case_id"],err,{"matrix_rgb_to_xyz":M,"xyz":xyz,"xyY":xyy}

def check_package(d,vsha):
 e=[]; p=json.load(open(d/"PACKAGE_MANIFEST.json",encoding="utf-8"))
 if p.get("manifest_sha256")!=MANIFEST_SHA or p.get("program")!="P01" or p.get("gate")!="GATE-1": e.append("package identity")
 vm=p.get("verification_method",{})
 if vm.get("method_id")!=METHOD_ID or vm.get("method_version")!=METHOD_VERSION or vm.get("sha256")!=vsha: e.append("package verifier")
 seen=set()
 for x in p.get("records",[]):
  cid=x.get("case_id"); seen.add(cid); f=d/FILES.get(cid,"")
  if cid not in FILES or not f.exists() or x.get("sha256")!=sha(f) or x.get("gate1_status")!="PASS": e.append(f"record:{cid}")
 if seen!=set(FILES): e.append("record set")
 if p.get("publication_readiness")!="PASS": e.append("publication_readiness")
 return e

def check_sums(d):
 e=[]
 for line in (d/"SHA256SUMS.txt").read_text().splitlines():
  if not line.strip(): continue
  try: h,n=line.split("  ",1)
  except: e.append("malformed checksum"); continue
  p=d/n
  if not p.exists() or sha(p)!=h: e.append(f"checksum:{n}")
 return e

def main():
 a=argparse.ArgumentParser(); a.add_argument("--package",type=Path,default=Path(__file__).resolve().parent)
 a.add_argument("--manifest",type=Path,required=True); a.add_argument("--write-report",action="store_true")
 a=a.parse_args(); vsha=sha(Path(__file__).resolve())
 if sha(a.manifest)!=MANIFEST_SHA: print("FAIL: frozen manifest SHA",file=sys.stderr); return 2
 m=json.load(open(a.manifest,encoding="utf-8"))
 if (m.get("manifest_id"),m.get("version"),m.get("status"))!=("ATLAS-CLARUS-GATE1-EXECUTION-MANIFEST","0.1","FROZEN"):
  print("FAIL: manifest identity",file=sys.stderr); return 2
 cases=[]; errors=[]
 for cid,fn in FILES.items():
  got,e,d=check_record(a.package/fn,vsha); e += ([] if got==cid else ["file case_id"])
  cases.append({"case_id":cid,"status":"PASS" if not e else "FAIL","errors":e,"independent_reconstruction":d}); errors+=e
 pe=check_package(a.package,vsha); ce=check_sums(a.package); errors+=pe+ce
 report={"schema_id":"ATLAS_CLARUS_P01_GATE1_VERIFICATION_REPORT_V0_1","method_id":METHOD_ID,
 "method_version":METHOD_VERSION,"verifier_sha256":vsha,"manifest_sha256":MANIFEST_SHA,"cases":cases,
 "package_manifest_validation":"PASS" if not pe else "FAIL","package_manifest_errors":pe,
 "checksum_validation":"PASS" if not ce else "FAIL","checksum_errors":ce,
 "publication_readiness":"PASS" if not errors else "FAIL",
 "gate_boundary":{"atlas_matching":"NOT_EXECUTED","pkl_matching":"NOT_EXECUTED","delta_e":"NOT_EXECUTED",
 "delta_lambda":"NOT_EXECUTED","identity_freeze":"NOT_EXECUTED","production":"NOT_EXECUTED","measured_qc_status":"NOT_MEASURED"}}
 if a.write_report: (a.package/"VERIFICATION_REPORT.json").write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
 for x in cases: print(f"{x['case_id']}: {x['status']}")
 print("PACKAGE_MANIFEST:",report["package_manifest_validation"]); print("CHECKSUMS:",report["checksum_validation"])
 print("PUBLICATION_READINESS:",report["publication_readiness"]); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
