#!/usr/bin/env python3
import argparse
import os

def generate_html_from_code(file_path):
    html_output = []
    code_block = []
    comment_buffer = []
    last_was_br = False

    def flush_code_block():
        nonlocal last_was_br
        if code_block:
            html_output.append("<pre><code>")
            html_output.extend(code_block)
            html_output.append("</code></pre>")
            code_block.clear()
            last_was_br = False

    def flush_comment_buffer():
        nonlocal last_was_br
        if comment_buffer:
            merged_comment = "<br>".join(comment_buffer)
            html_output.append(f"<p>{merged_comment}</p>")
            comment_buffer.clear()
            last_was_br = False

    with open(file_path, 'r') as file:
        for line in file:
            stripped = line.strip()

            if not stripped:
                flush_comment_buffer()
                flush_code_block()
                if not last_was_br:
                    html_output.append("<br>")
                    last_was_br = True
                continue

            if stripped.startswith("//"):
                flush_code_block()
                comment_text = stripped[2:].strip()
                if comment_text:
                    comment_buffer.append(comment_text)
                last_was_br = False
            elif "// " in stripped:
                flush_comment_buffer()
                code_part, comment_part = stripped.split("// ", 1)
                code_part = code_part.rstrip()
                if code_part:
                    flush_code_block()
                    html_output.append("<pre><code>")
                    html_output.append(code_part)
                    html_output.append("</code></pre>")
                if comment_part.strip():
                    html_output.append(f"<div class='side-note'><em>[ℹ]</em> {comment_part.strip()}</div><br>")
                last_was_br = False
            else:
                flush_comment_buffer()
                code_block.append(line.rstrip())
                last_was_br = False

    flush_comment_buffer()
    flush_code_block()
    return "\n".join(html_output)


def generate_full_html(body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>brdown output</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        code {{ font-family: monospace; }}
        p {{ margin-top: 1em; }}
        .side-note {{ background: #fff3cd; padding: 8px; border-left: 4px solid #ffeeba; margin-bottom: 1em; }}
    </style>
</head>
<body>
{body}
<br><br>
<small>Generated with brdown</small>
</body>
</html>"""

def main():
    parser = argparse.ArgumentParser(description="Transform your commented code into an HTML docpage.")
    parser.add_argument("input", help="Input code file")
    parser.add_argument("-o", "--output", help="Output HTML file (optional)")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: Couldn't find file '{args.input}'.")
        return

    html_body = generate_html_from_code(args.input)
    full_html = generate_full_html(html_body)

    if args.output:
        with open(args.output, "w") as f:
            f.write(full_html)
        print(f"HTML output saved to {args.output}")
    else:
        print(full_html)

if __name__ == "__main__":
    main()

