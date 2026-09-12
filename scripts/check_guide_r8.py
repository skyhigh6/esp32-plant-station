"""PDF page/text bounds and raster previews for human-readable visual review."""
from pathlib import Path
import fitz,json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
pdf=ROOT/'output/pdf/Plant_Station_R8_Illustrated_Assembly_Guide.pdf'
out=ROOT/'output/pdf/qa/r8';out.mkdir(parents=True,exist_ok=True)
doc=fitz.open(pdf)
assert len(doc)==10
report={'pages':len(doc),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'page_checks':[]}
texts=[]
for i,page in enumerate(doc):
    words=page.get_text('words');assert words
    for x0,y0,x1,y1,*_ in words:
        assert x0>=26 and x1<=570 and y0>=25 and y1<=825,(i,x0,y0,x1,y1)
    t=page.get_text();texts.append(t)
    assert 'R8-A1' in t and 'First article pending' in t
    pix=page.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False)
    pix.save(out/f'page_{i+1:02}.png')
    report['page_checks'].append({'page':i+1,'words':len(words),'text_in_page_bounds':True})
full='\n'.join(texts)
for required in ['28 x 20','10.4','3 x 8','3 x 6','M2.5 x 16','D_6p2','NOT VERIFIED','22 pass']:
    assert required in full,required
for i in range(0,10,2):
    ims=[Image.open(out/f'page_{j+1:02}.png') for j in (i,i+1)]
    sheet=Image.new('RGB',(sum(im.width for im in ims),max(im.height for im in ims)), 'white')
    sheet.paste(ims[0],(0,0));sheet.paste(ims[1],(ims[0].width,0))
    sheet.save(out/f'review_{i//2+1}.png')
(out/'automated_checks.json').write_text(json.dumps(report,indent=2))
print('PASS: ten PDF pages, page bounds, footers, critical dimensions and quantities; rendered five review sheets')
