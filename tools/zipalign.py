import zipfile,sys,struct
src,dst=sys.argv[1],sys.argv[2]
zin=zipfile.ZipFile(src)
with open(dst,'wb') as f:
    zout=zipfile.ZipFile(f,'w')
    for info in zin.infolist():
        data=zin.read(info.filename)
        ni=zipfile.ZipInfo(info.filename,date_time=info.date_time)
        ni.compress_type=info.compress_type; ni.external_attr=info.external_attr
        if ni.compress_type==zipfile.ZIP_STORED:
            # header = 30 + len(name) + len(extra); pad extra so data starts on 4-byte boundary
            off=f.tell()+30+len(ni.filename.encode())
            pad=(-off)%4
            ni.extra=b'\0'*pad
        zout.writestr(ni,data)
    zout.close()
