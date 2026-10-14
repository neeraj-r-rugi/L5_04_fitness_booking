"""Fitness club class booking ledger.

Books members into classes up to a capacity limit, handles cancellations
and exports the rosters to a JSON file.
"""
import glob
import json
import os

DEFAULT_EXPORT = "gym_schedule.json"

# Global State
class_capacity = {"Yoga": 3, "HIIT": 5, "Spin": 4}
rosters = {}
booking_log = []


def book_class(member_id, class_name, attendance_log=None):
    """Book a member into a class.

    Returns True if the booking was made, False if the class is unknown,
    the member is already booked, or the class is full.
    Successful bookings are appended to ``attendance_log`` (or to the
    module-wide ``booking_log`` when none is given).
    """
    member_id = str(member_id)
    if class_name not in class_capacity:
        print("Unknown class:", class_name)
        return False
    roster = rosters.setdefault(class_name, [])
    if member_id in roster:
        print(f"{member_id} is already booked into {class_name}")
        return False
    if len(roster) >= class_capacity[class_name]:
        print("Class full:", class_name)
        return False
    roster.append(member_id)
    log = booking_log if attendance_log is None else attendance_log
    log.append(f"{member_id} -> {class_name}")
    return True


def cancel_booking(member_id, class_name):
    """Remove a member from a class. Returns True if a booking was removed."""
    try:
        rosters[class_name].remove(str(member_id))
        print(f"Cancelled {member_id} from {class_name}")
    except (KeyError, ValueError):
        print("Nothing to cancel")
        return False
    return True


def set_capacity(class_name, seats):
    """Set the seat limit for a class.

    Raises ValueError if ``seats`` is not a non-negative integer. Lowering
    the limit below the current roster size keeps existing bookings but
    blocks new ones.
    """
    if isinstance(seats, bool) or not isinstance(seats, int) or seats < 0:
        raise ValueError(
            f"Capacity must be a non-negative integer, got {seats!r}"
        )
    class_capacity[class_name] = seats


def add_members(class_name, count):
    """Book up to ``count`` walk-in guests into a class.

    Guest IDs are unique within the class (GUEST-0, GUEST-1, ...), even
    across repeated calls. Stops at the first failed booking (e.g. class
    full) and returns the number of guests actually added.
    """
    added = 0
    guest_num = 0
    while added < count:
        guest_id = f"GUEST-{guest_num}"
        guest_num += 1
        if guest_id in rosters.get(class_name, []):
            continue
        if not book_class(guest_id, class_name):
            break
        added += 1
    return added


def export_roster(file=DEFAULT_EXPORT):
    """Write all rosters to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(rosters, handle, indent=2)


def clear_old_exports(prefix="old_"):
    """Delete ``<prefix>*.json`` files in the current directory.

    Uses glob/os.remove instead of a shell command, so the prefix can never
    be interpreted as shell syntax. Returns the number of files removed.
    """
    if not prefix:
        raise ValueError(
            "prefix must not be empty (would match every .json file)"
        )
    removed = 0
    for path in glob.glob(glob.escape(prefix) + "*.json"):
        try:
            os.remove(path)
            removed += 1
        except OSError as err:
            print(f"Could not delete {path}: {err}")
    return removed


def show_rosters():
    """Print every class and its members."""
    for class_name, members in rosters.items():
        print(class_name, ":", ", ".join(members))


def ask_guest_count(default=1):
    """Ask for the number of walk-in guests, re-prompting on bad input."""
    while True:
        raw = input(
            f"How many walk-in guests for HIIT? (Enter for {default}): "
        ).strip()
        if not raw:
            return default
        try:
            count = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if count < 0:
            print("Guest count cannot be negative.")
            continue
        return count


def main():
    """Demo run of the booking ledger."""
    for member in ("M1", "M2", "M3", "M4"):
        book_class(member, "Yoga")
    book_class(55, "HIIT")
    book_class("M5", "Pilates")
    try:
        set_capacity("Spin", -2)
    except ValueError as err:
        print("Could not set capacity:", err)
    add_members("Spin", 3)
    cancel_booking("M9", "Boxing")
    guests = ask_guest_count()
    added = add_members("HIIT", guests)
    print(f"Added {added} of {guests} walk-in guest(s) to HIIT")
    clear_old_exports()
    export_roster()
    show_rosters()


if __name__ == "__main__":
    main()
