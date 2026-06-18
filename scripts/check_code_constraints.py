import ast
import sys
from pathlib import Path

NESTING_NODES = (
    ast.If,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.With,
    ast.AsyncWith,
    ast.Try,
    ast.Match,
)
MAX_CODE_LINES = 50
MAX_NESTING = 3


def main() -> int:
    """检查 Python 代码是否满足函数行数和嵌套层级约束。"""
    paths = [Path(item) for item in sys.argv[1:]]
    files = [file for path in paths for file in _python_files(path)]
    violations = [item for file in files for item in _check_file(file)]
    for violation in violations:
        print(violation)
    return 1 if violations else 0


def _python_files(path: Path) -> list[Path]:
    if path.is_file() and path.suffix == ".py":
        return [path]
    if path.is_dir():
        return sorted(path.rglob("*.py"))
    return []


def _check_file(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    lines = source.splitlines()
    nodes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    ]
    return [message for node in nodes for message in _check_function(path, lines, node)]


def _check_function(
    path: Path,
    lines: list[str],
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> list[str]:
    messages = []
    code_lines = _code_line_count(lines, node.lineno, node.end_lineno or node.lineno)
    nesting = _max_nesting(node)
    name = getattr(node, "name", "<unknown>")
    if code_lines > MAX_CODE_LINES:
        messages.append(f"{path}:{node.lineno} {name} has {code_lines} code lines")
    if nesting > MAX_NESTING:
        messages.append(f"{path}:{node.lineno} {name} nesting is {nesting}")
    return messages


def _code_line_count(lines: list[str], start: int, end: int) -> int:
    selected = lines[start - 1 : end]
    return sum(1 for line in selected if _is_code_line(line))


def _is_code_line(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and not stripped.startswith("#")


def _max_nesting(node: ast.AST, depth: int = 0) -> int:
    child_depths = [
        _max_nesting(child, _next_depth(child, depth))
        for child in ast.iter_child_nodes(node)
    ]
    return max([depth, *child_depths])


def _next_depth(node: ast.AST, depth: int) -> int:
    return depth + 1 if isinstance(node, NESTING_NODES) else depth


if __name__ == "__main__":
    raise SystemExit(main())
