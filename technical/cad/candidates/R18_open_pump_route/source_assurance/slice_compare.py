from pathlib import Path
import subprocess,json,time
out=Path('.build/r18_source_audit').resolve()
results=[]
for name in ['baseline','candidate']:
 cmd=['C:/Program Files/Bambu Studio/bambu-studio.exe','--slice','1','--mstpp','120','--debug','2','--export-3mf',str(out/(name+'_sliced.3mf')),str(out/(name+'_project.3mf'))]
 print('start',name,flush=True);started=time.time()
 try:
  r=subprocess.run(cmd,capture_output=True,text=True,timeout=150)
  (out/(name+'_slice.log')).write_text(r.stdout+'\nSTDERR:\n'+r.stderr,encoding='utf8')
  result={'name':name,'exit_code':r.returncode,'elapsed_seconds':round(time.time()-started,1),'output_exists':(out/(name+'_sliced.3mf')).exists()}
 except subprocess.TimeoutExpired as e:
  result={'name':name,'timeout_seconds':150,'output_exists':(out/(name+'_sliced.3mf')).exists()}
  (out/(name+'_slice.log')).write_bytes((e.stdout or b'')+b'\nTIMEOUT\n'+(e.stderr or b''))
 print(result,flush=True);results.append(result);(out/'slice_process_results.json').write_text(json.dumps(results,indent=2))
