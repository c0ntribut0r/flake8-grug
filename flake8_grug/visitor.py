import ast
from dataclasses import dataclass, field

from .errors import Error
from .errors.copy_paste import iter_error_copy_paste
from .errors.early_quit import get_error_early_quit
from .errors.eval import get_error_eval
from .errors.try_too_much import get_error_try_too_much
from .errors.requests_no_status_check import get_error_requests_no_status_check


@dataclass
class Visitor(ast.NodeVisitor):
    errors: list[Error] = field(default_factory=list)

    def visit(self, node: ast.AST):
        if not node.parent:  # root node
            self.errors.extend(iter_error_copy_paste(self.lines))

        super().visit(node)

    def visit_If(self, node: ast.If):
        if error := get_error_early_quit(node):
            self.errors.append(error)

    def visit_Call(self, node: ast.Call):
        if error := get_error_eval(node):
            self.errors.append(error)

        if error := get_error_requests_no_status_check(node):
            self.errors.append(error)

    def visit_Try(self, node: ast.Try):
        if error := get_error_try_too_much(node):
            self.errors.append(error)
