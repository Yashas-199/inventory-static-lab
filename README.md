# inventory-static-lab
To enhance Python code quality, security, and style by utilizing static analysis tools (Pylint, Bandit, and Flake8) to detect and rectify common programming issues.

    -Simple in-memory inventory manager using a global stock_data dictionary.
    -Provided functions: addItem(item, qty, logs=[]), removeItem(item, qty), getQty(item),      loadData(file), saveData(file), printData(), checkLowItems(threshold).
    -Demonstrated basic usage in main() (adds/removes items, saves/loads JSON).

    - Removed unsafe eval() and replaced with explicit logging.
    - Replaced mutable default args and added input validation.
    - Replaced bare except with specific exceptions and logging.
    - Improved file I/O using context managers and validated JSON content.

    - Static analysis tools (Pylint/Bandit/Flake8) help find both security and correctness issues.
    - Small language details (mutable defaults, bare except) cause subtle bugs that are easy to miss.
    - Explicit input validation prevents many runtime errors and makes code more maintainable.

Commands — setup & run
    pip install --upgrade pip
    pip install pylint bandit flake8
    python3 inventory_system.py

    -Run static-analysis tools (before/after comparisons):
        pylint inventory_system.py > pylint_before.txt
        bandit -r inventory_system.py > bandit_before.txt
        flake8 inventory_system.py > flake8_before.txt

        pylint clean_inventory_system.py > pylint_after.txt
        bandit -r clean_inventory_system.py > bandit_after.txt
        flake8 clean_inventory_system.py > flake8_after.txt


| Priority | Issue Type | Tool Flagged | Location (Original Code) | Issue Description | Fix Applied | Status |
|---------|-------------|--------------|-------------------------|------------------|-------------|--------|
| **High** | Unsafe `eval()` usage | Bandit | Line ~50 (`eval("print('eval used')")`) | Allows arbitrary code execution → major security vulnerability | Removed `eval()` and replaced with safe `logging.info()` | Fixed |
| **High** | Bare `except:` | Pylint + Bandit | `removeItem()` & `loadData()` | Silences real errors, hides failures, and makes debugging impossible | Replaced with specific exception handling (`FileNotFoundError`, `JSONDecodeError`, `KeyError`, etc.) | Fixed |
| **High** | Mutable default argument (`logs=[]`) | Pylint | `addItem()` function parameter | Default list is shared across calls causing unexpected state changes | Used `logs=None` and initialized inside function | Fixed |
| **High** | Missing input validation (wrong types or negative qty) | Manual + Pylint hints | `addItem("banana", -2)` & `addItem(123, "ten")` | Allows invalid data → logical errors & crashes | Added type & value checks → raises `TypeError` / `ValueError` | Fixed |
| **Medium** | File I/O without context manager | Pylint | `loadData()` & `saveData()` | Not closing files properly → resource leaks | Updated to `with open(...)` blocks | Fixed |
| **Medium** | Potential `KeyError` accessing stock | Manual | `getQty(item)` | Crashes when item absent → no default handling | Used `.get(item, 0)` to avoid crashes | Fixed |
| **Medium** | Removing more items than available or negative removal | Manual | `removeItem(item, qty)` | Inventory becomes inconsistent | Added validation & quantity checks; raise errors appropriately | Fixed |



# Reflection — Lab 5 Static Code Analysis:
    Which issues were the easiest to fix, and which were the hardest? Why?
    -Mutable default args and small style issues were easy: changing `logs=[]` to `None` is straightforward.

    Did the static analysis tools report any false positives?
    -Pylint suggested some refactors that are stylistic rather than bugs; for example, naming suggestions that do not affect correctness.

    How would you integrate static analysis tools into your actual software development
    workflow?
    -Add Pylint/Bandit/Flake8 to CI (GitHub Actions). Run locally pre-commit hooks. Fail builds for high severity Bandit findings.

    What tangible improvements did you observe in the code quality, readability, or potential
    robustness after applying the fixes?
    -Safer I/O, removal of `eval`, explicit type checks reduce runtime exceptions and security risk, and logging improves debuggability.



