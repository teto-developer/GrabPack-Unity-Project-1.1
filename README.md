# GrabPack-Unity-Project-1.1

Download for unity poppy playtime project
Unity Version: 2021.3.36f1

How to Open:
1. Click Code → Download ZIP
2. Extract the folder
3. Open Unity Hub
4. Add Project from extracted folder

Please do not reupload or resell this project, you are welcome to use for your own projects/fan games


## Structure-preserving export
If you want to migrate/port this project while keeping the exact file structure and assets unchanged, you can generate a verified export package:

```bash
python3 Tools/preserve_structure_port.py ./PortedProject
```

This copies `Assets/`, `Packages/`, and `ProjectSettings/` into `./PortedProject` and creates `port-manifest.json` with SHA256 hashes for integrity verification.
