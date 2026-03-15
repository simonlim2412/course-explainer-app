---
description: Automates creating a Pull Request for uncommitted changes
---

This workflow automates the process of saving your current uncommitted changes, bringing in the latest code from the base branch, and submitting a Pull Request.

**Steps for the workflow:**

1. **Check for Uncommitted Changes**
   - Run `git status` to check if there are any pending code changes.
   - If everything is already committed (working tree is clean), simply let the user know and stop the workflow here.
   - If there are uncommitted changes, proceed to the next steps.

2. **Update the Base Branch**
   - Temporarily save the uncommitted changes: `git stash`
   - Switch to the base branch: `git checkout Antigravity-Course`
   - Pull the latest updates: `git pull origin Antigravity-Course`

3. **Create a Feature Branch**
   - Create and switch to a new feature branch using a descriptive, concise name: `git checkout -b <new-feature-branch>`
   - Restore the saved changes: `git stash pop`

4. **Stage and Commit**
   - Stage all changes: `git add .`
   - Look at the changes and come up with a message that accurately describes what the user worked on.
   - Commit the code: `git commit -m "<descriptive message>"`

5. **Push and Create Pull Request**
   - Push the code to the remote repository: `git push -u origin <new-feature-branch>`
   - Create a Pull Request back into the `Antigravity-Course` branch using the GitHub CLI (`gh`):
     `gh pr create --base Antigravity-Course --head <new-feature-branch> --title "<PR Title>" --body "<PR Description>"`

6. **Provide the PR Link**
   - Once the Pull Request is created, output the final PR link for the user so they can verify it. Keep the output language simple and human-readable!
