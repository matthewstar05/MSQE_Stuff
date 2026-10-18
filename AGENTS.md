# Agent instructions for MSQE_Stuff

These instructions apply to every coding agent working in this repo (Claude Code, Codex, Cursor, Gemini/Antigravity, and others).

## Auto-commit and push (standing authorization)

The owner has given standing permission to commit and push. **Do not ask for confirmation.** At the end of every prompt where you created, modified, moved, or deleted files in this repo:

**Only commit and push changes you made yourself.** Other agents often work in this repo at the same time. Their edits and commits are theirs to push.

1. **Stage only your own changes.** List the paths you created, modified, or deleted for this prompt and stage exactly those: `git add -- <paths>` (deletions too: `git add -A -- <paths>`). **Never** run a bare `git add -A`, `git add .`, or `git commit -a`, and never stage a file you didn't edit. The only exception is when the user names specific files to include.
2. **Commit once per prompt** with a short imperative subject that names the course, e.g. `ECON 5021: add Lecture 13 page to Unit 2 TLDR`. Use whatever co-author or attribution trailer your harness requires.
3. **Sync:** `git pull --rebase --autostash origin main`.
4. **Check that you'd only push your own work:** run `git log --format='%h %s' origin/main..HEAD`. It must list **only** the commit(s) you just made. If it shows anyone else's unpushed commit, **do not push**, because `git push` would publish their work too. Leave your commit local and tell the user.
5. **Push:** `git push origin main`.
6. **Report the result in one line,** e.g. `Committed abc1234 and pushed.` If nothing changed, skip the commit and say nothing about git.

### Guardrails

- Never force-push, rewrite published history, amend someone else's commit, or use `--no-verify`.
- If the autostash can't be re-applied cleanly, stop and tell the user. The stash holds other agents' uncommitted edits, so never drop it or resolve it yourself.
- If the rebase or push fails (conflict, auth, or rejected), stop. Leave the commit local and tell the user what failed. Don't try to resolve another agent's conflicting edits yourself.
- Never commit secrets (API keys, tokens, `.env`, credentials), LaTeX build byproducts (`*.aux`, `*.log`, `*.out`, `*.toc`, `*.synctex.gz`), scratch or temp files, or any file over 50 MB. Ask the user before committing files like these.
- Leave files you didn't touch alone, even when they show up as modified or untracked. They may belong to another agent's work in progress.
- **ECON 5560 team repo:** `SS1-ECON5560-AppliedEconProj1/ECON5560-Team3/` is a subtree of the separate, public `team3` repository. Committing it inside MSQE_Stuff is fine. **Never** run `git team3-push` (`git subtree push ... team3 main`) or push to the `team3` remote unless the user asks for it in that prompt. Never put Canvas pages or course materials into the Team3 repo.

## Repo conventions

- Each course has its own top-level folder, named like `SS1-ECON5021-AdvEconometrics1` (term, course number, short name).
- Within a course, materials go in `Course_Info/`, `Lecture_Notes/`, `Exercises/`, `Scripts/`, and exam-prep folders such as `Exam1/` and `Exam2/`.
- LaTeX: there is no TeX Live installation. Compile with `tectonic` and render pages with `pdftoppm` (poppler).
- Canvas downloads should be organized into the matching course folder rather than left in `~/Downloads`.
