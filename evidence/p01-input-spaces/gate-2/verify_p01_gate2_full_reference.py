#!/usr/bin/env python3
"""Final independent P01 Gate-2 full-reference verifier v0.3.0.

This script does not import atlas_clarus.binding. It independently verifies:
- the published P01-A Gate-1 predecessor;
- the frozen Gate-2 manifest and master;
- two complete 13,283-row RGB rankings;
- the complete Gate-2 evidence/boundary fields;
- the immutable verification report;
- package artifact hashes and SHA256SUMS.txt.

SHA256SUMS.txt binds every package payload artifact except itself.
"""
from __future__ import annotations
import argparse, ast, hashlib, json
from pathlib import Path
from typing import Any
import pandas as pd

METHOD_ID = "ATLAS_CLARUS_P01_GATE2_FULL_REFERENCE_VERIFIER"
METHOD_VERSION = "0.3.0"
EXPECTED_MASTER_SHA = "8283ab91b10f89ac758d09ecf5fb4d6343536600a06dd468b1cc1ecf4ec747c4"
EXPECTED_MASTER_ROWS = 13283
EXPECTED_GATE1_SHA = "e7d4b87ca6274e2d15edcc975591e682c62bff3fe0ad04f90020cc846b9a8dbc"
EXPECTED_GATE2_MANIFEST_SHA = "ae866f5484eed44b0dc6b7283c81b577b39aaa8be483b3e5375adb9c96839256"
EXPECTED_INPUT = [0, 255, 0]
EXPECTED_GATE3_STATE = "READY"
EXPECTED_PUBLICATION_STATE = "PUBLICATION_READY"

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def load_json(path: Path) -> dict[str, Any]:
    value=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value

def rgb_tuple(value: Any) -> tuple[int,int,int]:
    if isinstance(value,str):
        value=ast.literal_eval(value)
    if not isinstance(value,(list,tuple)) or len(value)!=3:
        raise ValueError(f"Invalid RGB triplet: {value!r}")
    rgb=tuple(int(v) for v in value)
    if any(v<0 or v>255 for v in rgb):
        raise ValueError(f"RGB outside 0..255: {rgb!r}")
    return rgb

def req(obj: dict[str,Any], keys: list[str], where: str) -> None:
    missing=[k for k in keys if k not in obj]
    if missing:
        raise ValueError(f"{where} missing required keys: {missing}")

def parse_checksums(path: Path) -> dict[str,str]:
    entries={}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        digest,name=raw.split("  ",1)
        if name in entries:
            raise ValueError(f"Duplicate checksum entry: {name}")
        entries[name]=digest
    return entries

def parse_rgb_rows(df: pd.DataFrame):
    return [(int(row_id), rgb_tuple(value)) for row_id,value in df["rgb"].items()]

def rank_loop(src, rows):
    ranked=[]
    for row_id,rgb in rows:
        d2=sum((a-b)**2 for a,b in zip(src,rgb))
        ranked.append((d2,row_id,rgb))
    ranked.sort(key=lambda x:(x[0],x[1]))
    return ranked

def rank_vectorized(src, rows):
    frame=pd.DataFrame(
        [{"row_id":row_id,"r":rgb[0],"g":rgb[1],"b":rgb[2]} for row_id,rgb in rows]
    )
    frame["d2"]=(frame["r"]-src[0])**2+(frame["g"]-src[1])**2+(frame["b"]-src[2])**2
    frame=frame.sort_values(["d2","row_id"], kind="stable")
    return [
        (int(row.d2),int(row.row_id),(int(row.r),int(row.g),int(row.b)))
        for row in frame.itertuples(index=False)
    ]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--master", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--gate1-evidence", required=True)
    ap.add_argument("--package-manifest", required=True)
    ap.add_argument("--checksums", required=True)
    ap.add_argument("--summary", required=True)
    ap.add_argument("--report", required=True)
    args=ap.parse_args()

    master=Path(args.master)
    manifest_path=Path(args.manifest)
    evidence_path=Path(args.evidence)
    gate1_path=Path(args.gate1_evidence)
    package_path=Path(args.package_manifest)
    checksums_path=Path(args.checksums)
    summary_path=Path(args.summary)
    report_path=Path(args.report)

    checks=[]
    def ck(name, condition, detail):
        status="PASS" if bool(condition) else "FAIL"
        checks.append({"check":name,"status":status,"detail":str(detail)})
        if status=="FAIL":
            print(json.dumps({"status":"FAIL","failed_check":name,"checks":checks}, indent=2))
            raise SystemExit(1)

    # Hash gates before any pickle loading.
    master_sha=sha256_file(master)
    gate1_sha=sha256_file(gate1_path)
    manifest_sha=sha256_file(manifest_path)
    evidence_sha=sha256_file(evidence_path)
    report_sha=sha256_file(report_path)
    self_sha=sha256_file(Path(__file__))

    ck("master_sha256", master_sha==EXPECTED_MASTER_SHA, master_sha)
    ck("gate1_evidence_sha256", gate1_sha==EXPECTED_GATE1_SHA, gate1_sha)
    ck("gate2_manifest_sha256", manifest_sha==EXPECTED_GATE2_MANIFEST_SHA, manifest_sha)

    manifest=load_json(manifest_path)
    evidence=load_json(evidence_path)
    gate1=load_json(gate1_path)
    package=load_json(package_path)
    report=load_json(report_path)

    req(manifest,["manifest_id","version","status","predecessor_contract","input_contract","master_contract","selection_contract","gate_boundary"],"manifest")
    req(evidence,["schema_id","program","gate","case_id","manifest_binding","predecessor_binding","input","master_validation","selection","diagnostics","prohibited_influence_check","gate_boundary","gate2_status","forward_contract","verification_method","conformance_harness"],"evidence")
    req(package,["schema_id","program","gate","status","publication_readiness","manifest_sha256","master_sha256","gate1_p01a_evidence_sha256","artifacts","result","conformance_harness_note","checksum_contract"],"package")
    req(report,["schema_id","status","method_id","method_version","verifier_sha256","master_sha256","gate1_evidence_sha256","gate2_manifest_sha256","gate2_evidence_sha256","winner","runner_up","gate_boundary","gate3_authorization","publication_readiness"],"report")

    ck("manifest_frozen", manifest["status"]=="FROZEN", manifest["status"])
    ck("manifest_binding", evidence["manifest_binding"]["manifest_sha256"]==manifest_sha and package["manifest_sha256"]==manifest_sha, evidence["manifest_binding"])
    ck("manifest_predecessor_hash", manifest["predecessor_contract"]["gate1_evidence_sha256"]==gate1_sha, manifest["predecessor_contract"]["gate1_evidence_sha256"])

    gate1_ok=(
        gate1.get("case_id")=="P01-A" and
        gate1.get("gate1_status")=="PASS" and
        gate1.get("route_class")=="NORMATIVE" and
        gate1.get("input_space")=="sRGB" and
        gate1.get("rgb_u8")==EXPECTED_INPUT and
        gate1.get("forward_contract",{}).get("may_enter_gate_2") is True and
        gate1.get("diagnostics",{}).get("source_atlas_row_id") is None and
        gate1.get("diagnostics",{}).get("identity_freeze")=="NOT_EXECUTED"
    )
    ck("gate1_predecessor_semantics", gate1_ok, {
        "case_id":gate1.get("case_id"),
        "status":gate1.get("gate1_status"),
        "route":gate1.get("route_class"),
        "input_space":gate1.get("input_space"),
        "rgb_u8":gate1.get("rgb_u8"),
        "may_enter_gate_2":gate1.get("forward_contract",{}).get("may_enter_gate_2")
    })
    ck("evidence_predecessor_binding", evidence["predecessor_binding"]["gate1_evidence_sha256"]==gate1_sha and package["gate1_p01a_evidence_sha256"]==gate1_sha, evidence["predecessor_binding"])

    input_ok=(
        manifest["input_contract"]["case_id"]=="P01-A" and
        manifest["input_contract"]["rgb_u8"]==EXPECTED_INPUT and
        manifest["input_contract"]["route_class"]=="NORMATIVE" and
        evidence["input"]["rgb_u8"]==EXPECTED_INPUT and
        evidence["input"]["route_class"]=="NORMATIVE"
    )
    ck("p01a_input_contract", input_ok, evidence["input"])

    # Only after trusted SHA-256 gate do we deserialize the pickle.
    df=pd.read_pickle(master)
    ck("master_row_count", len(df)==EXPECTED_MASTER_ROWS, len(df))
    ck("master_range_index", df.index.equals(pd.RangeIndex(0,EXPECTED_MASTER_ROWS)), repr(df.index))
    for col in ("reference","rgb","hex"):
        ck(f"master_column_{col}", col in df.columns, col)

    rows=parse_rgb_rows(df)
    src=tuple(EXPECTED_INPUT)
    rank_a=rank_loop(src,rows)
    rank_b=rank_vectorized(src,rows)
    ck("dual_ranking_equivalence", rank_a==rank_b, "loop ranking == vectorized ranking for all 13283 rows")

    winner_d2,winner_id,winner_rgb=rank_a[0]
    runner_d2,runner_id,runner_rgb=rank_a[1]
    winner_tied_ids=[row_id for d2,row_id,_ in rank_a if d2==winner_d2]
    runner_tied_ids=[row_id for d2,row_id,_ in rank_a if d2==runner_d2]
    winner_ref=str(df.loc[winner_id,"reference"])
    winner_hex=str(df.loc[winner_id,"hex"])
    runner_ref=str(df.loc[runner_id,"reference"])

    sel=evidence["selection"]
    expected_selection={
        "rows_evaluated":EXPECTED_MASTER_ROWS,
        "gate2_selected_atlas_row_id":winner_id,
        "gate2_selected_display_row":winner_id+1,
        "reference":winner_ref,
        "atlas_rgb":list(winner_rgb),
        "atlas_hex":winner_hex,
        "d2_rgb":winner_d2,
        "winner_tie_count":len(winner_tied_ids),
        "winner_tied_atlas_row_ids":winner_tied_ids,
        "tie_break_applied":len(winner_tied_ids)>1,
    }
    for key,value in expected_selection.items():
        ck(f"selection_{key}", sel.get(key)==value, f"{sel.get(key)!r} == {value!r}")

    diag=evidence["diagnostics"]
    expected_diag={
        "runner_up_atlas_row_id":runner_id,
        "runner_up_display_row":runner_id+1,
        "runner_up_reference":runner_ref,
        "runner_up_rgb":list(runner_rgb),
        "runner_up_d2_rgb":runner_d2,
        "runner_up_tie_count":len(runner_tied_ids),
        "runner_up_tied_atlas_row_ids":runner_tied_ids,
        "runner_up_tie_break_applied":len(runner_tied_ids)>1,
        "winner_margin_d2":runner_d2-winner_d2,
    }
    for key,value in expected_diag.items():
        ck(f"diagnostic_{key}", diag.get(key)==value, f"{diag.get(key)!r} == {value!r}")

    prohibited=evidence["prohibited_influence_check"]
    expected_prohibited={
        "lab_used":False,
        "delta_e_used":False,
        "delta_lambda_used":False,
        "icc_used":False,
        "cmyk_used":False,
        "gamut_mapping_used":False,
        "material_or_profile_approval_used":False,
    }
    ck("prohibited_influence_flags", all(prohibited.get(k) is v for k,v in expected_prohibited.items()), prohibited)

    boundary=evidence["gate_boundary"]
    boundary_ok=(
        boundary.get("persistent_source_atlas_row_id_freeze")=="NOT_EXECUTED" and
        boundary.get("freeze_status")=="NOT_FROZEN_GATE2" and
        boundary.get("production_atlas_row_id")=="NOT_EXECUTED" and
        boundary.get("measured_qc_status")=="NOT_MEASURED"
    )
    ck("gate2_boundary", boundary_ok, boundary)
    ck("gate2_status", evidence["gate2_status"]=="PASS", evidence["gate2_status"])

    gate3_ev=evidence["forward_contract"].get("gate3_authorization")
    gate3_pkg=package["result"].get("gate3_authorization")
    gate3_rep=report.get("gate3_authorization")
    ck("gate3_state_consistency", gate3_ev==gate3_pkg==gate3_rep==EXPECTED_GATE3_STATE, f"{gate3_ev}/{gate3_pkg}/{gate3_rep}")

    harness_note=evidence["conformance_harness"].get("staging_semantics","")
    ck("conformance_harness_staging_note", "staging" in harness_note.lower() and "workflow v3.4.0" in harness_note.lower() and "binding.py" in harness_note.lower(), harness_note)

    # Verifier self-binding.
    method=evidence["verification_method"]
    ck("verifier_method", method.get("method_id")==METHOD_ID and method.get("method_version")==METHOD_VERSION, method)
    ck("verifier_self_hash", method.get("sha256")==self_sha, self_sha)
    ck("verifier_no_core_import", method.get("imports_atlas_clarus_binding") is False, method)

    # Immutable report content.
    expected_report_core={
        "status":"PASS",
        "method_id":METHOD_ID,
        "method_version":METHOD_VERSION,
        "verifier_sha256":self_sha,
        "master_sha256":master_sha,
        "gate1_evidence_sha256":gate1_sha,
        "gate2_manifest_sha256":manifest_sha,
        "gate2_evidence_sha256":evidence_sha,
        "gate3_authorization":EXPECTED_GATE3_STATE,
        "publication_readiness":EXPECTED_PUBLICATION_STATE,
    }
    for key,value in expected_report_core.items():
        ck(f"report_{key}", report.get(key)==value, f"{report.get(key)!r} == {value!r}")

    expected_winner={
        "atlas_row_id":winner_id,"display_row":winner_id+1,"reference":winner_ref,
        "rgb":list(winner_rgb),"hex":winner_hex,"d2_rgb":winner_d2,
        "tie_count":len(winner_tied_ids),"tied_atlas_row_ids":winner_tied_ids,
    }
    for key,value in expected_winner.items():
        ck(f"report_winner_{key}", report["winner"].get(key)==value, f"{report['winner'].get(key)!r} == {value!r}")

    expected_runner={
        "atlas_row_id":runner_id,"display_row":runner_id+1,"reference":runner_ref,
        "rgb":list(runner_rgb),"d2_rgb":runner_d2,"tie_count":len(runner_tied_ids),
        "tied_atlas_row_ids":runner_tied_ids,"tie_break_applied":len(runner_tied_ids)>1,
        "winner_margin_d2":runner_d2-winner_d2,
    }
    for key,value in expected_runner.items():
        ck(f"report_runner_{key}", report["runner_up"].get(key)==value, f"{report['runner_up'].get(key)!r} == {value!r}")

    ck("report_gate_boundary", report["gate_boundary"]==boundary, report["gate_boundary"])

    # Package artifact hashes: all immutable payload artifacts except the
    # package manifest itself and SHA256SUMS.txt (to avoid mutual/self cycles).
    artifact_paths={
        manifest_path.name:manifest_path,
        manifest_path.with_suffix(".md").name:manifest_path.with_suffix(".md"),
        "ATLAS_Clarus_Gate-2_Execution_Manifest_v0.1_SHA256SUMS.txt":
            manifest_path.with_name("ATLAS_Clarus_Gate-2_Execution_Manifest_v0.1_SHA256SUMS.txt"),
        evidence_path.name:evidence_path,
        Path(__file__).name:Path(__file__),
        report_path.name:report_path,
        summary_path.name:summary_path,
    }
    for name,path in artifact_paths.items():
        entry=package["artifacts"].get(name,{})
        ck(f"package_artifact_{name}", entry.get("sha256")==sha256_file(path), f"{entry.get('sha256')} / {sha256_file(path)}")
    ck("package_report_role", package["artifacts"][report_path.name].get("role")=="FINAL_VERIFICATION_REPORT", package["artifacts"][report_path.name])

    # Human-readable summary must carry final key facts.
    summary=summary_path.read_text(encoding="utf-8")
    summary_needles=[
        "atlas_row_id = 5082","H135_L070_C100","d²_RGB = 3025",
        "runner_up_tie_count = 2","[4886, 5081]",
        "PUBLICATION READY","Gate-3 authorization: `READY`",
        "P01 conformance-harness staging field"
    ]
    ck("summary_key_facts", all(n in summary for n in summary_needles), summary_needles)

    # Frozen manifest companion.
    companion=manifest_path.with_name("ATLAS_Clarus_Gate-2_Execution_Manifest_v0.1_SHA256SUMS.txt")
    companion_entries=parse_checksums(companion)
    companion_ok=(
        companion_entries.get(manifest_path.name)==sha256_file(manifest_path) and
        companion_entries.get("ATLAS_Clarus_Gate-2_Execution_Manifest_v0.1_FROZEN.md")==sha256_file(manifest_path.with_suffix(".md"))
    )
    ck("frozen_manifest_companion_checksums", companion_ok, companion_entries)

    # Full package checksum scope: eight payload files, never SHA256SUMS itself.
    checksum_entries=parse_checksums(checksums_path)
    required_checksum_names={
        "ATLAS_Clarus_Gate-2_Execution_Manifest_v0.1_FROZEN.json",
        "ATLAS_Clarus_Gate-2_Execution_Manifest_v0.1_FROZEN.md",
        "ATLAS_Clarus_Gate-2_Execution_Manifest_v0.1_SHA256SUMS.txt",
        "P01-A_Gate-2_Full-Reference_Evidence_v0.1.json",
        "verify_p01_gate2_full_reference.py",
        "VERIFICATION_REPORT.json",
        "EXECUTION_SUMMARY.md",
        "PACKAGE_MANIFEST.json",
    }
    ck("checksum_scope_exact", set(checksum_entries)==required_checksum_names, sorted(checksum_entries))
    ck("checksum_self_excluded", checksums_path.name not in checksum_entries, sorted(checksum_entries))
    for name,digest in checksum_entries.items():
        ck(f"checksum_{name}", sha256_file(checksums_path.parent/name)==digest, name)

    contract=package["checksum_contract"]
    ck("checksum_contract", contract.get("filename")=="SHA256SUMS.txt" and contract.get("payload_count")==8 and contract.get("self_included") is False, contract)

    final_governance=(
        package["status"]=="PUBLICATION_READY" and
        package["publication_readiness"]==EXPECTED_PUBLICATION_STATE and
        report["publication_readiness"]==EXPECTED_PUBLICATION_STATE
    )
    ck("publication_governance_state", final_governance, {
        "package_status":package["status"],
        "package_readiness":package["publication_readiness"],
        "report_readiness":report["publication_readiness"],
    })

    result={
        "status":"PASS",
        "method_id":METHOD_ID,
        "method_version":METHOD_VERSION,
        "verifier_sha256":self_sha,
        "master_sha256":master_sha,
        "gate1_evidence_sha256":gate1_sha,
        "gate2_manifest_sha256":manifest_sha,
        "gate2_evidence_sha256":evidence_sha,
        "verification_report_sha256":report_sha,
        "winner":expected_winner,
        "runner_up":expected_runner,
        "gate3_authorization":EXPECTED_GATE3_STATE,
        "publication_readiness":EXPECTED_PUBLICATION_STATE,
        "check_count":len(checks),
        "checks":checks,
    }
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
