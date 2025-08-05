from fastapi import APIRouter
# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from fastapi.responses import JSONResponse
import subprocess, tempfile, os, sys
from app.routes.api_models import CodeRequest

router = APIRouter()

@router.post("/run-python/")
async def run_python_code(request: CodeRequest):
    code_to_run = request.code
    DANGEROUS = ['os.', 'sys.', 'subprocess', 'socket', 'eval(', 'exec(', 'open(', '__import__']
    if any(danger in code_to_run for danger in DANGEROUS):
        return {"status": "error", "output": "", "error": "Unsafe code blocked."}

    output, error, temp_file_path = '', '', ''
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py', encoding='utf-8') as temp_file:
            temp_file.write(code_to_run)
            temp_file_path = temp_file.name

        result = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        output, error = result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        error = 'Execution timed out (5 seconds).'
    except Exception as e:
        error = f'Error: {str(e)}'
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return {"status": "success" if not error else "error", "output": output.strip(), "error": error.strip()}
