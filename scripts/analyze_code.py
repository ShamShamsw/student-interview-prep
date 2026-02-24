#!/usr/bin/env python3
"""Code Quality Analyzer for Interview Solutions.

Analyzes solution code for:
- Time complexity
- Space complexity
- Code style and readability
- Best practices
- Optimization opportunities

Usage:
    python scripts/analyze_code.py solutions/01-two-sum.py
    python scripts/analyze_code.py solutions/ --all
    python scripts/analyze_code.py solutions/15-valid-palindrome.py --detailed
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

# Color codes
COLORS = {
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


def colorize(text: str, color: str) -> str:
    """Apply color to text."""
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"


class CodeAnalyzer:
    """Analyze code quality and complexity."""

    def __init__(self):
        """Initialize analyzer."""
        self.issues = []
        self.suggestions = []
        self.complexity_score = 0
    
    def analyze_file(self, file_path: Path) -> dict[str, Any]:
        """Analyze a Python file."""
        try:
            code = file_path.read_text(encoding="utf-8")
            tree = ast.parse(code)
            
            analysis = {
                "file": str(file_path),
                "lines": len(code.split("\n")),
                "functions": self._count_functions(tree),
                "classes": self._count_classes(tree),
                "complexity": self._analyze_complexity(tree, code),
                "style": self._analyze_style(code),
                "documentation": self._analyze_documentation(tree, code),
                "best_practices": self._check_best_practices(tree, code),
                "score": 0,
            }
            
            # Calculate overall score
            analysis["score"] = self._calculate_score(analysis)
            
            return analysis
        
        except Exception as e:
            return {"error": str(e), "file": str(file_path)}
    
    def _count_functions(self, tree: ast.AST) -> int:
        """Count function definitions."""
        return sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
    
    def _count_classes(self, tree: ast.AST) -> int:
        """Count class definitions."""
        return sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
    
    def _analyze_complexity(self, tree: ast.AST, code: str) -> dict[str, Any]:
        """Analyze time and space complexity."""
        complexity = {
            "time": "Unknown",
            "space": "Unknown",
            "cyclomatic": self._calculate_cyclomatic(tree),
            "nested_loops": self._count_nested_loops(tree),
            "recursion": self._has_recursion(tree),
        }
        
        # Try to detect complexity from code
        complexity["time"] = self._estimate_time_complexity(tree, code)
        complexity["space"] = self._estimate_space_complexity(tree, code)
        
        return complexity
    
    def _calculate_cyclomatic(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _count_nested_loops(self, tree: ast.AST) -> int:
        """Count maximum nesting level of loops."""
        max_depth = 0
        
        def count_depth(node: ast.AST, current_depth: int = 0) -> int:
            depth = current_depth
            if isinstance(node, (ast.For, ast.While)):
                depth += 1
            
            max_found = depth
            for child in ast.iter_child_nodes(node):
                child_depth = count_depth(child, depth)
                max_found = max(max_found, child_depth)
            
            return max_found
        
        return count_depth(tree)
    
    def _has_recursion(self, tree: ast.AST) -> bool:
        """Check if code uses recursion."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                # Check if function calls itself
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name) and child.func.id == func_name:
                            return True
        return False
    
    def _estimate_time_complexity(self, tree: ast.AST, code: str) -> str:
        """Estimate time complexity."""
        # Check for common patterns
        nested_loops = self._count_nested_loops(tree)
        
        if nested_loops >= 3:
            return "O(n³) or worse"
        elif nested_loops == 2:
            return "O(n²)"
        elif nested_loops == 1:
            # Check for binary search pattern
            if "//2" in code or "left" in code and "right" in code:
                return "O(n log n) or O(n)"
            return "O(n)"
        elif self._has_recursion(tree):
            return "O(2ⁿ) or O(n)"
        else:
            return "O(1) or O(n)"
    
    def _estimate_space_complexity(self, tree: ast.AST, code: str) -> str:
        """Estimate space complexity."""
        # Simple heuristic based on data structure usage
        if "dict" in code.lower() or "set" in code.lower():
            return "O(n)"
        elif self._has_recursion(tree):
            return "O(n) recursion stack"
        else:
            return "O(1)"
    
    def _analyze_style(self, code: str) -> dict[str, Any]:
        """Analyze code style."""
        lines = code.split("\n")
        
        style = {
            "avg_line_length": sum(len(line) for line in lines) / len(lines) if lines else 0,
            "long_lines": sum(1 for line in lines if len(line) > 100),
            "blank_lines": sum(1 for line in lines if not line.strip()),
            "comments": sum(1 for line in lines if line.strip().startswith("#")),
        }
        
        # Check naming conventions
        snake_case = len(re.findall(r"\bdef [a-z_]+\(", code))
        camel_case = len(re.findall(r"\bdef [a-z][A-Za-z]+\(", code))
        
        style["naming"] = "snake_case" if snake_case > camel_case else "camelCase"
        
        return style
    
    def _analyze_documentation(self, tree: ast.AST, code: str) -> dict[str, Any]:
        """Analyze documentation quality."""
        doc = {
            "has_module_docstring": ast.get_docstring(tree) is not None,
            "function_docstrings": 0,
            "total_functions": 0,
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                doc["total_functions"] += 1
                if ast.get_docstring(node):
                    doc["function_docstrings"] += 1
        
        if doc["total_functions"] > 0:
            doc["docstring_coverage"] = doc["function_docstrings"] / doc["total_functions"] * 100
        else:
            doc["docstring_coverage"] = 100
        
        return doc
    
    def _check_best_practices(self, tree: ast.AST, code: str) -> list[str]:
        """Check for best practices."""
        practices = []
        
        # Check for list comprehensions vs loops
        list_comps = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ListComp))
        if list_comps > 0:
            practices.append("✅ Uses list comprehensions")
        
        # Check for type hints
        has_annotations = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.returns:
                has_annotations = True
                break
        
        if has_annotations:
            practices.append("✅ Uses type hints")
        else:
            practices.append("⚠️  Consider adding type hints")
        
        # Check for magic numbers
        magic_numbers = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Num) and not isinstance(node.n, bool):
                if node.n not in [0, 1, -1, 2]:  # Common acceptable numbers
                    magic_numbers.append(node.n)
        
        if magic_numbers:
            practices.append(f"⚠️  Magic numbers found: {set(magic_numbers)}")
        
        # Check for early returns
        if "return" in code:
            practices.append("✅ Uses early returns")
        
        return practices
    
    def _calculate_score(self, analysis: dict[str, Any]) -> int:
        """Calculate overall quality score (0-100)."""
        score = 100
        
        # Deduct for issues
        if analysis["complexity"]["cyclomatic"] > 10:
            score -= 10
        elif analysis["complexity"]["cyclomatic"] > 5:
            score -= 5
        
        if analysis["complexity"]["nested_loops"] > 2:
            score -= 15
        
        if analysis["style"]["long_lines"] > 5:
            score -= 10
        
        if analysis["documentation"]["docstring_coverage"] < 50:
            score -= 15
        elif analysis["documentation"]["docstring_coverage"] < 80:
            score -= 5
        
        return max(0, score)
    
    def display_analysis(self, analysis: dict[str, Any], detailed: bool = False) -> None:
        """Display analysis results."""
        if "error" in analysis:
            print(colorize(f"❌ Error analyzing {analysis['file']}: {analysis['error']}", "red"))
            return
        
        print(colorize(f"\n📊 CODE ANALYSIS: {Path(analysis['file']).name}\n", "bold"))
        print("=" * 70)
        
        # Overall score
        score = analysis["score"]
        score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
        print(colorize(f"\n🎯 Quality Score: {score}/100", score_color))
        
        # Basic metrics
        print(colorize("\n📈 Metrics:", "cyan"))
        print(f"   Lines of Code: {analysis['lines']}")
        print(f"   Functions: {analysis['functions']}")
        print(f"   Classes: {analysis['classes']}")
        
        # Complexity
        print(colorize("\n⚙️  Complexity:", "cyan"))
        comp = analysis["complexity"]
        print(f"   Time: {comp['time']}")
        print(f"   Space: {comp['space']}")
        print(f"   Cyclomatic: {comp['cyclomatic']}")
        print(f"   Max Loop Nesting: {comp['nested_loops']}")
        print(f"   Uses Recursion: {'Yes' if comp['recursion'] else 'No'}")
        
        if detailed:
            # Style
            print(colorize("\n🎨 Style:", "cyan"))
            style = analysis["style"]
            print(f"   Avg Line Length: {style['avg_line_length']:.1f}")
            print(f"   Long Lines (>100 chars): {style['long_lines']}")
            print(f"   Comments: {style['comments']}")
            print(f"   Naming Convention: {style['naming']}")
            
            # Documentation
            print(colorize("\n📚 Documentation:", "cyan"))
            doc = analysis["documentation"]
            print(f"   Module Docstring: {'✅' if doc['has_module_docstring'] else '❌'}")
            print(f"   Function Docstrings: {doc['function_docstrings']}/{doc['total_functions']}")
            print(f"   Coverage: {doc['docstring_coverage']:.0f}%")
        
        # Best practices
        print(colorize("\n✨ Best Practices:", "cyan"))
        for practice in analysis["best_practices"]:
            print(f"   {practice}")
        
        print("\n" + "=" * 70)
        print()


def main() -> None:
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze code quality")
    parser.add_argument("path", help="File or directory to analyze")
    parser.add_argument("--all", "-a", action="store_true", help="Analyze all files in directory")
    parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed analysis")
    
    args = parser.parse_args()
    
    analyzer = CodeAnalyzer()
    path = Path(args.path)
    
    if path.is_file():
        analysis = analyzer.analyze_file(path)
        analyzer.display_analysis(analysis, detailed=args.detailed)
    elif path.is_dir() and args.all:
        for py_file in path.glob("**/*.py"):
            if "__pycache__" not in str(py_file):
                analysis = analyzer.analyze_file(py_file)
                analyzer.display_analysis(analysis, detailed=args.detailed)
    else:
        print(colorize("❌ Invalid path or missing --all flag for directory", "red"))


if __name__ == "__main__":
    main()
