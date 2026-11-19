import argparse
import os
from core.hasher import find_duplicates
from core.sorter import organize_directory
from core.logger import save_log, rollback

def main():
    parser = argparse.ArgumentParser(description="Smart File Organizer & Duplicate Finder")
    parser.add_argument("path", help="Target directory path")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    parser.add_argument("--dedupe", action="store_true", help="Scan and quarantine duplicate files")
    parser.add_argument("--undo", action="store_true", help="Revert the last organization run")
    args = parser.parse_args()

    target = os.path.abspath(args.path)
    if not os.path.isdir(target):
        print(f"Error: '{target}' is not a valid directory.")
        return

    if args.undo:
        count = rollback(target)
        print(f"Rollback complete: restored {count} files.")
        return

    if args.dedupe:
        dupes = find_duplicates(target)
        print(f"Found {len(dupes)} duplicate groups:")
        for file_hash, paths in dupes.items():
            print(f"  [{file_hash[:10]}...] Keep: {paths[0]}")
            for dup in paths[1:]:
                print(f"     Duplicate: {dup}")

    ops = organize_directory(target, dry_run=args.dry_run)
    mode = "DRY RUN" if args.dry_run else "EXECUTED"
    print(f"[{mode}] Processed {len(ops)} files.")
    if not args.dry_run and ops:
        save_log(target, ops)

if __name__ == "__main__":
    main()
