#!/usr/bin/python3
import base64
import json
import os

file_lists = []
with open("global.json", "r") as f:
    file_lists = json.load(f)

with open("semantic-2.sql", "w") as f:
    f.write(
        "USE compiler;\n"
    )

# Get phase_id from config (default to 1 for semantic-1)
phase_id = 2

for case in file_lists:
    case_name = case.get("name", "")

    # Extract case name from path
    source = case.get("source", "")[0]
    input = case.get("input", "")[0]
    output = case.get("output", "")[0]

    # 0 = should compile successfully
    # 1 = should fail compilation
    compile_result = -case.get("compileexitcode", 0)

    # Read the test case file
    content = None
    try:
        with open(source, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {case}: {e}")
        continue
    
    # Encode code as base64
    base64_code = base64.b64encode(content.encode()).decode()
    
    # Generate SQL INSERT statement
    try: 
        with open("semantic-2.sql", "a") as f:
            f.write(
                f'INSERT INTO TestCases (test_case_disp_name, problem_phase, source_code_base64, compile_result) '
                f'VALUES ("{case_name}", {phase_id}, "{base64_code}", {compile_result});\n'
            )
    except Exception as e:
        print(f"Error writing SQL for {case}: {e}")
