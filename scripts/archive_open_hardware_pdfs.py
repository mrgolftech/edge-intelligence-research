#!/usr/bin/env python3
"""Archive unmodified BeagleBoard CC-BY-4.0 original product PDFs at pinned commits.

No PDF rendering, conversion, recompression, or other modifications.
Source: references/product-documents/open-hardware-pdf-sources.csv
Output:
  references/product-documents/originals/beagleboard/BHxxx_*.pdf
  references/product-documents/open-hardware-pdf-manifest.csv
"""
import csv
import hashlib
import io
import pathlib
import re
import urllib.parse
import urllib.request
from datetime import date
from pypdf import PdfReader

ROOT = pathlib.Path("references/product-documents")
SOURCE = ROOT / "open-hardware-pdf-sources.csv"
OUT = ROOT / "originals" / "beagleboard"
MANIFEST = ROOT / "open-hardware-pdf-manifest.csv"
MAX_BYTES = 35 * 1024 * 1024


def archive(row):
    result = dict(row)
    result.update(download_url="",local_path="",pages="",size_bytes="",sha256="",verified_date=date.today().isoformat(),status="FAILED",error="")
    try:
        repository = row["upstream_repo"]
        revision = row["upstream_commit"]
        path = row["upstream_path"]
        if not re.fullmatch(r"beagleboard/[a-zA-Z0-9_-]+", repository):
            raise ValueError("only BeagleBoard official GitHub repositories")
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("revision must be pinned 40-character Git SHA")
        if not path.lower().endswith(".pdf") or ".." in path:
            raise ValueError("source must be PDF path without directory traversal")
        if row["license"] != "CC-BY-4.0":
            raise ValueError("not authorized for public original redistribution")
        quoted = urllib.parse.quote(path, safe="/")
        url = "https://raw.githubusercontent.com/" + repository + "/" + revision + "/" + quoted
        result["download_url"] = url
        req = urllib.request.Request(url,headers={"User-Agent":"edge-intelligence-research-original-document-archive/1.0","Accept":"application/pdf,*/*"})
        with urllib.request.urlopen(req,timeout=75) as response:
            data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:raise ValueError("file too large")
        if len(data) != int(row["expected_bytes"]):
            raise ValueError("source byte count mismatch (pinned blob may be LFS or changed)")
        if not data.startswith(b"%PDF-"):raise ValueError("not a PDF file")
        reader = PdfReader(io.BytesIO(data),strict=False)
        if len(reader.pages) < 1:raise ValueError("zero-page PDF")
        dest = OUT / (row["source_id"] + "_" + re.sub(r"[^A-Za-z0-9_.-]","_",pathlib.PurePosixPath(path).name))
        # Exact, unmodified original bytes; preserve original file metadata in manifest.
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(data)
        result.update(local_path=str(dest),pages=len(reader.pages),size_bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),status="ARCHIVED")
    except Exception as ex:
        result["error"] = type(ex).__name__ + ": " + str(ex)[:300]
    print(row["source_id"],result["status"],result["size_bytes"],result["pages"],result["error"],flush=True)
    return result


def main():
    with SOURCE.open(newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
    dests = set()
    results = []
    for row in rows:
        if row["source_id"] in dests:raise ValueError("duplicate source ID")
        dests.add(row["source_id"])
        results.append(archive(row))
    fields=["source_id","product","upstream_repo","upstream_commit","upstream_path","expected_bytes","license","usage","download_status","download_url","local_path","pages","size_bytes","sha256","verified_date","status","error"]
    with MANIFEST.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        w.writerows(results)
    success=sum(x["status"]=="ARCHIVED" for x in results)
    print(f"Unmodified originals archived: {success}/{len(rows)}",flush=True)
    if success==0:raise SystemExit(2)


if __name__ == "__main__":
    main()
