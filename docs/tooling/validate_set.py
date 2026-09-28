"""Verify controlled PDF identities, LOEP, placement, source hashes and content."""
from pathlib import Path
import hashlib
import json
import re
import sys
import pymupdf as fitz
from PIL import Image, ImageDraw

SET=Path(__file__).resolve().parents[1]


def main():
    matrix={row['id']:row for row in json.loads((SET/'control/change_matrix.json').read_text())}
    evidence=json.loads((SET/'control/evidence_register.json').read_text())
    for row in evidence:
        if hashlib.sha256((SET/row['snapshot']).read_bytes()).hexdigest()!=row['sha256']:
            raise AssertionError(f"Evidence hash changed: {row['source']}")
    report={'documents':{},'source_hash_records':len(evidence),'checks':[]}
    for folder in sorted((SET/'documents').iterdir()):
        d=json.loads((folder/'document.json').read_text(encoding='utf-8'))
        placements=json.loads((folder/'placements.json').read_text())
        pdf_path=folder/placements['document']
        expected=f"{d['document_id']}  |  DESIGN R17  |  D02"
        with fitz.open(pdf_path) as pdf:
            pages=len(pdf)
            texts=[]
            for i,page in enumerate(pdf):
                text=page.get_text()
                if expected not in text:raise AssertionError(f'Header missing {folder.name} p{i+1}')
                if f'{i+1} / {pages}' not in text:raise AssertionError(f'Footer missing {folder.name} p{i+1}')
                if '\ufffd' in text:raise AssertionError('Replacement glyph')
                for block in page.get_text('dict')['blocks']:
                    if block['type']!=0:continue
                    for line in block['lines']:
                        for span in line['spans']:
                            rect=fitz.Rect(span['bbox'])
                            if rect.x0<2 or rect.x1>page.rect.width-2 or rect.y0<2 or rect.y1>page.rect.height-2:
                                raise AssertionError(f'Text outside page: {folder.name} p{i+1}: {span["text"]}')
                texts.append(text)
            front='\n'.join(texts[:placements['front_pages']])
            for p in range(1,pages+1):
                if not re.search(rf'(?:^|\n){p}\s*\nD02\s*\n',front):
                    raise AssertionError(f'Missing effective-page row {folder.name} {p}')
            for si,sec in enumerate(d['sections'],1):
                actual=placements['section_pages'][str(si)]
                if not actual or sec['title'] not in '\n'.join(texts[n-1] for n in actual):
                    raise AssertionError(f'Bad section mapping {folder.name} {si}')
            for row in placements['placements']:
                x0,y0,x1,y1=row['rect']
                if y0<54 or y1>795 or x0<112 or x1>552:
                    raise AssertionError(f'Body placement outside frame: {folder.name} {row["block_id"]} {row["rect"]}')
                if row['labels']:
                    labels={matrix[x]['revision'] for x in row['change_ids']}
                    if set(row['labels'])!=labels:raise AssertionError('Uncontrolled bars')
            body='\n'.join(texts[placements['front_pages']:])
            required={
                'AM_R17':['9.8 x 4.2','15.2','1,000-4,000','D10 is unconnected','3.5 V','Unassigned'],
                'TR_R17':['R15','R16','9.998','exits 1','Unassigned'],
                'TS_R17':['A17-01','A17-13','Not tested','Not yet defined','Unassigned'],
            }[folder.name]
            for term in required:
                if term not in body:raise AssertionError(f'Missing key content {folder.name}: {term}')
            report['documents'][folder.name]={'pdf':pdf_path.name,'pages':pages,
                'front_pages':placements['front_pages'],'sha256':hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
                'barred_placements':sum(bool(row['labels']) for row in placements['placements']),
                'identity_loep_sections_bounds':True}
        renders=sorted((folder/'rendered').glob('page-*.png'))
        if len(renders)!=pages:raise AssertionError('Wrong render count')
        for index in range(0,len(renders),4):
            opened=[Image.open(path).convert('RGB') for path in renders[index:index+4]]
            w,h=opened[0].size
            sheet=Image.new('RGB',(2*w+36,2*h+60),'#d5d5d5')
            draw=ImageDraw.Draw(sheet)
            for n,img in enumerate(opened):
                x=12+(n%2)*(w+12);y=25+(n//2)*(h+25)
                sheet.paste(img,(x,y));draw.text((x,y-17),f'{folder.name} / page {index+n+1}',fill='black')
            sheet.save(folder/'rendered'/f'contact-{index//4+1:02d}.png')
    report['checks']=['PDF identity and page count','Every effective-page row','Every section map',
                      'Every body placement within frame','Revision bars resolve to matrix',
                      'All frozen-source hashes','Current configuration content checks','Every PDF page rendered']
    (SET.parent/'verification/documents/validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','pages':sum(v['pages'] for v in report['documents'].values()),'documents':report['documents']}))


if __name__=='__main__':main()
