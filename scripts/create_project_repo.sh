#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: create_project_repo.sh <repo-name> [public|private]

Create or reuse a GitHub repository for the current directory, initialize local
git if needed, ensure the default branch is main, configure origin, and push the
initial commit.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage >&2
  exit 1
fi

repo_name="$1"
visibility="${2:-public}"

case "$visibility" in
  public|private) ;;
  *)
    echo "Visibility must be 'public' or 'private'." >&2
    exit 1
    ;;
esac

for cmd in git gh; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
done

if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI is not authenticated. Run 'gh auth login' first." >&2
  exit 1
fi

owner="${GITHUB_OWNER:-$(gh api user -q .login)}"
remote_url="https://github.com/${owner}/${repo_name}.git"
repo_dir="$(pwd)"

if [[ ! -d "${repo_dir}/.git" ]]; then
  git init "$repo_dir" >/dev/null
fi

# Set a repo-local identity if one is not already configured.
if ! git -C "$repo_dir" config user.name >/dev/null 2>&1; then
  git -C "$repo_dir" config user.name "${GIT_AUTHOR_NAME:-$owner}"
fi

if ! git -C "$repo_dir" config user.email >/dev/null 2>&1; then
  git -C "$repo_dir" config user.email "${GIT_AUTHOR_EMAIL:-${owner}@users.noreply.github.com}"
fi

# Keep the initial bootstrap reproducible even in an empty directory.
if [[ -z "$(find "$repo_dir" -mindepth 1 -maxdepth 1 ! -name .git -print -quit)" ]]; then
  printf '# %s\n\nBootstrapped project repository.\n' "$repo_name" > README.md
fi

if ! gh repo view "${owner}/${repo_name}" >/dev/null 2>&1; then
  gh repo create "${owner}/${repo_name}" "--${visibility}" >/dev/null
fi

if git -C "$repo_dir" rev-parse --verify HEAD >/dev/null 2>&1; then
  git -C "$repo_dir" branch -M main
else
  git -C "$repo_dir" symbolic-ref HEAD refs/heads/main
fi

if git -C "$repo_dir" remote get-url origin >/dev/null 2>&1; then
  existing_remote="$(git -C "$repo_dir" remote get-url origin)"
  if [[ "$existing_remote" != "$remote_url" ]]; then
    git -C "$repo_dir" remote set-url origin "$remote_url"
  fi
else
  git -C "$repo_dir" remote add origin "$remote_url"
fi

git -C "$repo_dir" add -A

if ! git -C "$repo_dir" rev-parse --verify HEAD >/dev/null 2>&1; then
  git -C "$repo_dir" commit -m "scaffold: initialize ${repo_name}" >/dev/null
elif ! git -C "$repo_dir" diff --cached --quiet; then
  git -C "$repo_dir" commit -m "docs: sync project bootstrap state" >/dev/null
fi

gh auth setup-git >/dev/null 2>&1 || true
git -C "$repo_dir" push -u origin main

printf 'Repository ready: %s\n' "$remote_url"
