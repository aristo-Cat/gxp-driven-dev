#!/bin/sh
# Activate the gxp-driven-dev git locks (L7). Run once per clone.
cd "$(git rev-parse --show-toplevel)" || exit 1
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit .githooks/pre-push 2>/dev/null
echo "Installed: core.hooksPath -> .githooks"
echo "Active: pre-commit (anti-leak + @AGENTS.md single-source check + staged frontmatter), pre-push (hard-block)."
