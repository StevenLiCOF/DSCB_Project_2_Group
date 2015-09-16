# Help! I'm stuck in merge hell!

## It says you have uncommitted changes:
That's true! You can either 
 - commit your changes
 - `git stash` your changes to wipe them out, and save them to a "stash" that you could reapply later.

## It says I have a merge conflict
This means that some files on the remote you're pulling from changed in some way that isn't easily combined with your changes to those files. This can happen when we push sample code to the repo and your local code isn't exactly the same (which it probably won't be).

### Ways to deal with this:
- You can open the files with conflicts and edit them manually
- If you just want to overwrite your local copy with whatever you're pulling, run `git checkout --theirs <file path goes here>`. There's also an `--ours` option if you want to overwrite the version on remote.
- You can cancel the merge so you can save your own copy of your file. Do this with `git merge --abort`. When you've saved a copy, committed it, and are ready to resume merging, do so with `git merge <remote>/<branch>`. Note that you'll probably still be have to deal with a conflict, but this lets you save a copy first so you can `git checkout --theirs`

Once you're done, whatever strategy you pick, you must commit the merged files using `git add` and `git commit`.

# I did an oopsie and want to return a file to the way it was on a certain commit

To do this you need to figure out the "hash" for the commit you want to revert the file to, which is a pile of unique letters and numbers that identify a commit. A hash looks like this: 55269341c7452fc06855d66aa78d149fc992279e. You don't have to copy the whole thing though; Git can figure most things out from the first few 5 or 6 numbers.

You can find a hash by going to the file on Github and clicking the "History" button, or using the command `git log <file path goes here>`.

Once you have the hash of a commit you want to revert a file to, revert it using `git checkout <commit hash> <file path>`.

## I did a big oopsie and want to revert the entire repo to the way it was at a certain commit
If you want to revert the entire repo instead of a single file, use `git revert <commit hash>`.

