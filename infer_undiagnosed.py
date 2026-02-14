#!/usr/bin/env python3
import csv
path='Cleaning_data_cleaned.csv'
with open(path,'r',encoding='utf-8') as f:
    reader=csv.reader(f)
    header=next(reader)
    lower=[h.strip().lower() for h in header]
    try:
        diq_idx=lower.index('diq010')
    except ValueError:
        diq_idx=None
    try:
        lbx_idx=lower.index('lbxgh')
    except ValueError:
        lbx_idx=None
    total=0
    diag=0
    bio=0
    und=0
    missing_bio=0
    for row in reader:
        total+=1
        diag_flag=False
        if diq_idx is not None and diq_idx < len(row):
            v=row[diq_idx].strip()
            if v!='':
                try:
                    if float(v)==1.0:
                        diag_flag=True
                except:
                    if v.lower() in ('1','yes','y','true'):
                        diag_flag=True
        bio_flag=False
        if lbx_idx is not None and lbx_idx < len(row):
            vv=row[lbx_idx].strip()
            try:
                hv=float(vv)
                if hv>=6.5:
                    bio_flag=True
            except:
                missing_bio+=1
        if diag_flag:
            diag+=1
        if bio_flag:
            bio+=1
            if not diag_flag:
                und+=1
    print(f"Rows scanned: {total}")
    if diq_idx is None:
        print('DIQ010 column not found in CSV header')
    else:
        print(f"Diagnosed (DIQ010==1): {diag}")
    if lbx_idx is None:
        print('LBXGH column not found in CSV header')
    else:
        print(f"Biomarker HbA1c>=6.5: {bio} (missing HbA1c values: {missing_bio})")
        print(f"Inferred undiagnosed (HbA1c>=6.5 and DIQ010!=1): {und}")
    if lbx_idx is not None and total>0:
        print(f"Prevalence (biomarker) among all rows: {bio/total:.4%}")
    if total>0:
        print(f"Prevalence inferred undiagnosed among all rows: {und/total:.4%}")
