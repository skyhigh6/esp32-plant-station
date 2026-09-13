# R10 interactive STL explorer

From the repository root, run `python -m http.server 8767 --bind 127.0.0.1 --directory mechanical/concept_rev10`, then open http://127.0.0.1:8767/viewer/ . Stop the server with Ctrl+C.

Drag to rotate, scroll to zoom and right-drag to pan. Use the explosion slider, visibility checkboxes, part selector and isolation button to inspect the six enclosure STLs. Reset view frames the visible parts. Assemble returns all displayed parts to their original common coordinates. No mesh files are changed.

Loads the original STL files without simplification. Knob options and coupons are excluded because they use local accessory coordinates. Displayed dimensions are each original STL bounding box, not measurements between selected points. Explosion directions are illustrative, not a validated disassembly sequence.

Internet access is required for pinned Three.js 0.160.1 modules from jsDelivr. Uses the Three.js [OrbitControls](https://threejs.org/docs/#examples/en/controls/OrbitControls) and [STLLoader](https://threejs.org/docs/#examples/en/loaders/STLLoader). No analytics or uploads.
