#!/usr/bin/env bash
# WendtVer for this repository: https://wendtver.org
#
#   Start at 0.0.0. Every commit increments PATCH.
#   PATCH rolls over to 0 at 10 and increments MINOR.
#   MINOR rolls over to 0 at 10 and increments MAJOR.
#
# The version is therefore the commit count written one digit at a time. It is
# derived, not decided, which is the whole point: a hand-maintained version
# drifts, and the number in plugin.json is not decoration — Claude Code uses it
# as the update key and skips the update when it matches what a user already
# has. A stale version means installed users silently stop receiving anything.
#
# SemVer is not used because a skill has no contract to break. There is no API
# whose removal is a MAJOR event and no addition that is a MINOR one.
#
# Squash is the only merge method here, so a branch's own commit count is
# irrelevant: four commits on a branch still add exactly one to main. The
# version a branch must carry is the base branch's count plus one.
#
# Usage:
#   scripts/version.sh            print the version this branch should carry
#   scripts/version.sh --current  print the version HEAD should carry
#   scripts/version.sh --check    verify plugin.json against the commit count
#   scripts/version.sh --write    set plugin.json to this branch's version
#
# BASE overrides the base branch, which defaults to main.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

manifest=".claude-plugin/plugin.json"

encode() { printf '%d.%d.%d' "$(( $1 / 100 ))" "$(( ($1 / 10) % 10 ))" "$(( $1 % 10 ))"; }

count=$(git rev-list --count HEAD)
base_branch="${BASE:-main}"

# The count this branch produces on the base branch once squashed: the base's
# own count plus the one commit the squash creates. Falls back to the local
# branch when there is no remote-tracking ref, and to HEAD when there is no
# base either, which is the case on main itself.
target_count() {
  local ref
  for ref in "origin/$base_branch" "$base_branch"; do
    if git rev-parse --verify --quiet "$ref" >/dev/null; then
      git rev-list --count "$ref"
      return
    fi
  done
  echo "$count"
}

read_version() { python3 -c "import json;print(json.load(open('$manifest')).get('version',''))"; }

case "${1:-}" in
  --current) encode "$count"; echo ;;
  --check)
    # On the base branch the commit count is the truth. On any other branch
    # HEAD's count is not what will land, so the check is against what the
    # squash will produce.
    if [ "$(git rev-parse --abbrev-ref HEAD)" = "$base_branch" ]; then
      n="$count"; how="$count commits"
    else
      n=$(( $(target_count) + 1 )); how="$base_branch + 1 squashed commit"
    fi
    want=$(encode "$n")
    have=$(read_version)
    if [ "$want" = "$have" ]; then
      printf 'ok   version %s matches %s\n' "$have" "$how"
    else
      printf 'FAIL %s says version %s; %s means %s\n' "$manifest" "${have:-<unset>}" "$how" "$want" >&2
      printf '     fix: scripts/version.sh --write\n' >&2
      exit 1
    fi ;;
  --write)
    want=$(encode "$(( $(target_count) + 1 ))")
    python3 - "$manifest" "$want" <<'PY'
import collections, json, sys
path, want = sys.argv[1], sys.argv[2]
with open(path) as fh:
    data = json.load(fh, object_pairs_hook=collections.OrderedDict)
data["version"] = want
with open(path, "w") as fh:
    json.dump(data, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
PY
    printf 'wrote version %s (%s + 1 squashed commit)\n' "$want" "$base_branch" ;;
  *) encode "$(( $(target_count) + 1 ))"; echo ;;
esac
