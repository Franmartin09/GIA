#!/usr/bin/env python3
import subprocess
import sys
import os
import google.generativeai as genai

# --------------------------
# Model Config
# --------------------------
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("❌ Error: No API KEY found.")
    sys.exit(1)

genai.configure(api_key=API_KEY)


def has_changes():
    """Check if there are changes in the repo (staged or unstaged)."""
    status = run_git_command(["git", "status", "--porcelain"])
    return bool(status)

def get_diff(staged=True):
    """Get diff of staged or unstaged changes."""
    cmd = ["git", "diff", "--staged"] if staged else ["git", "diff"]
    return run_git_command(cmd)


def run_git_command(args):
    """Run a git command and return cleaned output."""
    try:
        result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return result.stdout.strip() if result.stdout else ""
    except Exception as e:
        print(f"❌ Error running git command {' '.join(args)}: {e}")
        return ""


def generate_commit_message(diff):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
You are an expert software engineer assistant specialized in writing clear, detailed, and professional Git commit messages.

Given the following Git diff, generate a commit message with the following format:

- A concise **title** line (max 50 characters) summarizing the overall change.
- A blank line.
- A detailed **description** explaining the main changes, motivation, and any relevant context.
- If applicable, mention important files or modules affected.
- Use imperative mood (e.g., "Add", "Fix", "Refactor").

Here is the Git diff:

{diff}
"""
    response = model.generate_content(prompt)
    return response.text.strip()


def print_usage():
    print("""
\033[1;33mUsage:\033[0m
  \033[1;32mgai -a\033[0m               Stage ALL changes, create an automatic commit and push
  \033[1;32mgai -f <file>\033[0m       Stage ONLY <file>, create an automatic commit and push

\033[1;33mExamples:\033[0m
  \033[1;32mgai -a\033[0m
  \033[1;32mgai -f app.py\033[0m
""")


def main():
    if "-a" in sys.argv:
        if not has_changes():
            print("⚠️ There are no changes in the repository to commit.")
            return

        # Stage all changes
        subprocess.run(["git", "add", "."])

        diff = get_diff(staged=True)
        if not diff:
            print("⚠️ There are no actual changes in the staging area.")
            return

        commit_message = generate_commit_message(diff)
        if not commit_message:
            print("⚠️ Failed to generate a commit message.")
            return

        subprocess.run(["git", "commit", "-m", commit_message])
        subprocess.run(["git", "push", "--force-with-lease"])
        print(f"✅ Commit pushed: {commit_message}")
    elif "-f" in sys.argv and len(sys.argv) > 2:
        file_to_stage = sys.argv[sys.argv.index("-f") + 1]
        if not os.path.isfile(file_to_stage):
            print(f"❌ Error: File '{file_to_stage}' does not exist.")
            return

        # Stage the specified file
        subprocess.run(["git", "add", file_to_stage])

        diff = get_diff(staged=True)
        if not diff:
            print("⚠️ There are no actual changes in the staging area.")
            return

        commit_message = generate_commit_message(diff)
        if not commit_message:
            print("⚠️ Failed to generate a commit message.")
            return

        subprocess.run(["git", "commit", "-m", commit_message])
        subprocess.run(["git", "push", "--force-with-lease"])
        print(f"✅ Commit pushed for {file_to_stage}: {commit_message}")
    else:
        print_usage()


if __name__ == "__main__":
    main()
