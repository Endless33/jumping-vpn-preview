import os
import re

class SpecMap:
    """
    Builds a cross-reference map between DEMO_SPEC.md and demo_engine source files.
    """

    def __init__(self, spec_path="DEMO_SPEC.md", src_dir="demo_engine", output="SPEC_MAP.md"):
        self.spec_path = spec_path
        self.src_dir = src_dir
        self.output = output
        self.spec_sections = []
        self.code_index = {}

    def load_spec(self):
        with open(self.spec_path, "r") as f:
            lines = f.readlines()

        current = None
        for line in lines:
            if line.startswith("#"):
                current = line.strip()
                self.spec_sections.append({"section": current, "keywords": [], "matches": []})
            else:
                if current:
                    words = re.findall(r"[A-Za-z_]+", line)
                    self.spec_sections[-1]["keywords"].extend(words)

    def index_code(self):
        for root, _, files in os.walk(self.src_dir):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    with open(path, "r") as f:
                        content = f.read()
                    self.code_index[path] = content

    def match(self):
        for section in self.spec_sections:
            keywords = set(k.lower() for k in section["keywords"] if len(k) > 4)
            for path, content in self.code_index.items():
                text = content.lower()
                score = sum(1 for k in keywords if k in text)
                if score > 5:  # threshold
                    section["matches"].append({"file": path, "score": score})

    def export(self):
        lines = []
        lines.append("# DEMO_SPEC → CODE Cross-Reference\n")
        lines.append("This document maps specification sections to implementation files.\n")

        for sec in self.spec_sections:
            lines.append(f"## {sec['section']}\n")
            if not sec["matches"]:
                lines.append("_No matching implementation found._\n")
                continue

            lines.append("| File | Match Score |")
            lines.append("|------|-------------|")
            for m in sec["matches"]:
                lines.append(f"| `{m['file']}` | {m['score']} |")
            lines.append("")

        with open(self.output, "w") as f:
            f.write("\n".join(lines))

        return self.output