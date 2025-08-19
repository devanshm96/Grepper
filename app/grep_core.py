# app/grep_core.py
def match_pattern(input_line, pattern):
    if pattern == "\\d":
        return any(char.isdigit() for char in input_line)
    if pattern == "\\w":
        return any(char.isalnum() or char == "_" for char in input_line)
    if pattern.startswith("[") and pattern.endswith("]"):
        if len(pattern) > 2 and pattern[1] == "^":
            return any(char not in pattern[2:-1] for char in input_line)
        else:
            return any(char in pattern[1:-1] for char in input_line)
    if len(pattern) == 1:
        return pattern in input_line
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")

def grep_match(text, pattern):
    # Return matching lines for a simple UI
    lines = text.splitlines()
    return [line for line in lines if match_pattern(line, pattern)]
