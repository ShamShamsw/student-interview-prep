# Mini-Project 04: Stack-Based Calculator

**Time:** 1–1.5 hours  
**Difficulty:** Medium  
**Concepts:** Stack data structure, parsing, expression evaluation, Reverse Polish Notation

---

## Objective

Build a calculator that evaluates mathematical expressions using a stack. This combines two common interview topics: stack usage and expression parsing.

## Requirements

### Part 1: RPN (Reverse Polish Notation) Evaluator

Evaluate expressions in postfix notation where operators come after their operands.

```python
calc = RPNCalculator()

calc.evaluate("3 4 +")           # 7
calc.evaluate("3 4 + 2 *")       # 14  → (3 + 4) * 2
calc.evaluate("5 1 2 + 4 * + 3 -")  # 14  → 5 + ((1 + 2) * 4) - 3
calc.evaluate("10 2 /")          # 5.0
```

### Part 2: Infix to Postfix Converter

Convert standard infix notation to postfix, respecting operator precedence and parentheses.

```python
to_postfix("3 + 4")             # "3 4 +"
to_postfix("3 + 4 * 2")         # "3 4 2 * +"  (multiplication first)
to_postfix("( 3 + 4 ) * 2")     # "3 4 + 2 *"
```

### Part 3: Full Calculator

Combine both parts so users can type normal expressions and get results.

```python
calc = Calculator()
calc.calculate("3 + 4 * 2")     # 11
calc.calculate("( 3 + 4 ) * 2") # 14
calc.calculate("10 / 3")        # 3.333...
```

## Approach

### RPN Evaluator (Shunting-yard output)
1. Split the expression into tokens
2. For each token:
   - If it's a number, push onto the stack
   - If it's an operator, pop two operands, apply the operator, push the result
3. The final item on the stack is the answer

### Infix to Postfix (Shunting-yard algorithm)
1. Maintain an output queue and an operator stack
2. For each token:
   - Number → add to output
   - `(` → push to operator stack
   - `)` → pop operators to output until `(` is found
   - Operator → pop higher-precedence operators to output, then push current operator
3. Pop remaining operators to output

## Hints

<details>
<summary>Hint 1: Operator precedence</summary>

```python
PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
```
</details>

<details>
<summary>Hint 2: RPN evaluation core</summary>

```python
def evaluate_rpn(tokens):
    stack = []
    for token in tokens:
        if token in '+-*/':
            b, a = stack.pop(), stack.pop()  # Note: b is popped first
            stack.append(apply_op(a, b, token))
        else:
            stack.append(float(token))
    return stack[0]
```
</details>

<details>
<summary>Hint 3: Division by zero</summary>

Don't forget to handle division by zero gracefully — raise a clear error message.
</details>

## Tests to Write

```python
def test_rpn_addition():
    calc = RPNCalculator()
    assert calc.evaluate("3 4 +") == 7

def test_rpn_complex():
    calc = RPNCalculator()
    assert calc.evaluate("5 1 2 + 4 * + 3 -") == 14

def test_infix_to_postfix_precedence():
    assert to_postfix("3 + 4 * 2") == "3 4 2 * +"

def test_infix_to_postfix_parentheses():
    assert to_postfix("( 3 + 4 ) * 2") == "3 4 + 2 *"

def test_calculator_basic():
    calc = Calculator()
    assert calc.calculate("3 + 4 * 2") == 11

def test_division_by_zero():
    calc = RPNCalculator()
    with pytest.raises(ZeroDivisionError):
        calc.evaluate("5 0 /")

def test_negative_numbers():
    calc = Calculator()
    assert calc.calculate("10 - 15") == -5
```

## Stretch Goals

1. Support unary negation (`-5 + 3`) and exponentiation (`2 ^ 10`)
2. Add a REPL loop where the user can type expressions interactively
3. Support variables: `x = 5` then `x + 3` → 8
4. Add a `history` feature that shows previous calculations
