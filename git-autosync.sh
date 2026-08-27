#!/bin/bash
# Add, commit, pull --rebase and push this repo. launchd runs it every 15 minutes
# and captures the output.
set -eu
export GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=15'
export GIT_TERMINAL_PROMPT=0
cd -- "$(dirname -- "$0")"

for marker in rebase-merge rebase-apply MERGE_HEAD; do
	if [ -e "$(git rev-parse --git-path "$marker")" ]; then
		echo "$(date '+%F %T') skip, repo is mid-$marker and needs a human"
		exit 0
	fi
done

git add -A
git diff --cached --quiet || git commit -qm "auto-sync: $(date '+%F %T') on $(hostname -s)"
git pull -q --rebase --autostash || { git rebase --abort || true; exit 1; }
git push -q
