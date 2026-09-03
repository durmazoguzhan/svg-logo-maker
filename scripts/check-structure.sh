#!/usr/bin/env bash
# Asserts the layout that Claude Code's plugin loader and the marketplace expect.
#
# Every check here corresponds to something in the plugin reference: the
# manifest lives in .claude-plugin/ and nothing else does, skills are found at
# skills/<name>/SKILL.md, and the skill's invocation name comes from the
# frontmatter rather than the directory, so the two must agree or an update
# silently renames the skill.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

PLUGIN=svg-logo-maker
fail=0
check() { if eval "$1" >/dev/null 2>&1; then echo "ok   $2"; else echo "FAIL $2"; fail=1; fi; }
json() { python3 -c "import json,sys;print(json.load(open(sys.argv[1]))$2)" "$1"; }

check '[ -f .claude-plugin/plugin.json ]'                  "plugin manifest exists"
check 'python3 -c "import json;json.load(open(\".claude-plugin/plugin.json\"))"'      "plugin manifest is valid JSON"
check 'python3 -c "import json;json.load(open(\".claude-plugin/marketplace.json\"))"' "marketplace manifest is valid JSON"
check "[ \"\$(json .claude-plugin/plugin.json '[\"name\"]')\" = $PLUGIN ]"            "plugin name is $PLUGIN"
check "[ \"\$(json .claude-plugin/marketplace.json '[\"plugins\"][0][\"name\"]')\" = $PLUGIN ]" \
                                                           "marketplace lists $PLUGIN"
check "[ \"\$(json .claude-plugin/marketplace.json '[\"plugins\"][0][\"source\"]')\" = ./ ]" \
                                                           "marketplace source is the repository root"

# A `version` on the marketplace entry pins the plugin and would then have to
# move in lockstep with plugin.json. One update key, in one file.
check '! grep -q "\"version\"" <(python3 -c "import json;print(json.dumps(json.load(open(\".claude-plugin/marketplace.json\"))[\"plugins\"][0]))")' \
                                                           "marketplace entry carries no competing version"

# .claude-plugin holds the manifests and nothing else; components live at root.
check '[ "$(find .claude-plugin -type f -not -name "*.json" | wc -l)" -eq 0 ]' \
                                                           ".claude-plugin holds manifests only"
check "[ -f skills/$PLUGIN/SKILL.md ]"                     "skill is at skills/$PLUGIN/SKILL.md"
check "[ -d skills/$PLUGIN/references ]"                   "reference directory exists"
check "[ -d skills/$PLUGIN/scripts ]"                      "script directory exists"

# The invocation name comes from frontmatter first, directory second. If they
# disagree the skill quietly changes name between installs.
check "grep -qE '^name: $PLUGIN\$' skills/$PLUGIN/SKILL.md" \
                                                           "SKILL.md frontmatter name matches the directory"
check "head -1 skills/$PLUGIN/SKILL.md | grep -qx -- ---"  "SKILL.md opens with frontmatter"
check "grep -qE '^description:' skills/$PLUGIN/SKILL.md"   "SKILL.md declares a description"

check '[ -f LICENSE ]'                                     "LICENSE exists"
check '[ -f README.md ]'                                   "README exists"
check '[ -f CONTRIBUTING.md ]'                             "CONTRIBUTING exists"
check '[ -f SECURITY.md ]'                                 "SECURITY exists"
check '[ -f CODE_OF_CONDUCT.md ]'                          "CODE_OF_CONDUCT exists"
check '[ -f CHANGELOG.md ]'                                "CHANGELOG exists"

# Executables, because a script the loader cannot run is a script that is not there.
for f in skills/$PLUGIN/scripts/*.sh; do
  check "[ -x $f ]" "$(basename "$f") is executable"
done

exit $fail
