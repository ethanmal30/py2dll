import os
import tempfile
import subprocess
import shutil
from pathlib import Path

def build_dll(py_files, name: str = None, outdir: str = "dist"):
    if isinstance(py_files, str):
        py_files = py_files.split()
    name = name or "compiled"
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        module_files = []
        for i, py_file in enumerate(py_files, start=1):
            src_file = Path(py_file)
            dest_file = temp_path / f"mod{i}.py"
            shutil.copy2(src_file, dest_file)
            module_files.append(f'"mod{i}.py"')
        
        modules_str = ",\n        ".join(module_files)
        setup_code = f"""from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize([
        {modules_str}
    ], compiler_directives={{'language_level': "3"}})
)
"""
        
        setup_path = temp_path / "setup.py"
        setup_path.write_text(setup_code, encoding="utf-8")

        try:
            result = subprocess.run(
                ["python", "setup.py", "build_ext", "--inplace"],
                check=True,
                cwd=temp_path,
                capture_output=True,
                text=True
            )
            
            for file in temp_path.iterdir():
                if file.suffix == '.pyd':
                    dll_path = outdir / f"{name}.dll"
                    shutil.copy2(file, dll_path)
                    return dll_path
            
            raise FileNotFoundError("No .pyd file was generated")

        except subprocess.CalledProcessError as e:
            error_output = e.stderr if e.stderr else "No error details available"
            raise RuntimeError(f"Compilation failed: {error_output}") from e