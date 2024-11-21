import os
import sys
import json

def deserialize_nested_json(data):
    if isinstance(data, dict):
        return {k: deserialize_nested_json(v) for k, v in data.items()}
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data
    return data

def main():
    input_string = os.getenv('INPUT_STRING')
    input_path = os.getenv('INPUT_PATH')
    max_size = int(os.getenv('MAX_SIZE', 1000))

    if not (input_string or input_path) or (input_string and input_path):
        print("Error: Provide either string or path, but not both.")
        sys.exit(1)

    if input_path:
        if not os.path.isfile(input_path):
            print(f"Error: Input file {input_path} not found.")
            sys.exit(1)
        with open(input_path, 'r') as file:
            input_data = file.read()
    else:
        input_data = input_string

    if not input_data:
        print("Error: Input data is empty.")
        sys.exit(1)

    if (file_size := len(input_data)) > max_size:
        print(f":warning: String content too long ({file_size} chars); exceeds {max_size} byte limit.")
        sys.exit(0)

    try:
        parsed_data = json.dumps(deserialize_nested_json(json.loads(input_data)), indent=2)
    except json.JSONDecodeError:
        print("Error: Input data is not valid JSON.")
        parsed_data = input_data  # Use raw input if not valid JSON

    summary_header = os.getenv('SUMMARY_HEADER')
    data_type = os.getenv('DATA_TYPE')
    github_step_summary = os.getenv('GITHUB_STEP_SUMMARY')

    output = f"## {summary_header}\n<details><summary>Click to expand</summary>\n\n```{data_type}\n{parsed_data}\n```\n</details>\n"
    with open(github_step_summary, 'a') as file:
        file.write(output)

if __name__ == '__main__':
    main()