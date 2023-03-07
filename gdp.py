import argparse
import re
from abc import ABC, abstractmethod

ALLOWED_DEPENDENCIES = [
    "api",
    "implementation",
    "compile",
    "compileOnly",
    "kapt",
    "testImplementation",
    "androidTestImplementation",
]


def is_valid_dependency(line):
    for dep in ALLOWED_DEPENDENCIES:
        if dep in line:
            return True
    return False


def get_dependency_format(line):
    for dep in ALLOWED_DEPENDENCIES:
        if dep in line:
            return dep
    return None


class ParserFormat(ABC):
    @abstractmethod
    def write(self, deps, filename: str):
        pass

    @abstractmethod
    def parse(self, text):
        pass

    @staticmethod
    def file_header(title):
        return (
            f"============================================\n"
            f"{title}\r"
            f"============================================\r\r"
        )


class NormalFormat(ParserFormat):
    def parse(self, text):
        deps = []
        for line in text.splitlines():
            if is_valid_dependency(line) and "group" in line:
                dep = line.split("'")
                deps.append(
                    {
                        "group": dep[1],
                        "name": dep[3],
                        "version": dep[5],
                        "type": get_dependency_format(line),
                    }
                )
        return deps

    def write(self, deps, filename: str):
        with open(filename, "w") as f:
            f.write(self.file_header("NORMAL FORMATTED DEPENDENCIES"))
            for dep in deps:
                text = self.format_output(dep)
                f.write(text + "\r")

    def format_output(self, dep):
        return (
            f"{dep['type']} "
            f"group: '{dep['group']}', "
            f"name: '{dep['name']}', "
            f"version: '{dep['version']}'"
        )


class ShortFormat(ParserFormat):
    def parse(self, text):
        deps = []
        for line in text.splitlines():
            if (
                is_valid_dependency(line)
                and ":" in line
                and "name" not in line
                and "(" not in line  # skip kolin format
            ):
                quoted = re.compile(r'(?:\'|")(.*)(?:\'|")')
                result = quoted.findall(line)
                for c in ["'", '"']:
                    dep = result[0].replace(c, "")
                dep = dep.split(":")
                if len(dep) > 1:
                    deps.append(
                        {
                            "group": dep[0],
                            "name": dep[1],
                            "version": dep[2],
                            "type": get_dependency_format(line),
                        }
                    )
        return deps

    def write(self, deps, filename: str):
        with open(filename, "w") as f:
            f.write(self.file_header("SHORT FORMATTED DEPENDENCIES"))
            for dep in deps:
                text = self.format_output(dep)
                f.write(text + "\r")

    def format_output(self, dep):
        return f"{dep['type']} '{dep['group']}:{dep['name']}:{dep['version']}'"


class KotlinFormat(ParserFormat):
    def parse(self, text):
        deps = []
        for line in text.splitlines():
            if is_valid_dependency(line) and ":" in line and "(" in line:
                quoted = re.compile(r'(?:\'|")(.*)(?:\'|")')
                result = quoted.findall(line)
                for c in ["'", '"']:
                    dep = result[0].replace(c, "")
                dep = dep.split(":")
                deps.append(
                    {
                        "group": dep[0],
                        "name": dep[1],
                        "version": dep[2],
                        "type": get_dependency_format(line),
                    }
                )
        return deps

    def write(self, deps, filename: str):
        with open(filename, "w") as f:
            f.write(self.file_header("KOTLIN FORMATTED DEPENDENCIES"))
            for dep in deps:
                text = self.format_output(dep)
                f.write(text + "\r")

    def format_output(self, dep):
        return (
            f"{dep['type']}('{dep['group']}:{dep['name']}:{dep['version']}')"
        )


def get_input(input_format):
    if input_format == "normal":
        return NormalFormat()
    elif input_format == "short":
        return ShortFormat()
    elif input_format == "kotlin":
        return KotlinFormat()
    else:
        raise ValueError("Unknown input format")


def get_output(output_format):
    if output_format == "normal":
        return NormalFormat()
    elif output_format == "short":
        return ShortFormat()
    elif output_format == "kotlin":
        return KotlinFormat()
    else:
        raise ValueError("Unknown output format")


def main():
    parser = argparse.ArgumentParser(description="Gradle dependencies parser")
    parser.add_argument("file", help="Path to build.gradle file")
    parser.add_argument(
        "-f", "--output_file", help="Output file", default="data/output.txt"
    )
    parser.add_argument(
        "-i",
        "--input-format",
        help="Input format (normal, short, kotlin)",
        default="normal",
    )
    parser.add_argument(
        "-o",
        "--output-format",
        help="Output format (normal, short, kotlin)",
        default="normal",
    )
    args = parser.parse_args()

    input = get_input(args.input_format)
    output = get_output(args.output_format)

    with open(args.file, "r") as f:
        deps = input.parse(f.read())
        output.write(deps, args.output_file)


if __name__ == "__main__":
    main()
