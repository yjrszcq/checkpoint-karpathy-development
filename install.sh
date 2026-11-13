#!/usr/bin/env bash
# Install the canonical skill, references, scripts, and assets. Bash 3.2+.
set -euo pipefail

SKILL_NAME=checkpoint-karpathy-development
REPOSITORY=yjrszcq/checkpoint-karpathy-development
HARNESS_LIST=(claude codex pi ohmypi antigravity cursor deepseek gemini opencode custom)
HARNESS_NAMES=('Claude Code' 'Codex' 'Pi' 'Oh My Pi' 'Antigravity' 'Cursor' 'DeepSeek Harness' 'Gemini CLI' 'OpenCode' 'Custom')
selected=()
scope=
project_dir=
skills_dir=
source_dir=
ref=main
dry_run=false
run_dir=
active_target=
active_backup=
activation_started=false

die() { printf 'Error: %s\n' "$*" >&2; exit 1; }

usage() {
  cat <<'EOF'
Checkpoint Karpathy skill installer

Usage: bash install.sh [OPTIONS]
  --harness NAME[,NAME...]  Select one or more harnesses (repeatable).
  --scope user|project     Default: user; interactive selection if no harness given.
  --project PATH           Project root; implies --scope project.
  --skills-dir PATH        Override the skills parent directory (one harness only).
  --source PATH            Install from a local checkout without downloading.
  --ref REF                GitHub branch, tag, or commit to download (default: main).
  --dry-run                Print destinations without writing or downloading.
  --list                   List harness names.
  -h, --help               Show this help.

Harnesses: Claude Code, Codex, Pi, Oh My Pi, Antigravity, Cursor,
  DeepSeek Harness, Gemini CLI, OpenCode, Custom.
For --harness identifiers, see:
  https://github.com/yjrszcq/checkpoint-karpathy-development/blob/main/docs/guide.md#harness-identifiers
Use --harness custom --skills-dir PATH for other compatible harnesses.
With no --harness, read an interactive menu from /dev/tty (also works with curl | bash).
Select custom to enter the skills parent directory; the skill folder is added inside it.

Examples:
  bash install.sh --harness codex --scope user
  bash install.sh --harness claude,cursor --project /path/to/project
  bash install.sh --harness pi --source . --dry-run
  bash install.sh --harness custom --skills-dir /path/to/skills
EOF
}

add_harness() {
  local name existing
  name=$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')
  case "$name" in
    claude|claudecode|claude-code) name=claude ;;
    codex|pi|cursor|opencode|custom) ;;
    omp|ohmypi|oh-my-pi) name=ohmypi ;;
    antigravity|antigrivaty) name=antigravity ;;
    deepseek|deepseekharness|deepseek-harness|dsh) name=deepseek ;;
    gemini|geminicli|gemini-cli) name=gemini ;;
    *) die "Unknown harness: $1. See the harness identifiers table in docs/guide.md." ;;
  esac
  for existing in ${selected[@]+"${selected[@]}"}; do
    [[ "$existing" != "$name" ]] || return 0
  done
  selected+=("$name")
}

need_value() { [[ $# -ge 2 && -n "$2" && "$2" != --* ]] || die "$1 requires a value."; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --harness)
      need_value "$@"
      harness_input=$2
      [[ "$harness_input" != ,* && "$harness_input" != *, && "$harness_input" != *,,* ]] || die 'Empty harness name.'
      IFS=, read -r -a names <<< "$harness_input"
      for name in "${names[@]}"; do add_harness "$name"; done
      shift 2 ;;
    --scope) need_value "$@"; scope=$2; shift 2 ;;
    --project) need_value "$@"; project_dir=$2; shift 2 ;;
    --skills-dir) need_value "$@"; skills_dir=$2; shift 2 ;;
    --source) need_value "$@"; source_dir=$2; shift 2 ;;
    --ref) need_value "$@"; ref=$2; shift 2 ;;
    --dry-run) dry_run=true; shift ;;
    --list)
      printf '%s\n' "${HARNESS_NAMES[@]}"
      exit 0 ;;
    -h|--help) usage; exit 0 ;;
    *) die "Unknown option: $1. Run with --help." ;;
  esac
done

if [[ -n "$project_dir" ]]; then
  [[ -z "$scope" || "$scope" == project ]] || die '--project conflicts with --scope user.'
  scope=project
fi
if [[ ${#selected[@]} -eq 0 ]]; then
  if ! { exec 3<>/dev/tty; } 2>/dev/null; then
    die 'No terminal available. Specify --harness NAME and optionally --scope user|project.'
  fi
  printf 'Select harnesses by number (separated by spaces or commas):\n' >&3
  for ((i=0; i<${#HARNESS_LIST[@]}; i++)); do
    if [[ "${HARNESS_LIST[$i]}" == custom ]]; then
      printf '  %s) Custom (enter installation path)\n' "$((i+1))" >&3
    else
      printf '  %s) %s\n' "$((i+1))" "${HARNESS_NAMES[$i]}" >&3
    fi
  done
  printf '> ' >&3
  IFS= read -r answer <&3 || die 'No harness selected.'
  answer=${answer//,/ }
  read -r -a choices <<< "$answer"
  for choice in ${choices[@]+"${choices[@]}"}; do
    case "$choice" in
      [1-9]|10) add_harness "${HARNESS_LIST[$((choice-1))]}" ;;
      *) add_harness "$choice" ;;
    esac
  done
  [[ ${#selected[@]} -gt 0 ]] || die 'No harness selected.'
  for name in "${selected[@]}"; do
    if [[ "$name" == custom ]]; then
      [[ ${#selected[@]} -eq 1 ]] || die 'Select custom on its own.'
      if [[ -z "$skills_dir" ]]; then
        printf 'Skills directory (parent of %s/): ' "$SKILL_NAME" >&3
        IFS= read -r skills_dir <&3 || die 'No installation path entered.'
        [[ -n "${skills_dir//[[:space:]]/}" ]] || die 'No installation path entered.'
      fi
    fi
  done
  if [[ -z "$scope" && "${selected[0]}" != custom ]]; then
    printf 'Install scope: 1) user  2) project [1]: ' >&3
    IFS= read -r answer <&3 || die 'No scope selected.'
    case "$answer" in ''|1|user) scope=user ;; 2|project) scope=project ;; *) die 'Invalid scope.' ;; esac
  fi
  exec 3>&-
fi
scope=${scope:-user}
[[ "$scope" == user || "$scope" == project ]] || die 'Scope must be user or project.'
[[ -z "$skills_dir" || ${#selected[@]} -eq 1 ]] || die '--skills-dir requires exactly one harness.'
for name in "${selected[@]}"; do
  if [[ "$name" == custom ]]; then
    [[ ${#selected[@]} -eq 1 ]] || die 'Select custom on its own.'
    [[ -n "$skills_dir" ]] || die 'Custom harness requires --skills-dir PATH.'
  fi
done
if [[ "$scope" == project ]]; then
  project_dir=${project_dir:-$PWD}
  [[ -d "$project_dir" ]] || die "Project directory does not exist: $project_dir"
  project_dir=$(cd "$project_dir" && pwd -P)
fi
case "$skills_dir" in
  '~') skills_dir=$HOME ;;
  '~/'*) skills_dir=$HOME/${skills_dir#\~/} ;;
esac
if [[ -n "$skills_dir" && "$skills_dir" != /* ]]; then skills_dir=$PWD/$skills_dir; fi

skills_root() {
  if [[ -n "$skills_dir" ]]; then printf '%s\n' "$skills_dir"; return; fi
  if [[ "$scope" == project ]]; then
    case "$1" in
      claude) printf '%s/.claude/skills\n' "$project_dir" ;;
      codex|antigravity) printf '%s/.agents/skills\n' "$project_dir" ;;
      pi) printf '%s/.pi/skills\n' "$project_dir" ;;
      ohmypi) printf '%s/.omp/skills\n' "$project_dir" ;;
      cursor) printf '%s/.cursor/skills\n' "$project_dir" ;;
      deepseek) printf '%s/.dsh/skills\n' "$project_dir" ;;
      gemini) printf '%s/.gemini/skills\n' "$project_dir" ;;
      opencode) printf '%s/.opencode/skills\n' "$project_dir" ;;
      custom) die 'Custom harness requires --skills-dir PATH.' ;;
    esac
  else
    case "$1" in
      claude) printf '%s/skills\n' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" ;;
      codex) printf '%s/.agents/skills\n' "$HOME" ;;
      pi) printf '%s/skills\n' "${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}" ;;
      ohmypi) printf '%s/.omp/agent/skills\n' "$HOME" ;;
      antigravity) printf '%s/.gemini/config/skills\n' "$HOME" ;;
      cursor) printf '%s/.cursor/skills\n' "$HOME" ;;
      deepseek) printf '%s/skills\n' "${DSH_HOME:-$HOME/.dsh}" ;;
      gemini) printf '%s/.gemini/skills\n' "$HOME" ;;
      opencode) printf '%s/opencode/skills\n' "${XDG_CONFIG_HOME:-$HOME/.config}" ;;
      custom) die 'Custom harness requires --skills-dir PATH.' ;;
    esac
  fi
}

# Resolve every selection before creating files; shared destinations install once.
destinations=()
harnesses=()
for name in "${selected[@]}"; do
  root=$(skills_root "$name")
  [[ "$root" == /* ]] || die "Skills directory must resolve to an absolute path: $root"
  target=${root%/}/$SKILL_NAME
  duplicate=false
  for existing in ${destinations[@]+"${destinations[@]}"}; do
    [[ "$existing" != "$target" ]] || duplicate=true
  done
  printf '%s (%s): %s\n' "$name" "$scope" "$target"
  if ! "$duplicate"; then destinations+=("$target"); harnesses+=("$name"); fi
done
if "$dry_run"; then exit 0; fi

on_exit() {
  local code=$?
  trap - EXIT
  # Restore the old bundle if activation was interrupted, preserving partial output.
  if "$activation_started" && [[ -e "$active_target" || -L "$active_target" ]]; then
    if ! mv "$active_target" "$run_dir/interrupted-install"; then
      printf 'Could not relocate partial installation: %s\nPrevious backup: %s\n' "$active_target" "$active_backup" >&2
      exit "$code"
    fi
  fi
  if [[ -n "$active_backup" && ( -e "$active_backup" || -L "$active_backup" ) ]]; then
    if mv "$active_backup" "$active_target"; then
      printf 'Restored previous installation: %s\n' "$active_target" >&2
    else
      printf 'Previous installation retained at: %s\n' "$active_backup" >&2
    fi
  fi
  if [[ $code -ne 0 && -n "$run_dir" ]]; then printf 'Installer files retained at: %s\n' "$run_dir" >&2; fi
  exit "$code"
}
trap on_exit EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

validate_package() {
  local package=$1 file
  [[ -s "$package/SKILL.md" ]] || die "Missing SKILL.md in $package"
  [[ -s "$package/LICENSE" ]] || die "Missing LICENSE in $package"
  grep -Eq '^name: checkpoint-karpathy-development[[:space:]]*$' "$package/SKILL.md" || die "Unexpected skill name in $package/SKILL.md"
  for file in project-state.md goal-input.md roadmap-templates.md checkpoint-details.md; do
    [[ -s "$package/references/$file" ]] || die "Missing reference: $package/references/$file"
  done
  for file in init_project.py create_goal.py archive_goal.py project_state.py goal_documents.py requirements.txt; do
    [[ -s "$package/scripts/$file" ]] || die "Missing script resource: $package/scripts/$file"
  done
  for file in README.md status.md context.md milestones.md milestone.md phase.md changelog.md progress.md; do
    [[ -s "$package/assets/roadmap/$file" ]] || die "Missing goal template: $package/assets/roadmap/$file"
  done
  for file in en.md zh.md; do
    [[ -s "$package/assets/memory/$file" ]] || die "Missing memory template: $package/assets/memory/$file"
  done
  for file in en.yaml zh.yaml; do
    [[ -s "$package/assets/config/$file" ]] || die "Missing configuration template: $package/assets/config/$file"
  done
}

if [[ -n "$source_dir" ]]; then
  [[ -d "$source_dir" ]] || die "Source directory does not exist: $source_dir"
  source_dir=$(cd "$source_dir" && pwd -P)
else
  command -v curl >/dev/null || die 'curl is required for remote installation.'
  command -v tar >/dev/null || die 'tar is required for remote installation.'
  [[ -n "$ref" && "$ref" != *[!a-zA-Z0-9._/-]* ]] || die 'Invalid Git reference.'
  cache_root=${XDG_CACHE_HOME:-$HOME/.cache}/checkpoint-karpathy-installer
  mkdir -p "$cache_root"
  download_dir=$(mktemp -d "$cache_root/source.XXXXXX")
  printf 'Downloading %s (%s)...\n' "$REPOSITORY" "$ref"
  curl -fSL --retry 2 --connect-timeout 15 --max-time 180 \
    "https://codeload.github.com/$REPOSITORY/tar.gz/$ref" -o "$download_dir/source.tar.gz"
  tar -tzf "$download_dir/source.tar.gz" > "$download_dir/archive-list.txt"
  IFS= read -r archive_root < "$download_dir/archive-list.txt"
  archive_root=${archive_root%%/*}
  [[ -n "$archive_root" && "$archive_root" != . && "$archive_root" != .. && "$archive_root" != *[!a-zA-Z0-9._-]* ]] || die 'Unexpected archive root.'
  tar -xzf "$download_dir/source.tar.gz" -C "$download_dir" "$archive_root/SKILL.md" "$archive_root/LICENSE" "$archive_root/references" "$archive_root/scripts" "$archive_root/assets"
  source_dir=$download_dir/$archive_root
  validate_package "$source_dir"
  rm -f "$download_dir/source.tar.gz"
  printf 'Reusable source cache: %s\n' "$source_dir"
fi
validate_package "$source_dir"

for ((i=0; i<${#destinations[@]}; i++)); do
  target=${destinations[$i]}
  name=${harnesses[$i]}
  if [[ -f "$target/SKILL.md" && -d "$target/references" ]] && \
      cmp -s "$source_dir/SKILL.md" "$target/SKILL.md" && \
      cmp -s "$source_dir/LICENSE" "$target/LICENSE" && \
      diff -qr "$source_dir/references" "$target/references" >/dev/null 2>&1 && \
      diff -qr "$source_dir/scripts" "$target/scripts" >/dev/null 2>&1 && \
      diff -qr "$source_dir/assets" "$target/assets" >/dev/null 2>&1; then
    printf 'Already up to date: %s\n' "$target"
    continue
  fi
  if [[ -z "$run_dir" ]]; then
    state_root=${XDG_STATE_HOME:-$HOME/.local/state}/checkpoint-karpathy-installer
    mkdir -p "$state_root/backups"
    run_dir=$(mktemp -d "$state_root/backups/$(date +%Y%m%d-%H%M%S).XXXXXX")
  fi
  stage=$run_dir/staged-$name
  mkdir "$stage"
  cp "$source_dir/SKILL.md" "$stage/SKILL.md"
  cp "$source_dir/LICENSE" "$stage/LICENSE"
  for resource in references scripts assets; do
    cp -R "$source_dir/$resource" "$stage/$resource"
  done
  validate_package "$stage"
  for resource in references scripts assets; do
    diff -qr "$source_dir/$resource" "$stage/$resource" >/dev/null
  done
  cmp "$source_dir/SKILL.md" "$stage/SKILL.md"
  cmp "$source_dir/LICENSE" "$stage/LICENSE"
  mkdir -p "${target%/*}"
  active_target=$target
  active_backup=
  if [[ -e "$target" || -L "$target" ]]; then
    active_backup=$run_dir/previous-$name
    mv "$target" "$active_backup"
    printf 'Previous installation backup: %s\n' "$active_backup"
  fi
  activation_started=true
  if ! mv "$stage" "$target"; then die "Could not activate installation at $target"; fi
  activation_started=false active_backup= active_target=
  printf 'Installed: %s\n' "$target"
done
if [[ -n "$run_dir" ]]; then rmdir "$run_dir" 2>/dev/null || true; fi
printf 'Done. Restart your harness or reload its skills, then invoke %s.\n' "$SKILL_NAME"
