No Reflection Questions Were Provided.

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.60 / 10 (16 messages) | **10.00 / 10** |
| Bandit | 1 High | **No issues identified** |
| Flake8 | 10 warnings | **Clean** |

### Behaviour before vs after (default run)

| | Before | After |
|---|---|---|
| Yoga | `M1, M2, M3, M4` (overbooked) | `M1, M2, M3` (M4 rejected: "Class full") |
| Pilates | `M5` (class doesn't exist) | Rejected: "Unknown class" |
| Spin | empty (capacity -2, all guests rejected) | `GUEST-0, GUEST-1, GUEST-2` (-2 rejected, capacity stays 4) |
| HIIT | `55, GUEST-0` (int mixed with str) | `55, GUEST-0` (all strings, still capped at 2) |