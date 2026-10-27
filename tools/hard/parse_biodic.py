import pdfplumber, re, unicodedata, json, sys
out = {}
for f in sys.argv[2:]:
    rows = []
    fam = None
    for pg in pdfplumber.open(f).pages:
        for ln in (pg.extract_text() or "").splitlines():
            ln = unicodedata.normalize("NFKC", ln).strip()
            ln = re.sub(r"(?<=[ァ-ヶ])[-‐−―ｰ](?=[ァ-ヶ])", "ー", ln)  # 長音が「-」になっている行（デールギセル、シータテハ）
            m = re.match(r"^(\d{3,5})\s*([A-Z][a-z]+(?:\s+\([A-Z][a-z]+\))?\s+[a-z][a-z-]+(?:\s+[a-z][a-z-]+)?)\s+([ァ-ヶー・]+)(.*)$", ln)
            if m:
                alt = re.findall(r"[（(]([ァ-ヶー・]+)[)）]", m[4])
                rows.append({"code": m[1], "sci": re.sub(r"\s+\([A-Z][a-z]+\)", "", m[2]), "ja": m[3], "alt": alt, "rest": m[4].strip(), "family": fam}); continue
            m = re.match(r"^([A-Z]{4,}(?:IDAE|INAE))\b.*?([ァ-ヶー]+科)?$", ln)
            if m: fam = m[1]
    out[f.split("/")[-1][:-4]] = rows
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=0)
for k, v in out.items(): print(k, len(v), v[:2])
