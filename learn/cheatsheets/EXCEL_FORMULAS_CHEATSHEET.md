# Excel Formulas Cheatsheet

> A comprehensive reference for Excel formulas used in data analysis — organized by category with syntax, examples, and Python/pandas equivalents.

---

## Table of Contents

1. [Lookup & Reference](#lookup--reference)
2. [Logical Functions](#logical-functions)
3. [Math & Statistics](#math--statistics)
4. [Conditional Aggregation](#conditional-aggregation)
5. [Text / String Functions](#text--string-functions)
6. [Date & Time](#date--time)
7. [Array & Dynamic Array Functions](#array--dynamic-array-functions)
8. [Database Functions (D-functions)](#database-functions-d-functions)
9. [Information Functions](#information-functions)
10. [Financial Functions](#financial-functions)
11. [Common Patterns & Combos](#common-patterns--combos)
12. [Power Query M Language Basics](#power-query-m-language-basics)

---

## Lookup & Reference

| Formula | Syntax | Description | Python Equivalent |
|---|---|---|---|
| `VLOOKUP` | `=VLOOKUP(key, range, col_num, FALSE)` | Look up key in first column of range, return value from col_num | `df.merge(lookup, on='key')` |
| `HLOOKUP` | `=HLOOKUP(key, range, row_num, FALSE)` | Like VLOOKUP but searches horizontally | `df.T.merge(...)` |
| `XLOOKUP` | `=XLOOKUP(key, lookup_array, return_array, "N/A")` | Modern lookup with flexible match modes | `df.merge(lookup, on='key', how='left')` |
| `INDEX` | `=INDEX(range, row, col)` | Return value at position | `df.iloc[row, col]` |
| `MATCH` | `=MATCH(key, range, 0)` | Return position of key in range | `df['col'].tolist().index(key)` |
| `INDEX+MATCH` | `=INDEX(return_range, MATCH(key, lookup_range, 0))` | Flexible two-way lookup | `df.set_index('key')['col'][key]` |
| `OFFSET` | `=OFFSET(ref, rows, cols, height, width)` | Return a range offset from a reference | `df.iloc[start:end]` |
| `INDIRECT` | `=INDIRECT("Sheet1!A1")` | Return value from a text-constructed reference | Dynamic `df[col_name]` |
| `CHOOSE` | `=CHOOSE(idx, val1, val2, val3)` | Select value by index | `[val1, val2, val3][idx-1]` |

### VLOOKUP vs. XLOOKUP
```
VLOOKUP (legacy):
=VLOOKUP(A2, $E$2:$G$100, 2, FALSE)
- Key must be in the FIRST column
- Returns error if key not found (wrap in IFERROR)
- col_num is positional — breaks if you insert columns

XLOOKUP (recommended):
=XLOOKUP(A2, $E$2:$E$100, $F$2:$F$100, "Not found", 0)
- Key can be in ANY column
- Built-in "if not found" argument
- Works left-to-right AND right-to-left
- Returns arrays natively
```

---

## Logical Functions

| Formula | Syntax | Description |
|---|---|---|
| `IF` | `=IF(condition, value_if_true, value_if_false)` | Conditional value |
| `IFS` | `=IFS(cond1, val1, cond2, val2, ...)` | Multiple conditions (no nesting) |
| `AND` | `=AND(cond1, cond2, ...)` | TRUE if all conditions are true |
| `OR` | `=OR(cond1, cond2, ...)` | TRUE if any condition is true |
| `NOT` | `=NOT(condition)` | Invert a boolean |
| `IFERROR` | `=IFERROR(expr, value_if_error)` | Catch errors, return fallback |
| `IFNA` | `=IFNA(expr, value_if_na)` | Catch only #N/A errors |
| `SWITCH` | `=SWITCH(expr, val1, result1, val2, result2, default)` | Match-case style logic |
| `XOR` | `=XOR(cond1, cond2)` | TRUE if an odd number of conditions are true |

```
Nested IF (avoid beyond 2 levels — use IFS or SWITCH instead):
=IF(A2>=90, "A", IF(A2>=80, "B", IF(A2>=70, "C", "F")))

IFS equivalent (cleaner):
=IFS(A2>=90, "A", A2>=80, "B", A2>=70, "C", TRUE, "F")

SWITCH equivalent:
=SWITCH(TRUE, A2>=90, "A", A2>=80, "B", A2>=70, "C", "F")
```

---

## Math & Statistics

| Formula | Description | Python Equivalent |
|---|---|---|
| `SUM(range)` | Sum of all values | `df['col'].sum()` |
| `AVERAGE(range)` | Arithmetic mean | `df['col'].mean()` |
| `MEDIAN(range)` | Middle value | `df['col'].median()` |
| `MODE.SNGL(range)` | Most frequent value | `df['col'].mode()[0]` |
| `MIN(range)` | Minimum value | `df['col'].min()` |
| `MAX(range)` | Maximum value | `df['col'].max()` |
| `COUNT(range)` | Count non-empty numeric cells | `df['col'].count()` |
| `COUNTA(range)` | Count all non-empty cells | `df['col'].notna().sum()` |
| `COUNTBLANK(range)` | Count empty cells | `df['col'].isna().sum()` |
| `STDEV.S(range)` | Sample standard deviation | `df['col'].std()` |
| `STDEV.P(range)` | Population standard deviation | `df['col'].std(ddof=0)` |
| `VAR.S(range)` | Sample variance | `df['col'].var()` |
| `PRODUCT(range)` | Multiply all values | `df['col'].prod()` |
| `ABS(n)` | Absolute value | `abs(n)` |
| `ROUND(n, places)` | Round to n decimal places | `round(n, places)` |
| `ROUNDUP(n, places)` | Always round up | `math.ceil(n * 10**p) / 10**p` |
| `ROUNDDOWN(n, places)` | Always round down | `math.floor(n * 10**p) / 10**p` |
| `INT(n)` | Floor to integer | `int(n)` |
| `MOD(n, divisor)` | Remainder | `n % divisor` |
| `POWER(n, exp)` | Exponentiation | `n ** exp` |
| `SQRT(n)` | Square root | `n ** 0.5` |
| `LOG(n, base)` | Logarithm | `math.log(n, base)` |
| `LN(n)` | Natural logarithm | `math.log(n)` |
| `EXP(n)` | e raised to n | `math.exp(n)` |
| `PERCENTILE.INC(range, k)` | kth percentile (0–1) | `df['col'].quantile(k)` |
| `QUARTILE.INC(range, q)` | Quartile (q = 1,2,3,4) | `df['col'].quantile(q/4)` |
| `RANK.EQ(val, range, order)` | Rank with ties equal | `df['col'].rank(method='min')` |
| `LARGE(range, k)` | kth largest value | `df['col'].nlargest(k).iloc[-1]` |
| `SMALL(range, k)` | kth smallest value | `df['col'].nsmallest(k).iloc[-1]` |
| `CORREL(range1, range2)` | Pearson correlation (-1 to 1) | `df['a'].corr(df['b'])` |

---

## Conditional Aggregation

These are the workhorses of Excel data analysis.

| Formula | Syntax | Description | SQL Equivalent |
|---|---|---|---|
| `COUNTIF` | `=COUNTIF(range, criteria)` | Count matching cells | `COUNT(CASE WHEN ... THEN 1 END)` |
| `COUNTIFS` | `=COUNTIFS(r1, c1, r2, c2, ...)` | Count with multiple criteria | `COUNT(CASE WHEN ... AND ... THEN 1 END)` |
| `SUMIF` | `=SUMIF(range, criteria, sum_range)` | Sum where condition is met | `SUM(CASE WHEN ... THEN val END)` |
| `SUMIFS` | `=SUMIFS(sum_range, r1, c1, r2, c2)` | Sum with multiple criteria | `SUM(CASE WHEN ... AND ... THEN val END)` |
| `AVERAGEIF` | `=AVERAGEIF(range, criteria, avg_range)` | Average where condition is met | `AVG(CASE WHEN ... THEN val END)` |
| `AVERAGEIFS` | `=AVERAGEIFS(avg_range, r1, c1, r2, c2)` | Average with multiple criteria | `AVG(CASE WHEN ... AND ... THEN val END)` |
| `MAXIFS` | `=MAXIFS(max_range, r1, c1, ...)` | Max with criteria | `MAX(CASE WHEN ... THEN val END)` |
| `MINIFS` | `=MINIFS(min_range, r1, c1, ...)` | Min with criteria | `MIN(CASE WHEN ... THEN val END)` |

```
Examples:
=COUNTIF(B2:B100, "Sales")              → count Sales dept rows
=COUNTIF(C2:C100, ">50000")             → count salaries > 50,000
=COUNTIFS(B2:B100, "Sales", D2:D100, "West") → Sales dept AND West region

=SUMIF(B2:B100, "Q1", C2:C100)         → sum revenue for Q1
=SUMIFS(C2:C100, B2:B100, "Sales", D2:D100, "West") → Sales + West revenue

=AVERAGEIF(B2:B100, ">0", C2:C100)     → avg revenue for positive rows

Wildcard criteria:
=COUNTIF(A2:A100, "Smith*")            → names starting with Smith
=COUNTIF(A2:A100, "*Ltd")              → names ending with Ltd
=COUNTIF(A2:A100, "???")               → exactly 3 characters
```

---

## Text / String Functions

| Formula | Description | Python Equivalent |
|---|---|---|
| `LEN(text)` | Length of string | `len(s)` |
| `LEFT(text, n)` | First n characters | `s[:n]` |
| `RIGHT(text, n)` | Last n characters | `s[-n:]` |
| `MID(text, start, n)` | n chars from position start | `s[start-1:start-1+n]` |
| `UPPER(text)` | Uppercase | `s.upper()` |
| `LOWER(text)` | Lowercase | `s.lower()` |
| `PROPER(text)` | Title Case | `s.title()` |
| `TRIM(text)` | Remove extra spaces | `s.strip()` |
| `CLEAN(text)` | Remove non-printable chars | `''.join(c for c in s if c.isprintable())` |
| `CONCATENATE(a, b)` | Join strings (legacy) | `a + b` |
| `CONCAT(a, b, c)` | Join strings modern | `''.join([a,b,c])` |
| `TEXTJOIN(delim, ignore_empty, ...)` | Join with delimiter | `delim.join(...)` |
| `FIND(substring, text)` | Position of substring (case-sensitive) | `s.find(sub) + 1` |
| `SEARCH(substring, text)` | Position (case-insensitive) | `s.lower().find(sub.lower()) + 1` |
| `SUBSTITUTE(text, old, new, n)` | Replace nth occurrence of old with new | `s.replace(old, new, n)` |
| `REPLACE(text, start, n, new)` | Replace n chars from position start | `s[:start-1] + new + s[start-1+n:]` |
| `REPT(text, n)` | Repeat string n times | `s * n` |
| `EXACT(a, b)` | Case-sensitive string comparison | `a == b` |
| `TEXT(value, format)` | Format number as text | `f'{value:,.2f}'` |
| `VALUE(text)` | Convert text to number | `float(s)` |
| `NUMBERVALUE(text, dec, grp)` | Convert text with locale separators | `float(s.replace(',',''))` |

---

## Date & Time

| Formula | Description | Python Equivalent |
|---|---|---|
| `TODAY()` | Current date | `datetime.date.today()` |
| `NOW()` | Current date and time | `datetime.datetime.now()` |
| `DATE(y, m, d)` | Construct a date | `datetime.date(y, m, d)` |
| `TIME(h, m, s)` | Construct a time | `datetime.time(h, m, s)` |
| `YEAR(date)` | Year component | `d.year` |
| `MONTH(date)` | Month component (1–12) | `d.month` |
| `DAY(date)` | Day component | `d.day` |
| `HOUR(datetime)` | Hour component | `d.hour` |
| `MINUTE(datetime)` | Minute component | `d.minute` |
| `WEEKDAY(date, 2)` | Day of week (1=Mon with type 2) | `d.weekday() + 1` |
| `WEEKNUM(date, 2)` | Week number of year | `d.isocalendar()[1]` |
| `EOMONTH(date, n)` | Last day of month n months away | `pd.tseries.offsets.MonthEnd(n)` |
| `EDATE(date, n)` | Date n months from date | `date + relativedelta(months=n)` |
| `DATEDIF(start, end, unit)` | Difference in "Y", "M", or "D" | `(end - start).days` |
| `NETWORKDAYS(start, end)` | Working days (excl weekends) | `np.busday_count(start, end)` |
| `WORKDAY(start, n)` | Date n working days from start | `np.busday_offset(start, n)` |
| `DATEVALUE(text)` | Convert text to date serial | `pd.to_datetime(text)` |

---

## Array & Dynamic Array Functions

Available in Excel 365 / Excel 2019+. These return arrays that "spill" into adjacent cells.

| Formula | Description |
|---|---|
| `FILTER(array, include, [if_empty])` | Filter by condition (replaces VLOOKUP for many rows) |
| `SORT(array, sort_index, order)` | Sort an array |
| `SORTBY(array, by_array, order)` | Sort by another array |
| `UNIQUE(array, by_col, exactly_once)` | Return distinct values |
| `SEQUENCE(rows, cols, start, step)` | Generate a sequence of numbers |
| `RANDARRAY(rows, cols, min, max, int)` | Random number array |
| `XLOOKUP(lookup, array, return, default)` | Modern lookup |
| `XMATCH(lookup, array, match_mode)` | Modern MATCH |
| `LET(name1, val1, ..., formula)` | Define variables within a formula |
| `LAMBDA(params, body)` | Define reusable custom functions |

```
Examples (Excel 365):

=FILTER(A2:C100, B2:B100="Sales")          → all Sales rows
=FILTER(A2:C100, (B2:B100="Sales")*(C2:C100>50000), "None")
                                            → AND condition
=SORT(FILTER(A2:C100, B2:B100="Sales"), 3, -1)  → filter then sort by col 3 desc

=UNIQUE(B2:B100)                            → distinct values
=UNIQUE(A2:B100, FALSE, TRUE)               → rows that appear exactly once

=SEQUENCE(10, 1, 1, 1)                      → 1 through 10

=LET(
    sales,   FILTER(A:C, B:B="Sales"),
    avg_rev, AVERAGE(INDEX(sales,,3)),
    avg_rev
)

Custom LAMBDA (define in Name Manager):
=LAMBDA(range, pct, PERCENTILE.INC(range, pct))
→ name it "PCTILE", then call: =PCTILE(C2:C100, 0.9)
```

---

## Database Functions (D-functions)

D-functions operate on a table (list) with a criteria range matching the column headers.

| Formula | Description |
|---|---|
| `DSUM(database, field, criteria)` | Sum matching records |
| `DAVERAGE(database, field, criteria)` | Average matching records |
| `DCOUNT(database, field, criteria)` | Count numeric cells matching criteria |
| `DCOUNTA(database, field, criteria)` | Count non-empty cells matching criteria |
| `DMAX(database, field, criteria)` | Max matching records |
| `DMIN(database, field, criteria)` | Min matching records |
| `DGET(database, field, criteria)` | Extract single matching record |

> D-functions have largely been replaced by `SUMIFS`, `FILTER`, and `XLOOKUP` in modern Excel.

---

## Information Functions

| Formula | Description | Python Equivalent |
|---|---|---|
| `ISBLANK(cell)` | TRUE if cell is empty | `pd.isna(val)` |
| `ISNUMBER(cell)` | TRUE if cell is a number | `isinstance(val, (int, float))` |
| `ISTEXT(cell)` | TRUE if cell is text | `isinstance(val, str)` |
| `ISERROR(cell)` | TRUE if cell has any error | try/except |
| `ISNA(cell)` | TRUE if cell is #N/A | `val is np.nan` |
| `ISODD(n)` / `ISEVEN(n)` | TRUE if odd/even | `n % 2 != 0` |
| `TYPE(cell)` | Returns 1=num, 2=text, 4=bool, 16=error | `type(val)` |
| `CELL("type", ref)` | Returns cell format metadata | `df.dtypes` |
| `N(value)` | Convert value to number (TRUE=1, FALSE=0) | `int(bool_val)` |

---

## Financial Functions

| Formula | Syntax | Description |
|---|---|---|
| `NPV` | `=NPV(rate, value1, value2, ...)` | Net Present Value of cash flows |
| `IRR` | `=IRR(values, guess)` | Internal Rate of Return |
| `PMT` | `=PMT(rate, nper, pv)` | Periodic payment for a loan |
| `PV` | `=PV(rate, nper, pmt)` | Present value |
| `FV` | `=FV(rate, nper, pmt, pv)` | Future value |
| `NPER` | `=NPER(rate, pmt, pv)` | Number of periods |
| `RATE` | `=RATE(nper, pmt, pv)` | Interest rate per period |
| `XNPV` | `=XNPV(rate, values, dates)` | NPV with irregular cash flow dates |
| `XIRR` | `=XIRR(values, dates)` | IRR with irregular dates |
| `SLN` | `=SLN(cost, salvage, life)` | Straight-line depreciation |
| `DB` | `=DB(cost, salvage, life, period)` | Fixed-declining depreciation |

---

## Common Patterns & Combos

### Two-way lookup (INDEX + MATCH)
```
=INDEX(C2:F10, MATCH(H2, A2:A10, 0), MATCH(H3, C1:F1, 0))
```

### Extract domain from email address
```
=MID(A2, FIND("@", A2)+1, LEN(A2)-FIND("@", A2))
```

### First word from full name
```
=LEFT(A2, FIND(" ", A2)-1)
```

### Last word (last name)
```
=RIGHT(A2, LEN(A2)-FIND("*", SUBSTITUTE(A2," ","*", LEN(A2)-LEN(SUBSTITUTE(A2," ","")))))
```

### Percentage of total (like % column in pivot table)
```
=C2/SUM($C$2:$C$100)    (format as %)
```

### Running total
```
=SUM($C$2:C2)            (copy down)
```

### Rank within group (no PivotTable needed)
```
=COUNTIFS($B$2:$B$100, B2, $C$2:$C$100, ">"&C2)+1
```

### Conditional formatting helper — top 10%
```
=C2>=PERCENTILE($C$2:$C$100, 0.9)
```

### Count unique values
```
=SUMPRODUCT(1/COUNTIF(A2:A100, A2:A100))
```

### Month-over-month change
```
=IF(ROW()-ROW($C$2)=0, "", (C2-C1)/C1)
```

---

## Power Query M Language Basics

Power Query is the data transformation layer inside Excel and Power BI.

```m
// Load a CSV
let
    Source = Csv.Document(File.Contents("C:\data\sales.csv"), [Delimiter=",", Encoding=65001]),
    Promoted = Table.PromoteHeaders(Source),
    ChangedTypes = Table.TransformColumnTypes(Promoted, {
        {"date", type date},
        {"revenue", type number}
    })
in
    ChangedTypes

// Filter rows
Table.SelectRows(Source, each [Region] = "West" and [Revenue] > 1000)

// Add a custom column
Table.AddColumn(Source, "Revenue Tier",
    each if [Revenue] > 10000 then "High"
    else if [Revenue] > 5000  then "Medium"
    else "Low"
)

// Group by (like pivot table)
Table.Group(Source, {"Department"}, {
    {"Total Revenue", each List.Sum([Revenue]),    type number},
    {"Avg Salary",    each List.Average([Salary]), type number},
    {"Count",         each Table.RowCount(_),      type number}
})

// Merge queries (VLOOKUP equivalent)
Table.NestedJoin(
    Orders, {"CustomerID"},
    Customers, {"ID"},
    "CustomerDetails", JoinKind.LeftOuter
)
```
