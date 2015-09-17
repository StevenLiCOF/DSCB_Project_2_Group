# Why is version control useful?
* **Backup** — coffee + keyboard = #%$*!
	* *Undo* — Oops, was that important?
* **Collaborate** — programming is a team sport
	* *Track steps* — What happened while you were sleeping
	* *Branching and merging* — Work in parallel and bring it back together

# A little on how Git works
## The Git index
Git keeps a local copy of everything you add to it, even if you delete it later.
The nice part about this – you don’t need an internet connection to use it, and you can revert to older versions super quickly.
*Imperfect analogy: if Git is a camera, the repo is what’s in frame*
##### Good Git Hygiene Tip:
For this reason, avoid adding *big* or *sensitive* files to the repo. They’re not easy to remove.

## Commits are snapshots of changes
When you change things in files, or add or remove files, you commit these changes and Git records the current state of everything
*Imperfect analogy: if Git is a camera, commits are pictures*
##### Good Git Hygiene Tip:
Try to make commits fairly atomic— if you changed a bunch of things, make separate commits with descriptive messages for each.

## Version history is (kind of) like a family tree
Every commit (except the first one) has a parent (AKA the state of the repo when you started making changes).

If you and someone else start working in parallel from the same starting point, git will try to merge your changes back together later\*

If you want to keep your work separate for a while (say, if you’re working on a new feature or something), you can make a *named branch* which will stay separate from the *master branch* until you say otherwise.

##### Good Git Hygiene Tip:
*merging will be much easier if you communicate and aren’t working in the same parts of the same files

## Remotes are copies of a repo on another computer **(or on a service like Github)**.

### GitHub is a central place to host a repo
GitHub is a place to store your repo, so others can clone it, push to it, and pull from it.

It also includes some very nice tools for software projects, like Markdown README rendering, issue tracker and wiki tools, and the ability to “fork” a project to make your own independent copy of it for development.

# Git basics
## Let’s Git Started 😆
### Get an existing repo
`git clone <url goes here>`
### Create a new repo
`git init <project name goes here>`

## When you’re ready to push code

### 1. See what’s changed since the last commit
`git status` shows files that have changed or are untracked
`git diff [optional: filename]` shows the changes themselves

### 2. “Stage” the things you want to include in your commit
This includes both files that have changed and new files you want to add.

`git add <file or directory>`

### 3. Commit your changes and add a useful message

`git commit -m ‘message goes here’`

### 4. (optional) Pull from the origin repo

`git pull`

If any other changes were made since you last pulled, this will attempt to merge them with yours. If you don’t do this and you need to, the remote repo will tell you.

### 5. Push to the origin repo

`git push`

## Additional useful commands
### `git log`
See the history of commits present in your copy of the repo.
### `git checkout <revision #, or branch name> <optional filename>`
If you give a revision number, this changes your files to how they were when that commit was the latest. Think of this like a time machine for going to old commits, without changing/losing anything in the present repo.

**WARNING:** if you specify a file, using `git checkout` without committing your latest changes will wipe them out.

If you give a branch name, `git checkout` will switch you to the most recent commit in that named branch and make that branch the active one (so new commits will be added to that branch)
### `git rm`
Remove a file from the repo
### `git mv`
Rename/move a file in the repo
### `git stash`
Save your changes to a “stash”, but don’t commit them. Useful if you might want to come back to things later, but want to wipe your changes clean right now.

## Flow for collaborating on bigger projects using GitHub (including this class!)
### 1. Do your work on a separate branch or GitHub fork
If you have push privileges on the project, you can make a new branch using `git branch <branch name>` and work on that.
If not, you can make your own separate copy of the repo using the **Fork** button on GitHub.
In either case, use the same workflow as above for committing and pushing.

### 2. Submit a pull request
When you’re ready to contribute back to the main branch, push all your changes up to GitHub and use the Pull Request tab to submit your changes.

### 3. The manager of that project will review your proposed changes
If there are additional changes that need to be made, you can push more commits to that branch and they’ll automatically be added to the pull request.

# Additional reference
* [GitHub - How to make a pull request](https://help.github.com/articles/using-pull-requests/)

## Atlassian Git tutorials
* [How to undo things you’ve already committed](https://www.atlassian.com/git/tutorials/undoing-changes)
* [Some different workflows for collaborating using Git](https://www.atlassian.com/git/tutorials/comparing-workflows)

## Git Cheatsheet
[PDF](https://training.github.com/kit/downloads/github-git-cheat-sheet.pdf)
