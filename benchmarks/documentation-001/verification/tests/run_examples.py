#!/usr/bin/env python3
import sys
import json
import subprocess
import tempfile
from pathlib import Path


def run_example(code, module_path):
    """Run a code example and check if it executes without errors.

    Args:
        code: The Python code to execute
        module_path: Path to the module being documented (to add to sys.path)

    Returns:
        dict with 'success' (bool), 'error' (str or None), 'output' (str)
    """
    # Create a temporary Python file with the example code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        # Add the module directory to sys.path so imports work
        module_dir = Path(module_path).parent
        f.write(f"import sys\n")
        f.write(f"sys.path.insert(0, '{module_dir}')\n\n")
        f.write(code)
        temp_file = f.name

    try:
        # Run the code
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )

        success = result.returncode == 0
        error = result.stderr if not success else None
        output = result.stdout

        return {
            'success': success,
            'error': error,
            'output': output
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Example execution timed out (10 seconds)',
            'output': ''
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'output': ''
        }
    finally:
        # Clean up temp file
        Path(temp_file).unlink(missing_ok=True)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: run_examples.py <module_path> <examples_json>", file=sys.stderr)
        sys.exit(1)

    module_path = sys.argv[1]
    examples_json = sys.argv[2]

    with open(examples_json, 'r') as f:
        examples = json.load(f)

    results = []
    for example in examples:
        result = run_example(example['code'], module_path)
        results.append({
            'location': example['location'],
            'code': example['code'],
            'success': result['success'],
            'error': result['error'],
            'output': result['output']
        })

    print(json.dumps(results, indent=2))
