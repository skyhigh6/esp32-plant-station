"""Build one editable JSON document. Python 3 + reportlab + pymupdf + pillow.
Usage: python tooling/build_document.py documents/AM_R6/document.json
Paths inside document.json are relative to its folder. No original is modified.
"""
import argparse, json, re, html
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
import pymupdf as fitz

W,H=595.276,841.89
LEFT,RIGHT,TOP,BOTTOM=114,45,57,48
# ReportLab's document frame has 6 pt inset on each side.
WIDTH=W-LEFT-RIGHT-12
BODY=ParagraphStyle('body',fontName='Helvetica',fontSize=9.5,leading=13,spaceAfter=7)
CELL=ParagraphStyle('cell',parent=BODY,fontSize=8.5,leading=11,spaceAfter=0)
HEAD=ParagraphStyle('head',parent=BODY,fontName='Helvetica-Bold',fontSize=15,leading=19,spaceAfter=12)
SUB=ParagraphStyle('sub',parent=BODY,fontName='Helvetica-Bold',fontSize=10.5,leading=14,spaceAfter=7)
SMALL=ParagraphStyle('small',parent=BODY,fontSize=8,leading=11)

def clean(s):
    s=str(s).replace('\u2011','-').replace('\u2013','-').replace('\u2014',' - ')
    s=s.replace('≤','&lt;=').replace('≥','&gt;=').replace('→','-&gt;').replace('×',' x ').replace('Ω','Ohm')
    s=re.sub(r' color=[\"\'][^\"\']+[\"\']','',s)
    return s

class Marked(Flowable):
    def __init__(self,inner,labels=(),ids=(),block_id='',log=None,section=0,skip_header=False):
        Flowable.__init__(self);self.inner=inner;self.labels=sorted(set(labels),key=lambda x:int(x[1:]));self.ids=ids;self.block_id=block_id;self.log=log;self.section=section;self.skip_header=skip_header
    def wrap(self,aW,aH):
        self.width,self.height=self.inner.wrap(aW,aH); return self.width,self.height
    def split(self,aW,aH):
        parts=self.inner.split(aW,aH)
        return [Marked(p,self.labels,self.ids,self.block_id,self.log,self.section,self.skip_header) for p in parts]
    def draw(self):
        self.inner.drawOn(self.canv,0,0)
        bar_height=self.height-(self.inner._rowHeights[0] if self.skip_header else 0)
        for i,label in enumerate(self.labels):
            x=-12-i*14
            self.canv.setStrokeColor(colors.black);self.canv.setLineWidth(.7)
            self.canv.line(x,1,x,max(2,bar_height-1))
            self.canv.saveState();self.canv.translate(x-2,max(0,(bar_height-stringWidth(label,'Helvetica-Bold',6.5))/2));self.canv.rotate(90)
            self.canv.setFillColor(colors.black);self.canv.setFont('Helvetica-Bold',6.5);self.canv.drawString(0,0,label);self.canv.restoreState()
        if self.log is not None:
            x,y=self.canv.absolutePosition(0,0)
            self.log.append(dict(block_id=self.block_id,section=self.section,body_page=self.canv.getPageNumber(),rect=[x,H-y-self.height,x+self.width,H-y],bar_rect=[x-12-max(0,len(self.labels)-1)*14,H-y-bar_height,x-12,H-y],labels=self.labels,change_ids=self.ids))

def para(s,style=BODY):return Paragraph(clean(s),style)
class RevisionTable(Table):
    """Row metadata travels with Paragraphs when ReportLab splits the table."""
    def draw(self):
        super().draw()
        for ri,row in enumerate(self._cellvalues):
            first=row[0]
            if isinstance(first,(list,tuple)):first=first[0] if first else None
            meta=getattr(first,'revision_meta',None)
            if not meta:continue
            labels,ids,bid,log,section=meta
            y=self._rowpositions[ri+1];height=self._rowHeights[ri]
            for i,label in enumerate(sorted(set(labels),key=lambda x:int(x[1:]))):
                x=-12-i*14;self.canv.setStrokeColor(colors.black);self.canv.setLineWidth(.7)
                self.canv.line(x,y+1,x,y+height-1)
                self.canv.saveState();self.canv.translate(x-2,y+max(0,(height-stringWidth(label,'Helvetica-Bold',6.5))/2));self.canv.rotate(90)
                self.canv.setFont('Helvetica-Bold',6.5);self.canv.setFillColor(colors.black);self.canv.drawString(0,0,label);self.canv.restoreState()
            x0,y0=self.canv.absolutePosition(0,y)
            log.append(dict(block_id=bid,section=section,body_page=self.canv.getPageNumber(),rect=[x0,H-y0-height,x0+self._width,H-y0],bar_rect=[x0-12-max(0,len(labels)-1)*14,H-y0-height,x0-12,H-y0],labels=labels,change_ids=ids))

def table(rows,widths=None,row_meta=None):
    if widths is None:widths=[WIDTH/len(rows[0])]*len(rows[0])
    else:widths=[WIDTH*x/sum(widths) for x in widths]
    cells=[[para(v,CELL) for v in row] for row in rows]
    for ri,meta in (row_meta or {}).items():cells[ri][0].revision_meta=meta
    t=RevisionTable(cells,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eeeeee')),('LINEBELOW',(0,0),(-1,-1),.35,colors.HexColor('#999999')),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5)]))
    return t

def build(path):
    path=Path(path).resolve();base=path.parent;d=json.loads(path.read_text(encoding='utf8'));log=[];story=[]
    issue=d['document_issue'];date=d['issue_date'];status=d['status']
    matrix=json.loads((base.parents[1]/'control/change_matrix.json').read_text(encoding='utf8'))
    changes={item['id']:item for item in matrix}
    def check_bars(labels,ids,block):
        if set(labels)!={changes[item]['revision'] for item in ids}:
            raise ValueError(f'{block}: labels and verified matrix IDs disagree')
    for sec in d['sections']:
        for block in sec['blocks']:
            check_bars(block.get('bars',[]),block.get('change_ids',[]),block.get('id','block'))
            for row,labels in block.get('row_bars',{}).items():
                check_bars(labels,block.get('row_change_ids',{}).get(row,[]),f'row {row}')
    for si,sec in enumerate(d['sections'],1):
        if si>1:story.append(PageBreak())
        story.append(Marked(para(f"{si:02d}  {sec['title']}",HEAD),block_id=f's{si}-heading',log=log,section=si))
        if sec.get('subtitle'):story.append(Marked(para(sec['subtitle'],SMALL),block_id=f's{si}-subtitle',log=log,section=si))
        for bi,b in enumerate(sec['blocks'],1):
            bid=b.get('id',f's{si}-b{bi}');labels=b.get('bars',[]);ids=b.get('change_ids',[])
            if labels and not ids:raise ValueError(f'{bid}: bars require verified change IDs')
            if any(int(v[1:])>d['design_revision'] for v in labels):raise ValueError(f'{bid}: future revision bar')
            kind=b['type']
            if kind=='table':
                rows=b['rows'];widths=b.get('widths');rbs=b.get('row_bars',{});rids=b.get('row_change_ids',{})
                if rbs:
                    metadata={}
                    for key,rlabs in rbs.items():
                        if not rids.get(key):raise ValueError(f'{bid} row {key}: missing change IDs')
                        if any(int(v[1:])>d['design_revision'] for v in rlabs):raise ValueError(f'{bid} row {key}: future bar')
                        metadata[int(key)]=(rlabs,rids[key],f'{bid}-row{key}',log,si)
                    story.append(Marked(table(rows,widths,metadata),block_id=bid,log=log,section=si));story.append(Spacer(1,9))
                else:story.append(Marked(table(rows,widths),labels,ids,bid,log,si));story.append(Spacer(1,9))
            elif kind=='image':
                ip=base/b['path'];iw,ih=ImageReader(str(ip)).getSize();scale=min(WIDTH/iw,b.get('max_height',310)/ih)
                story.append(Marked(Image(str(ip),width=iw*scale,height=ih*scale),labels,ids,bid,log,si))
                if b.get('caption'):story.append(Marked(para(b['caption'],SMALL),block_id=bid+'-caption',log=log,section=si))
                story.append(Spacer(1,8))
            else:
                st=SUB if kind=='heading' else BODY
                content=b['text']
                if kind in ['note','caution','warning']:
                    st=ParagraphStyle(kind,parent=BODY,borderColor=colors.black,borderWidth=.5,borderPadding=7,backColor=colors.HexColor('#f4f4f4'),spaceBefore=5,spaceAfter=10)
                    story.append(Spacer(1,9))
                    if not re.match(r'(?i)\s*(?:<b>)?'+kind,content):content='<b>'+kind.upper()+'</b><br/>'+content
                story.append(Marked(para(content,st),labels,ids,bid,log,si));story.append(Spacer(1,13 if kind in ['note','caution','warning'] else 5))
    body=base/'body.tmp.pdf'
    SimpleDocTemplate(str(body),pagesize=(W,H),leftMargin=LEFT,rightMargin=RIGHT,topMargin=TOP,bottomMargin=BOTTOM).build(story)
    nbody=len(fitz.open(body));section_pages={}
    for r in log:section_pages.setdefault(str(r['section']),set()).add(r['body_page'])
    # Front matter rebuilt until LOEP and total page counts stabilise.
    nfront=3
    for _ in range(6):
        frontstory=[para(d['title'],HEAD),Spacer(1,25),table([
            ['Controlled field','Value'],['Document number',d['document_id']],['Plant design revision',f"R{d['design_revision']}"],['Document issue',issue],['Issue date',date],['Preceding document',d['original_identity']],['Status',status]]),Spacer(1,16),para(d['scope_note']),para('R17 incorporates R15/R16 mechanical changes and the current Uno UI v6 interface. Previous issues are retained. Blank physical results remain open; no acceptance signature is inferred.',SMALL),PageBreak(),para('Revision control',HEAD),para('Narrow parallel left-margin bars identify surviving changes against the verified matrix. Dates are documentary dates. R15/R16 source changes are incorporated without creating intervening manual issues.'),table([['Revision / class','Change and affected content']]+[[h['revision'],h['description']] for h in d['history']],[95,340]),Spacer(1,10),para('D02 / document control: new integrated R17 technical content in the established D01 A4 template. Pagination, new headings and editorial reflow alone receive no technical bar.',SMALL),para(d['history_limit'],SMALL),PageBreak(),para('List of effective pages',HEAD),para(f'All pages are effective at {issue}, dated {date}, for the R17 prototype. Section references provide navigation; technical change labels are controlled separately.'),table([['Page','Issue','Content']]+[[str(p),issue,'Control pages' if p<=nfront else 'Section '+next((s for s,ps in section_pages.items() if p-nfront in ps),'?')] for p in range(1,nfront+nbody+1)],[40,70,325]),Spacer(1,12),para('Section / page cross-reference',SUB),table([['Section','Subject','Effective pages']]+[[str(i),sec['title'],', '.join(str(p+nfront) for p in sorted(section_pages[str(i)]))] for i,sec in enumerate(d['sections'],1)],[40,300,95])]
        front=base/'front.tmp.pdf'
        SimpleDocTemplate(str(front),pagesize=(W,H),leftMargin=LEFT,rightMargin=RIGHT,topMargin=TOP,bottomMargin=BOTTOM).build(frontstory)
        actual=len(fitz.open(front))
        if actual==nfront:break
        nfront=actual
    else:raise RuntimeError('Front matter page count did not converge')
    result=fitz.open(front);result.insert_pdf(fitz.open(body));total=len(result)
    for i,p in enumerate(result):
        p.insert_text((LEFT,30),f"{d['document_id']}  |  DESIGN R{d['design_revision']}  |  {issue}",fontsize=8,fontname='hebo')
        p.draw_line((LEFT,38),(W-RIGHT,38),color=(0,0,0),width=.5)
        p.insert_text((LEFT,H-25),'PLANT STATION  /  R17 prototype - physical acceptance open',fontsize=7.5)
        p.insert_text((W-RIGHT-64,H-25),f'{i+1} / {total}',fontsize=8)
    target=base/f"{d['document_id']}_R{d['design_revision']}_{issue}.pdf"
    result.set_metadata({'title':d['title'],'subject':f"Design R{d['design_revision']}; document issue {issue}"});result.save(target,garbage=4,deflate=True);result.close()
    for r in log:r['page']=r['body_page']+nfront
    manifest={'document':target.name,'pages':total,'front_pages':nfront,'section_pages':{k:[v+nfront for v in sorted(vs)] for k,vs in section_pages.items()},'placements':log}
    (base/'placements.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
    renders=base/'rendered';renders.mkdir(exist_ok=True)
    with fitz.open(target) as pdf:
        for i,p in enumerate(pdf):p.get_pixmap(matrix=fitz.Matrix(1.25,1.25)).save(renders/f'page-{i+1:03d}.png')
    body.unlink();front.unlink();print(json.dumps({'pdf':str(target),'pages':total}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('source');build(parser.parse_args().source)
