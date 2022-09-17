
# commit those edits

When you're about to create a new source file,
always check to verify you're doing it within some repo.
If it's for a brand new thing, consider creating a new repo.

Why? So it eventually gets saved to the cloud.
Some folks use SVN, perforce, and others for versioning, but on
modern projects the right answer will almost always be "git". So it's
enough to verify that `git status` shows your new file, perhaps as
untracked.  You don't _have_ to `git add` it, but usually it wouldn't
hurt, you can always `git rm` it later.

Some scripts truly are throw away one-offs.  That's fine. Put it in
a repo anyway, where it will appear as a line of status output until
you add or rm it. That line of output is a friendly reminder.

## benefits

Oh, let me count the ways! Here are just a few.

1. You're going to want to `git diff` current against recently working.
2. You're going to want to check out a previous version.
3. Commits are easy to `git push`, and then you're safe from `rm -rf .`, laptop stolen from car, and other mishaps.
4. Others can see your edit, e.g. via a slack'd github URL.
4. You can `git blame` to reveal state-of-mind and timestamp of last edit .
5. You can leverage pre-commit, lint, and CI/CD pipelines to tidy up your code.
6. If you keep it, then the PR pull request process can help improve quality.

## PR process

That last item is multi-faceted, and if code doesn't start out in a repo
it might not even occur to you to take advantage of the PR process.

- Run tests and linters before merging down to main. Ideally CI/CD will run these and make results visible in the PR.
- Read your own code, be the first reviewer. Seeing code in a new context lets you approach it afresh.
- Are there some rough edges? Is it simpler to just fix them, rather than ask forgiveness?
- Invite colleagues to review, and heed their remarks.
- Merge to main, deleting the feature branch. The cycle begins again. Rinse, lather, repeat.

## source in non-source files

I have seen people do remarkable things with source, including

- keep source only on laptop
- store the only networked copy in a section of a Confluence text document,
- or as part of a .PDF presentation of notebook results.

People do such things in good faith.
Maybe their professor or colleagues never requested source in a particular manner.
It's just a matter of folks approaching a situatio from different academic
cultures where there are different norms.

## source not planned for merging

I have also seen people create branches named after Partner-A, Partner-B ...,
with the intent that they exist forever and are never merged down.
Some branches are immortal, like `main` and `develop`.
Others should typically last for a sprint or two and then
go through PR, merge, delete.
Use `mkdir` to carve out a bit of namespace
if there's partner specific details that need to be buried somewhere.
That allows the files to still be available after checking out various branches.

Don't burden your colleagues with a branch that
slowly bit rots and will never be merged.
Before long it will show lint issues, failed tests,
dangling references to renamed methods and so on.
Best to halt the pain by deleting it.
