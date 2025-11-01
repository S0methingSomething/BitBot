#!/usr/bin/env python3
"""Robust validation tool integration depth analyzer."""

import ast
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class FunctionValidation:
    """Validation status for a single function."""

    name: str
    line: int
    has_beartype: bool
    has_deal_pre: bool
    has_deal_post: bool
    has_deal_ensure: bool
    has_deal_raises: bool
    has_type_hints: bool
    type_ignores: int
    validation_score: float
    weak_types: list[str]  # Type hints containing Any
    type_strength: float  # 0-100, penalized for Any usage
    any_justified: bool  # Whether Any usage is justified
    justification_reason: str  # Why Any is justified/unjustified
    # NEW: Sophisticated features
    type_complexity: int  # Nesting depth of types (0-10+)
    validation_depth: float  # Contract effectiveness (0-100)
    code_smells: list[str]  # Detected code smells
    escape_hatches: int  # cast() usage count
    loc: int  # Lines of code
    param_count: int  # Number of parameters
    cyclomatic_complexity: int  # Estimated complexity
    # NEW: Architecture-aware features
    function_type: str  # api_call, file_io, cli_command, parser, service
    has_retry: bool  # Has @retry decorator
    returns_result: bool  # Returns Result[T, E]
    uses_error_context: bool  # Uses error_context()
    uses_logger: bool  # Uses get_logger()
    has_repo_validation: bool  # Validates repo with "/" check
    is_thin: bool  # CLI command <50 LOC
    architectural_violations: list[str]  # Pattern violations
    architectural_score: float  # Architecture-aware score


@dataclass
class FileStats:
    """Statistics for a single file."""

    path: str
    functions: int
    classes: int
    pydantic_models: int
    beartype_count: int
    deal_pre_count: int
    deal_post_count: int
    deal_ensure_count: int
    deal_raises_count: int
    type_hints_count: int
    type_ignores: int
    integration_score: float
    unvalidated_functions: list[str]
    validation_details: list[FunctionValidation]
    weak_type_count: int  # Functions with Any in types
    type_strength_score: float  # Average type strength
    justified_any_count: int  # Functions with justified Any
    unjustified_any_count: int  # Functions with unjustified Any
    # NEW: Sophisticated features
    avg_type_complexity: float  # Average type nesting depth
    avg_validation_depth: float  # Average contract effectiveness
    total_code_smells: int  # Total code smells detected
    total_escape_hatches: int  # Total cast() usage
    god_functions: list[str]  # Functions >50 LOC or >10 branches
    # NEW: Architecture-aware features
    api_call_count: int
    file_io_count: int
    cli_command_count: int
    parser_count: int
    service_count: int


class ValidationAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing validation tool usage."""

    def __init__(self, content: str, filepath: Path):
        self.content = content
        self.filepath = filepath
        self.functions: list[FunctionValidation] = []
        self.classes = 0
        self.pydantic_models = 0
        self.current_function: dict[str, Any] | None = None

    def _is_any_justified(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, weak_types: list[str]
    ) -> tuple[bool, str]:
        """Determine if Any usage is justified based on context."""
        if not weak_types:
            return True, "No Any usage"

        func_name = node.name.lower()

        # Check function body for justification clues
        func_body = ast.unparse(node)

        # Justified patterns
        justifications = []

        # 1. Loads from JSON/TOML/external files
        if any(x in func_body for x in ["json.load", "toml.load", ".open(", "json.loads"]):
            justifications.append("loads dynamic data from file")

        # 2. External API calls
        if any(x in func_body for x in ["requests.", "praw.", "github.", "gh api", "run_command"]):
            justifications.append("interfaces with external API")

        # 3. Config/state management
        if any(x in func_name for x in ["load", "config", "state", "parse"]):
            justifications.append("config/state management")

        # 4. Has runtime validation
        has_validation = any(
            [
                any("beartype" in ast.unparse(d) for d in node.decorator_list),
                any("deal" in ast.unparse(d) for d in node.decorator_list),
            ]
        )
        if has_validation:
            justifications.append("has runtime validation")

        # 5. Pydantic model usage
        if "BaseModel" in func_body or "pydantic" in func_body:
            justifications.append("uses Pydantic validation")

        # 6. Data transformation/aggregation
        if any(x in func_name for x in ["transform", "aggregate", "collect", "gather"]):
            justifications.append("data transformation")

        # Unjustified patterns
        unjustifications = []

        # 1. Simple helper functions
        if func_name.startswith("_") and len(node.body) < 10:
            unjustifications.append("simple internal helper")

        # 2. No external dependencies
        if not any(x in func_body for x in ["json", "toml", "requests", "praw", "github", "open"]):
            unjustifications.append("no external data sources")

        # 3. Could use TypedDict
        if "dict[str, Any]" in str(weak_types) and len(weak_types) == 1:
            unjustifications.append("could use TypedDict")

        # Decision logic
        if len(justifications) >= 2:
            return True, f"Justified: {', '.join(justifications[:2])}"
        if len(justifications) == 1 and not unjustifications:
            return True, f"Likely justified: {justifications[0]}"
        if unjustifications:
            return False, f"Unjustified: {', '.join(unjustifications[:2])}"
        return False, "Unclear justification"

    def _calculate_type_complexity(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
        """Calculate type nesting depth (0-10+)."""
        max_depth = 0

        def get_depth(annotation: ast.expr, current_depth: int = 0) -> int:
            if isinstance(annotation, ast.Subscript):
                # dict[str, Any] or list[dict[...]]
                return max(
                    get_depth(annotation.value, current_depth + 1),
                    get_depth(annotation.slice, current_depth + 1),
                )
            if isinstance(annotation, ast.Tuple):
                # Union types or tuple elements
                return max(
                    (get_depth(elt, current_depth) for elt in annotation.elts),
                    default=current_depth,
                )
            return current_depth

        # Check return type
        if node.returns:
            max_depth = max(max_depth, get_depth(node.returns))

        # Check parameter types
        for arg in node.args.args:
            if arg.annotation:
                max_depth = max(max_depth, get_depth(arg.annotation))

        return max_depth

    def _calculate_validation_depth(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> float:
        """Calculate contract effectiveness (0-100)."""
        score = 0.0
        param_count = len(node.args.args)

        if param_count == 0:
            return 100.0  # No params to validate

        validated_params = set()

        for dec in node.decorator_list:
            try:
                dec_str = ast.unparse(dec)
                if "deal.pre" in dec_str or "@pre" in dec_str:
                    # Parse lambda to see which params are checked
                    if "lambda" in dec_str:
                        # Extract parameter names from lambda
                        for arg in node.args.args:
                            if arg.arg in dec_str and arg.arg != "_":
                                validated_params.add(arg.arg)
                        # Check if it's a weak contract
                        if ": True" in dec_str or "lambda: " in dec_str:
                            score -= 20  # Penalty for useless contract
            except Exception:
                continue

        # Score based on parameter coverage
        if param_count > 0:
            coverage = len(validated_params) / param_count
            score += coverage * 100

        return max(0.0, min(100.0, score))

    def _detect_code_smells(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
        """Detect code smells in function."""
        smells = []

        # 1. God function (>50 LOC)
        loc = (node.end_lineno or node.lineno) - node.lineno
        if loc > 50:
            smells.append(f"god_function ({loc} LOC)")

        # 2. Long parameter list (>5 params)
        param_count = len(node.args.args)
        if param_count > 5:
            smells.append(f"long_params ({param_count} params)")

        # 3. Deep nesting (>4 levels)
        max_nesting = self._calculate_max_nesting(node)
        if max_nesting > 4:
            smells.append(f"deep_nesting ({max_nesting} levels)")

        # 4. High cyclomatic complexity (>10 branches)
        complexity = self._calculate_cyclomatic_complexity(node)
        if complexity > 10:
            smells.append(f"high_complexity ({complexity} branches)")

        return smells

    def _calculate_max_nesting(self, node: ast.AST) -> int:
        """Calculate maximum nesting depth."""
        max_depth = 0

        class NestingVisitor(ast.NodeVisitor):
            def __init__(self):
                self.current_depth = 0
                self.max_depth = 0

            def visit_If(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

            def visit_For(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

            def visit_While(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

            def visit_With(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

            def visit_Try(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

        visitor = NestingVisitor()
        visitor.visit(node)
        return visitor.max_depth

    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity (branch count)."""
        complexity = 1  # Base complexity

        class ComplexityVisitor(ast.NodeVisitor):
            def __init__(self):
                self.complexity = 1

            def visit_If(self, node):
                self.complexity += 1
                self.generic_visit(node)

            def visit_For(self, node):
                self.complexity += 1
                self.generic_visit(node)

            def visit_While(self, node):
                self.complexity += 1
                self.generic_visit(node)

            def visit_ExceptHandler(self, node):
                self.complexity += 1
                self.generic_visit(node)

            def visit_BoolOp(self, node):
                self.complexity += len(node.values) - 1
                self.generic_visit(node)

        visitor = ComplexityVisitor()
        visitor.visit(node)
        return visitor.complexity

    def _count_escape_hatches(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
        """Count cast() usage in function."""
        count = 0
        func_body = ast.unparse(node)
        count += func_body.count("cast(")
        return count

    def _detect_function_type(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """Detect function type based on context and content."""
        func_body = ast.unparse(node)
        path_str = str(self.filepath)
        func_name = node.name

        # Exclude false positives first
        # __init__ is never an API call
        if func_name == "__init__":
            return "service"

        # get_client/get_logger/get_config are getters, not API calls
        if func_name in (
            "get_client",
            "get_logger",
            "get_config",
            "load_bot_state",
            "save_bot_state",
        ):
            return "service"

        # CLI command
        if "src/commands/" in path_str or any(
            "@app.command" in ast.unparse(d) for d in node.decorator_list
        ):
            return "cli_command"

        # API call - must actually make HTTP requests, not just use client objects
        # Check for actual API call patterns, not just imports
        api_patterns = [
            ".submit(",  # reddit.subreddit().submit()
            ".create_release(",  # github create
            "gh api",  # gh CLI API calls
            "requests.get(",
            "requests.post(",
        ]
        if any(pattern in func_body for pattern in api_patterns):
            return "api_call"

        # File I/O
        if any(
            x in func_body
            for x in ["open(", "Path(", ".read(", ".write(", ".read_text", ".write_text"]
        ):
            return "file_io"

        # Parser
        if "parse" in node.name.lower() and not any(
            x in func_body for x in ["open(", "requests.", "praw."]
        ):
            return "parser"

        return "service"

    def _has_retry_decorator(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Check if function has @retry decorator."""
        return any("retry" in ast.unparse(d).lower() for d in node.decorator_list)

    def _returns_result_type(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Check if function returns Result[T, E]."""
        if node.returns:
            return_str = ast.unparse(node.returns)
            return "Result[" in return_str
        return False

    def _uses_error_context(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Check if function uses error_context()."""
        func_body = ast.unparse(node)
        return "error_context(" in func_body

    def _uses_get_logger(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Check if function uses get_logger()."""
        func_body = ast.unparse(node)
        return "get_logger(" in func_body or "logger." in func_body

    def _has_repo_validation(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Check if repo parameter validated with '/' check."""
        for dec in node.decorator_list:
            dec_str = ast.unparse(dec)
            if "deal.pre" in dec_str and ("/" in dec_str and "repo" in dec_str):
                return True
        return False

    def _is_thin_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Check if function is thin (<50 LOC)."""
        loc = (node.end_lineno or node.lineno) - node.lineno
        return loc < 50

    def _validate_api_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        has_retry: bool,
        returns_result: bool,
        has_repo_validation: bool,
    ) -> list[str]:
        """Validate API call function patterns."""
        violations = []
        if not has_retry:
            violations.append("missing_retry: API call without @retry decorator")
        if not returns_result:
            violations.append("missing_result: API call should return Result[T, E]")
        # Check for repo parameter
        has_repo_param = any(arg.arg == "repo" for arg in node.args.args)
        if has_repo_param and not has_repo_validation:
            violations.append(
                "missing_repo_validation: repo parameter not validated with '/' check"
            )
        return violations

    def _validate_file_io_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, returns_result: bool
    ) -> list[str]:
        """Validate file I/O function patterns."""
        violations: list[str] = []
        # Exclude getters and simple utility functions
        if node.name in ("get_logger", "get_config", "get_client"):
            return violations
        if not returns_result:
            violations.append("missing_result: File I/O should return Result[T, E]")
        return violations

    def _validate_cli_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        uses_error_context: bool,
        uses_logger: bool,
        is_thin: bool,
    ) -> list[str]:
        """Validate CLI command function patterns."""
        violations = []
        if not uses_error_context:
            violations.append("missing_error_context: CLI command should use error_context()")
        if not uses_logger:
            violations.append("missing_logger: CLI command should use get_logger()")
        if not is_thin:
            violations.append("not_thin: CLI command should be <50 LOC (orchestration only)")
        return violations

    def _validate_parser_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        has_deal_pre: bool,
        weak_types: list[str],
    ) -> list[str]:
        """Validate parser function patterns."""
        violations = []
        if not has_deal_pre:
            violations.append(
                "missing_contracts: Parser should have @deal.pre for input validation"
            )
        # Only flag weak types in return values, not config parameters
        weak_return_types = [wt for wt in weak_types if wt.startswith("return:")]
        if weak_return_types:
            violations.append("weak_types: Parser should use specific types, not Any")
        return violations

    def _calculate_architectural_score(
        self,
        func_type: str,
        has_retry: bool,
        returns_result: bool,
        uses_error_context: bool,
        uses_logger: bool,
        is_thin: bool,
        has_deal_pre: bool,
        weak_types: list[str],
    ) -> float:
        """Calculate architecture-aware score based on function type."""
        score = 0.0

        if func_type == "api_call":
            # API: 40% retry + 30% Result + 30% contracts
            if has_retry:
                score += 40
            if returns_result:
                score += 30
            if has_deal_pre:
                score += 30
        elif func_type == "file_io":
            # File I/O: 50% Result + 30% error handling + 20% contracts
            if returns_result:
                score += 50
            if has_deal_pre:
                score += 50
        elif func_type == "cli_command":
            # CLI: 40% thin + 30% error_context + 30% logger
            if is_thin:
                score += 40
            if uses_error_context:
                score += 30
            if uses_logger:
                score += 30
        elif func_type == "parser":
            # Parser: 50% contracts + 50% no Any
            if has_deal_pre:
                score += 50
            if not weak_types:
                score += 50
        else:  # service
            # Service: balanced
            if returns_result:
                score += 30
            if has_deal_pre:
                score += 35
            if not weak_types:
                score += 35

        return min(score, 100.0)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition."""
        self.classes += 1
        # Check if Pydantic model
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == "BaseModel":
                self.pydantic_models += 1
                break
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Visit function definition."""
        # Skip private functions
        if node.name.startswith("_") and node.name != "__init__":
            return

        # Analyze decorators
        has_beartype = False
        has_deal_pre = False
        has_deal_post = False
        has_deal_ensure = False
        has_deal_raises = False

        for dec in node.decorator_list:
            try:
                dec_str = ast.unparse(dec)
                if "beartype" in dec_str:
                    has_beartype = True
                if "deal.pre" in dec_str or "@pre" in dec_str:
                    has_deal_pre = True
                if "deal.post" in dec_str or "@post" in dec_str:
                    has_deal_post = True
                if "deal.ensure" in dec_str or "@ensure" in dec_str:
                    has_deal_ensure = True
                if "deal.raises" in dec_str or "@raises" in dec_str:
                    has_deal_raises = True
            except Exception:
                continue

        # Check type hints and detect weak typing (Any usage)
        has_type_hints = bool(node.returns) or any(arg.annotation for arg in node.args.args)

        weak_types = []
        if has_type_hints:
            # Check return type for Any
            if node.returns:
                return_str = ast.unparse(node.returns)
                if "Any" in return_str:
                    weak_types.append(f"return: {return_str}")

            # Check parameter types for Any
            for arg in node.args.args:
                if arg.annotation:
                    arg_str = ast.unparse(arg.annotation)
                    if "Any" in arg_str:
                        weak_types.append(f"{arg.arg}: {arg_str}")

        # Calculate type strength (0-100)
        # Penalize for Any usage, but less if justified
        type_strength = 100.0
        any_justified = True
        justification_reason = "No Any usage"

        if has_type_hints:
            if weak_types:
                any_justified, justification_reason = self._is_any_justified(node, weak_types)

                if any_justified:
                    # Justified Any: lose only 10 points per usage
                    penalty = min(len(weak_types) * 10, 40)
                else:
                    # Unjustified Any: lose 20 points per usage
                    penalty = min(len(weak_types) * 20, 80)

                type_strength -= penalty
        else:
            type_strength = 0.0
            justification_reason = "No type hints"

        # Count type: ignore in function
        func_start = node.lineno
        func_end = node.end_lineno or func_start
        func_lines = self.content.split("\n")[func_start - 1 : func_end]
        type_ignores = sum(line.count("# type: ignore") for line in func_lines)

        # Calculate validation score for this function
        # Now includes type strength penalty
        score = self._calculate_function_score(
            has_beartype,
            has_deal_pre,
            has_deal_post,
            has_deal_ensure,
            has_deal_raises,
            has_type_hints,
            type_strength,
        )

        # Calculate new sophisticated metrics
        type_complexity = self._calculate_type_complexity(node)
        validation_depth = self._calculate_validation_depth(node)
        code_smells = self._detect_code_smells(node)
        escape_hatches = self._count_escape_hatches(node)
        loc = (node.end_lineno or node.lineno) - node.lineno
        param_count = len(node.args.args)
        cyclomatic_complexity = self._calculate_cyclomatic_complexity(node)

        # NEW: Architecture-aware detection
        function_type = self._detect_function_type(node)
        has_retry = self._has_retry_decorator(node)
        returns_result = self._returns_result_type(node)
        uses_error_context = self._uses_error_context(node)
        uses_logger = self._uses_get_logger(node)
        has_repo_validation = self._has_repo_validation(node)
        is_thin = self._is_thin_function(node)

        # Validate based on function type
        architectural_violations = []
        if function_type == "api_call":
            architectural_violations = self._validate_api_function(
                node, has_retry, returns_result, has_repo_validation
            )
        elif function_type == "file_io":
            architectural_violations = self._validate_file_io_function(node, returns_result)
        elif function_type == "cli_command":
            architectural_violations = self._validate_cli_function(
                node, uses_error_context, uses_logger, is_thin
            )
        elif function_type == "parser":
            architectural_violations = self._validate_parser_function(
                node, has_deal_pre, weak_types
            )

        # Calculate architectural score
        architectural_score = self._calculate_architectural_score(
            function_type,
            has_retry,
            returns_result,
            uses_error_context,
            uses_logger,
            is_thin,
            has_deal_pre,
            weak_types,
        )

        func_val = FunctionValidation(
            name=node.name,
            line=node.lineno,
            has_beartype=has_beartype,
            has_deal_pre=has_deal_pre,
            has_deal_post=has_deal_post,
            has_deal_ensure=has_deal_ensure,
            has_deal_raises=has_deal_raises,
            has_type_hints=has_type_hints,
            type_ignores=type_ignores,
            validation_score=score,
            weak_types=weak_types,
            type_strength=type_strength,
            any_justified=any_justified,
            justification_reason=justification_reason,
            type_complexity=type_complexity,
            validation_depth=validation_depth,
            code_smells=code_smells,
            escape_hatches=escape_hatches,
            loc=loc,
            param_count=param_count,
            cyclomatic_complexity=cyclomatic_complexity,
            function_type=function_type,
            has_retry=has_retry,
            returns_result=returns_result,
            uses_error_context=uses_error_context,
            uses_logger=uses_logger,
            has_repo_validation=has_repo_validation,
            is_thin=is_thin,
            architectural_violations=architectural_violations,
            architectural_score=architectural_score,
        )

        self.functions.append(func_val)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definition."""
        self.visit_FunctionDef(node)

    def _calculate_function_score(
        self,
        beartype: bool,
        pre: bool,
        post: bool,
        ensure: bool,
        raises: bool,
        hints: bool,
        type_strength: float,
    ) -> float:
        """Calculate validation strength score (0-100)."""
        score = 0.0

        # Type hints are baseline, but penalized for Any usage
        if hints:
            # Base 20 points, but scaled by type strength
            score += 20 * (type_strength / 100.0)

        # Beartype provides runtime validation (30 points)
        if beartype:
            score += 30

        # Deal contracts provide business logic validation
        if pre:
            score += 15  # Preconditions
        if post:
            score += 15  # Postconditions
        if ensure:
            score += 10  # Invariants
        if raises:
            score += 10  # Exception contracts

        return min(score, 100.0)


def analyze_file(filepath: Path) -> FileStats | None:
    """Analyze a single file for validation tool usage."""
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=str(filepath))
        analyzer = ValidationAnalyzer(content, filepath)
        analyzer.visit(tree)

        # Calculate aggregates
        beartype_count = sum(1 for f in analyzer.functions if f.has_beartype)
        deal_pre_count = sum(1 for f in analyzer.functions if f.has_deal_pre)
        deal_post_count = sum(1 for f in analyzer.functions if f.has_deal_post)
        deal_ensure_count = sum(1 for f in analyzer.functions if f.has_deal_ensure)
        deal_raises_count = sum(1 for f in analyzer.functions if f.has_deal_raises)
        type_hints_count = sum(1 for f in analyzer.functions if f.has_type_hints)

        # Find unvalidated functions (score < 50)
        unvalidated = [f"{f.name}:{f.line}" for f in analyzer.functions if f.validation_score < 50]

        # Count functions with weak types
        weak_type_count = sum(1 for f in analyzer.functions if f.weak_types)
        justified_any_count = sum(1 for f in analyzer.functions if f.weak_types and f.any_justified)
        unjustified_any_count = sum(
            1 for f in analyzer.functions if f.weak_types and not f.any_justified
        )

        # Calculate average type strength
        if analyzer.functions:
            type_strength_score = sum(f.type_strength for f in analyzer.functions) / len(
                analyzer.functions
            )
        else:
            type_strength_score = 100.0

        # Calculate file integration score (average of function scores)
        if analyzer.functions:
            integration_score = sum(f.validation_score for f in analyzer.functions) / len(
                analyzer.functions
            )
        else:
            integration_score = 0.0

        # Count total type: ignore comments
        type_ignores = content.count("# type: ignore")

        # Calculate new sophisticated metrics
        avg_type_complexity = (
            sum(f.type_complexity for f in analyzer.functions) / len(analyzer.functions)
            if analyzer.functions
            else 0.0
        )
        avg_validation_depth = (
            sum(f.validation_depth for f in analyzer.functions) / len(analyzer.functions)
            if analyzer.functions
            else 0.0
        )
        total_code_smells = sum(len(f.code_smells) for f in analyzer.functions)
        total_escape_hatches = sum(f.escape_hatches for f in analyzer.functions)
        god_functions = [
            f.name for f in analyzer.functions if any("god_function" in s for s in f.code_smells)
        ]

        # Calculate architecture stats
        api_call_count = sum(1 for f in analyzer.functions if f.function_type == "api_call")
        file_io_count = sum(1 for f in analyzer.functions if f.function_type == "file_io")
        cli_command_count = sum(1 for f in analyzer.functions if f.function_type == "cli_command")
        parser_count = sum(1 for f in analyzer.functions if f.function_type == "parser")
        service_count = sum(1 for f in analyzer.functions if f.function_type == "service")

        return FileStats(
            path=str(filepath.relative_to("src")),
            functions=len(analyzer.functions),
            classes=analyzer.classes,
            pydantic_models=analyzer.pydantic_models,
            beartype_count=beartype_count,
            deal_pre_count=deal_pre_count,
            deal_post_count=deal_post_count,
            deal_ensure_count=deal_ensure_count,
            deal_raises_count=deal_raises_count,
            type_hints_count=type_hints_count,
            type_ignores=type_ignores,
            integration_score=integration_score,
            unvalidated_functions=unvalidated,
            validation_details=analyzer.functions,
            weak_type_count=weak_type_count,
            type_strength_score=type_strength_score,
            justified_any_count=justified_any_count,
            unjustified_any_count=unjustified_any_count,
            avg_type_complexity=avg_type_complexity,
            avg_validation_depth=avg_validation_depth,
            total_code_smells=total_code_smells,
            total_escape_hatches=total_escape_hatches,
            god_functions=god_functions,
            api_call_count=api_call_count,
            file_io_count=file_io_count,
            cli_command_count=cli_command_count,
            parser_count=parser_count,
            service_count=service_count,
        )

    except SyntaxError as e:
        print(f"⚠️  Syntax error in {filepath}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"⚠️  Error analyzing {filepath}: {e}", file=sys.stderr)
        return None


def generate_recommendations(stats: FileStats) -> list[str]:
    """Generate actionable recommendations for a file."""
    recommendations: list[str] = []

    if stats.functions == 0:
        return recommendations

    # Check for weak typing (Any abuse)
    if stats.weak_type_count > 0:
        weak_funcs = [f.name for f in stats.validation_details if f.weak_types]
        recommendations.append(
            f"Replace Any with specific types in {stats.weak_type_count} functions: {', '.join(weak_funcs[:3])}"
        )

    # Check beartype coverage
    beartype_pct = (stats.beartype_count / stats.functions) * 100
    if beartype_pct < 100:
        missing = stats.functions - stats.beartype_count
        recommendations.append(f"Add @beartype to {missing} functions for runtime type checking")

    # Check deal contracts
    if stats.deal_pre_count == 0 and stats.functions > 0:
        recommendations.append("Consider adding @deal.pre contracts for input validation")

    if stats.deal_post_count == 0 and stats.functions > 0:
        recommendations.append("Consider adding @deal.post contracts for output validation")

    # Check type hints
    if stats.type_hints_count < stats.functions:
        missing = stats.functions - stats.type_hints_count
        recommendations.append(f"Add type hints to {missing} functions")

    # Check for excessive type: ignore
    if stats.type_ignores > stats.functions * 2:
        recommendations.append(f"Reduce {stats.type_ignores} type: ignore comments")

    # Check unvalidated functions
    if stats.unvalidated_functions:
        recommendations.append(
            f"Improve validation for: {', '.join(f.split(':')[0] for f in stats.unvalidated_functions[:3])}"
        )

    return recommendations


def main() -> None:
    """Run comprehensive validation tool integration analysis."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze validation tool integration depth")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--min-score", type=float, default=0, help="Minimum score to display")
    args = parser.parse_args()

    src_dir = Path("src")
    all_stats: list[FileStats] = []

    # Analyze all files
    for filepath in sorted(src_dir.rglob("*.py")):
        if filepath.name == "__init__.py":
            continue

        stats = analyze_file(filepath)
        if stats and stats.integration_score >= args.min_score:
            all_stats.append(stats)

    if args.json:
        # JSON output for CI
        output = {
            "files": [asdict(s) for s in all_stats],
            "summary": {
                "total_files": len(all_stats),
                "total_functions": sum(s.functions for s in all_stats),
                "total_classes": sum(s.classes for s in all_stats),
                "pydantic_models": sum(s.pydantic_models for s in all_stats),
                "beartype_coverage": sum(s.beartype_count for s in all_stats),
                "deal_contracts": sum(
                    s.deal_pre_count + s.deal_post_count + s.deal_ensure_count + s.deal_raises_count
                    for s in all_stats
                ),
                "average_score": sum(s.integration_score for s in all_stats) / len(all_stats)
                if all_stats
                else 0,
            },
        }
        print(json.dumps(output, indent=2))
        return

    # Human-readable output
    print("=== VALIDATION TOOL INTEGRATION DEPTH ANALYSIS ===\n")

    # Overall metrics
    total_funcs = sum(s.functions for s in all_stats)
    total_beartype = sum(s.beartype_count for s in all_stats)
    total_deal = sum(
        s.deal_pre_count + s.deal_post_count + s.deal_ensure_count + s.deal_raises_count
        for s in all_stats
    )
    total_hints = sum(s.type_hints_count for s in all_stats)
    total_weak_types = sum(s.weak_type_count for s in all_stats)
    avg_type_strength = (
        sum(s.type_strength_score for s in all_stats) / len(all_stats) if all_stats else 0
    )

    print("📊 OVERALL METRICS")
    print(f"Files Analyzed: {len(all_stats)}")
    print(f"Total Functions: {total_funcs}")
    print(f"Total Classes: {sum(s.classes for s in all_stats)}")
    print(f"Pydantic Models: {sum(s.pydantic_models for s in all_stats)}\n")

    print("🔧 VALIDATION COVERAGE")
    print(f"@beartype: {total_beartype}/{total_funcs} ({total_beartype/total_funcs*100:.1f}%)")
    print(f"@deal contracts: {total_deal} total")
    print(f"  - @deal.pre: {sum(s.deal_pre_count for s in all_stats)}")
    print(f"  - @deal.post: {sum(s.deal_post_count for s in all_stats)}")
    print(f"  - @deal.ensure: {sum(s.deal_ensure_count for s in all_stats)}")
    print(f"  - @deal.raises: {sum(s.deal_raises_count for s in all_stats)}")
    print(f"Type Hints: {total_hints}/{total_funcs} ({total_hints/total_funcs*100:.1f}%)\n")

    print("⚠️  TYPE STRENGTH")
    print(
        f"Functions with Any: {total_weak_types}/{total_funcs} ({total_weak_types/total_funcs*100:.1f}%)"
    )

    total_justified = sum(s.justified_any_count for s in all_stats)
    total_unjustified = sum(s.unjustified_any_count for s in all_stats)

    print(f"  - Justified Any: {total_justified} (dynamic data, external APIs)")
    print(f"  - Unjustified Any: {total_unjustified} (should be specific types)")
    print(f"Average Type Strength: {avg_type_strength:.1f}/100")

    if total_unjustified > 0:
        print(f"⚠️  WARNING: {total_unjustified} functions have unjustified Any usage!")
    elif total_weak_types > 0:
        print(f"✅ All {total_weak_types} Any usages are justified (dynamic data)\n")
    else:
        print("✅ No Any usage - perfect type safety!\n")

    # NEW: Sophisticated metrics
    print("🔬 SOPHISTICATED ANALYSIS")

    # Type Complexity
    avg_type_complexity = (
        sum(s.avg_type_complexity for s in all_stats) / len(all_stats) if all_stats else 0
    )
    print(f"Average Type Complexity: {avg_type_complexity:.1f} (nesting depth)")
    complex_types = sum(1 for s in all_stats for f in s.validation_details if f.type_complexity > 3)
    if complex_types > 0:
        print(f"  ⚠️  {complex_types} functions with deeply nested types (>3 levels)")

    # Validation Depth
    avg_validation_depth = (
        sum(s.avg_validation_depth for s in all_stats) / len(all_stats) if all_stats else 0
    )
    print(f"Average Validation Depth: {avg_validation_depth:.1f}% (parameter coverage)")
    weak_contracts = sum(
        1 for s in all_stats for f in s.validation_details if f.validation_depth < 50
    )
    if weak_contracts > 0:
        print(f"  ⚠️  {weak_contracts} functions with weak contracts (<50% param coverage)")

    # Code Smells
    total_smells = sum(s.total_code_smells for s in all_stats)
    print(f"Code Smells Detected: {total_smells}")
    if total_smells > 0:
        god_funcs = sum(len(s.god_functions) for s in all_stats)
        if god_funcs > 0:
            print(f"  ⚠️  {god_funcs} god functions (>50 LOC or >10 branches)")

    # Escape Hatches
    total_casts = sum(s.total_escape_hatches for s in all_stats)
    print(f"Escape Hatches (cast): {total_casts}")
    if total_casts > 0:
        print(f"  ⚠️  {total_casts} cast() usages bypass type checking")

    print()

    # NEW: Architectural compliance report
    print("🏗️  ARCHITECTURAL COMPLIANCE\n")

    # Function type distribution
    total_api = sum(s.api_call_count for s in all_stats)
    total_file_io = sum(s.file_io_count for s in all_stats)
    total_cli = sum(s.cli_command_count for s in all_stats)
    total_parser = sum(s.parser_count for s in all_stats)
    total_service = sum(s.service_count for s in all_stats)

    print("Function Type Distribution:")
    print(f"  API Calls: {total_api}")
    print(f"  File I/O: {total_file_io}")
    print(f"  CLI Commands: {total_cli}")
    print(f"  Parsers: {total_parser}")
    print(f"  Services: {total_service}\n")

    # Pattern compliance
    all_funcs_list = [f for s in all_stats for f in s.validation_details]

    # Retry compliance (API calls)
    api_funcs = [f for f in all_funcs_list if f.function_type == "api_call"]
    if api_funcs:
        retry_compliance = sum(1 for f in api_funcs if f.has_retry) / len(api_funcs) * 100
        print(
            f"Retry Pattern Compliance: {retry_compliance:.1f}% ({sum(1 for f in api_funcs if f.has_retry)}/{len(api_funcs)} API calls)"
        )
        if retry_compliance < 100:
            print(
                f"  ⚠️  {len(api_funcs) - sum(1 for f in api_funcs if f.has_retry)} API calls missing @retry"
            )

    # Result type compliance
    result_funcs = sum(1 for f in all_funcs_list if f.returns_result)
    result_compliance = result_funcs / len(all_funcs_list) * 100 if all_funcs_list else 0
    print(
        f"Result Type Usage: {result_compliance:.1f}% ({result_funcs}/{len(all_funcs_list)} functions)"
    )

    # Error context compliance (CLI commands)
    cli_funcs = [f for f in all_funcs_list if f.function_type == "cli_command"]
    if cli_funcs:
        error_ctx_compliance = (
            sum(1 for f in cli_funcs if f.uses_error_context) / len(cli_funcs) * 100
        )
        print(
            f"Error Context Usage: {error_ctx_compliance:.1f}% ({sum(1 for f in cli_funcs if f.uses_error_context)}/{len(cli_funcs)} CLI commands)"
        )
        if error_ctx_compliance < 100:
            print(
                f"  ⚠️  {len(cli_funcs) - sum(1 for f in cli_funcs if f.uses_error_context)} CLI commands missing error_context()"
            )

    # Logger compliance (CLI commands)
    if cli_funcs:
        logger_compliance = sum(1 for f in cli_funcs if f.uses_logger) / len(cli_funcs) * 100
        print(
            f"Logger Usage: {logger_compliance:.1f}% ({sum(1 for f in cli_funcs if f.uses_logger)}/{len(cli_funcs)} CLI commands)"
        )

    # Thin CLI compliance
    if cli_funcs:
        thin_compliance = sum(1 for f in cli_funcs if f.is_thin) / len(cli_funcs) * 100
        print(
            f"Thin CLI Commands: {thin_compliance:.1f}% ({sum(1 for f in cli_funcs if f.is_thin)}/{len(cli_funcs)} <50 LOC)"
        )

    print()

    # NEW: Architectural violations report
    all_violations = [
        (s.path, f.name, f.line, f.architectural_violations)
        for s in all_stats
        for f in s.validation_details
        if f.architectural_violations
    ]

    if all_violations:
        print("❌ ARCHITECTURAL VIOLATIONS\n")

        # Group by violation type
        violation_groups: dict[str, list[tuple[str, str, int]]] = {}
        for path, name, line, violations in all_violations:
            for v in violations:
                v_type = v.split(":")[0]
                if v_type not in violation_groups:
                    violation_groups[v_type] = []
                violation_groups[v_type].append((path, name, line))

        # Violation fix guidance
        fix_guidance = {
            "missing_retry": "Add @retry(retry=retry_if_result(should_retry_api_error), stop=stop_after_attempt(3), wait=wait_exponential())",
            "missing_result": "Change return type to Result[T, ErrorType] and wrap returns in Ok()/Err()",
            "missing_repo_validation": 'Add @deal.pre(lambda repo, **_: "/" in repo, message="Repository must be in owner/name format")',
            "missing_error_context": "Wrap main logic in: with error_context('operation description', ...): ...",
            "missing_logger": "Add: logger = get_logger(__name__) and use logger.info/error instead of print()",
            "not_thin": "Move business logic to service layer (gh/, reddit/, core/), keep CLI as orchestration only",
            "missing_contracts": "Add @deal.pre for input validation and @deal.post for output validation",
            "weak_types": "Replace Any with specific types (TypedDict, dataclass, or concrete types)",
        }

        for v_type, occurrences in sorted(
            violation_groups.items(), key=lambda x: len(x[1]), reverse=True
        ):
            print(f"{v_type.upper().replace('_', ' ')} ({len(occurrences)} occurrences)")
            print(f"  Fix: {fix_guidance.get(v_type, 'Review function implementation')}")
            for path, name, line in occurrences[:5]:  # Show first 5
                print(f"    • {path}:{line} - {name}()")
            if len(occurrences) > 5:
                print(f"    ... and {len(occurrences) - 5} more")
            print()

    # File-by-file analysis
    print("📁 FILE INTEGRATION SCORES\n")

    for stats in sorted(all_stats, key=lambda s: s.integration_score, reverse=True):
        if stats.functions == 0:
            continue

        score = stats.integration_score
        status = "🟢" if score >= 80 else "🟡" if score >= 50 else "🔴"

        print(f"{status} {stats.path} (score: {score:.1f}/100)")
        print(
            f"   Functions: {stats.functions} | @beartype: {stats.beartype_count} | "
            f"@deal: {stats.deal_pre_count + stats.deal_post_count + stats.deal_ensure_count + stats.deal_raises_count} | "
            f"Type hints: {stats.type_hints_count}"
        )

        # Show weak types warning with justification
        if stats.weak_type_count > 0:
            if stats.unjustified_any_count > 0:
                print(f"   ⚠️  Unjustified Any: {stats.unjustified_any_count} functions")
            if stats.justified_any_count > 0:
                print(f"   ℹ️  Justified Any: {stats.justified_any_count} functions (dynamic data)")

        # Show recommendations for low-scoring files
        if score < 80:
            recs = generate_recommendations(stats)
            if recs:
                print(f"   💡 {recs[0]}")

        if stats.unvalidated_functions:
            print(f'   ⚠️  Unvalidated: {", ".join(stats.unvalidated_functions[:3])}')

    # Overall score
    avg_score = sum(s.integration_score for s in all_stats) / len(all_stats) if all_stats else 0

    print(f"\n🎯 OVERALL INTEGRATION SCORE: {avg_score:.1f}/100")

    if avg_score >= 80:
        print("✅ Excellent integration depth")
    elif avg_score >= 50:
        print("⚠️  Moderate integration depth - improvements recommended")
    else:
        print("❌ Low integration depth - significant improvements needed")

    # Top recommendations
    print("\n💡 TOP RECOMMENDATIONS")
    all_recs: dict[str, int] = {}
    for stats in all_stats:
        for rec in generate_recommendations(stats):
            all_recs[rec] = all_recs.get(rec, 0) + 1

    for rec, count in sorted(all_recs.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  • {rec} ({count} files)")


if __name__ == "__main__":
    main()
