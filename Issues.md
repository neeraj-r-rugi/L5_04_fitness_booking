# Issues Found in `gym_system.py` 

 Line numbers refer to the original file that was given.

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | OS command injection via `os.system` | Security, **High** (B: B605, CWE-78) | 36 | A shell command is built from the user-controlled prefix. This can run arbitrary commands or delete all JSON files when the prefix is empty. | Use `glob` and `os.remove()` instead of a shell. Reject empty prefixes and handle `OSError`. |
| 2 | Off-by-one in capacity check (overbooking) | Logic bug, **High** (M) | 10 | `>` allows one extra booking after the class reaches capacity. | Use `>=` so a full class rejects new bookings. |
| 3 | Unknown classes accept bookings | Logic bug, **High** (M) | 9–10 | Unknown classes get capacity `0`, but the old check still allows a booking and creates a roster. | Check that the class exists before creating its roster; otherwise return `False`. |
| 4 | Mutable default argument | Bug, **Medium** (P: W0102) | 8 | A default list is shared by every call, so attendance entries accumulate unexpectedly. | Use `None` as the default and select `booking_log` inside the function. |
| 5 | Negative / invalid capacity accepted | Logic bug, **Medium** (M) | 27–28 | Negative, string, and float capacities were accepted, making classes invalid or unbookable. | Require a non-negative `int` that is not `bool`; raise `ValueError` for invalid values. |
| 6 | Unvalidated user input crashes program | Robustness bug, **Medium** (M) | 52–53 | Invalid input raises `ValueError`; negative input is silently ignored. | Validate input in `ask_guest_count()`, retry invalid values, and keep Enter as the default. |
| 7 | Resource leak: file never closed, no encoding | Bug, **Medium** (P: R1732, W1514) | 32–34 | The export file is not closed reliably, and its encoding depends on the operating system. | Use a `with open(..., encoding="utf-8")` block. |
| 8 | Bare `except` swallows all errors | Bug / style, **Medium** (P: W0702, F: E722) | 21 | A bare `except` hides programming errors and even catches interrupts. | Catch only `KeyError` and `ValueError`, then return whether cancellation succeeded. |
| 9 | Duplicate bookings allowed | Logic bug, **Medium** (M) | 8–15 | The same member can be booked into one class more than once. | Check the roster and reject an existing member. |
| 10 | Inconsistent member ID types | Data bug, **Medium** (M) | 49, JSON output | Integer and string IDs are mixed, so equivalent IDs can be treated as different members. | Convert IDs to strings when booking and cancelling. |
| 11 | Guest ID collisions and silent failures in `addMembers` | Logic bug, **Medium** (M) | 27–29 | Guest IDs restart on every call, and failed bookings are ignored. | Choose unused guest IDs, stop after the first failed booking, and return the number added. |
| 12 | `main()` runs on import | Design bug, **Low** (M) | 62 | Importing the module starts the program and asks for input. | Run `main()` only under an `if __name__ == "__main__":` guard. |
| 13 | Cancelling a booking in an unknown class relied on the bare except | Logic, **Low** (M) | 20–23 | Unknown classes raise `KeyError`, which was hidden by the bare handler. | Handle `KeyError` explicitly with the other expected cancellation error. |
| 14 | Function name not snake_case | Style, **Low** (P: C0103) | 27 | `addMembers` does not follow PEP 8 naming. | Rename it to `add_members` and update its call sites. |
| 15 | Non-idiomatic dict iteration | Style, **Low** (P: C0206) | 38–40 | The code loops over keys and performs a second lookup. | Iterate directly with `rosters.items()`. |
| 16 | Old-style string formatting | Style, **Low** (P: C0209) | 15 | The booking log uses `%` formatting. | Replace it with an f-string. |
| 17 | Missing docstrings | Style, **Low** (P: C0114, C0116 ×9) | 1, 8, 18, 24, 27, 31, 35, 38, 42 | The module and functions are undocumented. | Add docstrings describing purpose, return values, and errors. |
| 18 | Wrong blank-line spacing | Style, **Low** (F: E302 ×9, E305) | 8, 18, 24, 27, 31, 35, 38, 42, 58 | Top-level definitions do not have the required spacing. | Add two blank lines around top-level definitions. |

