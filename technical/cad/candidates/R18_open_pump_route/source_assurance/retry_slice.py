from pathlib import Path
import subprocess,json,time
out=Path('.build/r18_source_audit').resolve();started=time.time()
cmd=['C:/Program Files/Bambu Studio/bambu-studio.exe','--slice','1','--mstpp','120','--debug','2','--export-3mf',str(out/'candidate_sliced.3mf'),str(out/'candidate_project.3mf')]
try:
 r=subprocess.run(cmd,capture_output=True,text=True,timeout=150)
 (out/'candidate_slice.log').write_text(r.stdout+'\nSTDERR:\n'+r.stderr,encoding='utf8');result={'name':'candidate','attempt':2,'exit_code':r.returncode,'elapsed_seconds':round(time.time()-started,1),'output_exists':(out/'candidate_sliced.3mf').exists()}
except subprocess.TimeoutExpired as e:
 result={'name':'candidate','attempt':2,'timeout_seconds':150};(out/'candidate_slice.log').write_bytes((e.stdout or b'')+b'\nTIMEOUT\n'+(e.stderr or b''))
print(result,flush=True)
results=json.loads((out/'slice_process_results.json').read_text());results.append(result);(out/'slice_process_results.json').write_text(json.dumps(results,indent=2))
