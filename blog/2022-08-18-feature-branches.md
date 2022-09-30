
# feature branches

Here is how I work with feature branches.
These are my expectations for code authored by myself or by colleagues.

## have a working system

Always have a working system.
Typically on the `main` branch.
Don't break the build.
Have a way to automatically determine that things are mostly working.
Run such automated tests in a Github CI/CD pipeline,
as well as on your laptop.

## start with config files

When creating a new repo,
fill in some standard dot files.

Github will get you started with .gitconfig, LICENSE, and ReadMe.md.

Trailing whitespace details are too silly to even spend time thinking about.
Create .pre-commit-config.yaml so that you and your colleagues won't
accidentally introduce such problems.
Remember to `$ pre-commit install`.

Often a top level Makefile will be as helpful as a ReadMe.
When someone new starts interacting with the project,
it immediately shows them the sort of commands the author
expects will be be used with the code.

Most repos I work with contain some python code.
Which motivates adding .flake8 and .isort.cfg.

Create environment.yml to organize deps.
Omit the "defaults" channel, as "conda-forge" suffices.
Keep packages up-to-date.
Specify version constraints with `>=`, e.g. `- python >= 3.10.4`.
Occasionally update to 3.10.5 or whatever as you notice
that new revs are released.
Remember those automated tests?
This is one reason we need them -- run tests after `conda env update`
to verify it didn't break anything.
Pin to downrev, e.g. `- python == 3.10.4`, if something regressed.

## edits go in a feature branch

Initially you're in `main`, and that's fine for the first few commits.
But at some point you'll want to add a feature, and a branch is the
right place for that to happen.

Put the feature name in the branch name,
plus a Jira ticket number if there is one,
plus maybe your initials if the project has many active contributors.

WIP commits can be messy, they are just there to help the author
view diffs between what was recently working and what we have now.
As long as pre-commit hooks don't complain, it's all good.
Every so often you might want to lint as you go, anticipating the merge.

If a feature branch persists more than a week or three, that suggests
the feature is "too big" and might have been scoped smaller.

## PR process

The Jira ticket should make clear what needs to be implemented
to consider the feature "done", either done forever
or to close out an iteration.
Now that we have a working implementation,
it is time to revisit any rough edges in the code.
People sometimes say "we'll clean it up later",
but that never happens. _Now_ is the time to clean the code,
so the project won't take on an accumulating amount of technical debt.

Push, visit the github website, and create a Pull Request.
Feel free to do this a few days early, before it's all working
properly, if you find it helpful.

Verify that CI/CD tests ran, and that they are Green.
If not, then push some edits, lather, rinse, repeat.

### author actions

You are the first reviewer.

View the PR edits on the website, in the same way that
other reviewers will. This offers a different perspective
from what your IDE has been showing you, so you may
notice some new details or refactors that need attention.
Fix them as you encounter them.
Run final tests.

Now invite one or more colleagues to review.
They approach the code with fresh eyes,
so they will see different things that you didn't.

### reviewer actions

Cardinal rule: Be kind. Try to find nice things to say about
the code, as well as constructive suggestions for changes.

If author ignored the project's "make it lint clean" rule,
call that out. A branch with lint errors can't merge down,
and shouldn't even be proposed for merging.

If there's a clear bug, call it out.
Suggest a unit test that demonstrates how we're not NULL-safe or whatever.
Cite the spec, or suggest revising the spec.

If there's a six-versus-half-dozen issue,
where we could implement one way or another and both ways "work",
consider remaining silent.
If each way has pros and cons, consider commenting on them
to mentor or educate colleagues.
The code won't change in this PR, but the discussion
might influence coding decisions folks make in future.

If coverage report shows some target code is not
covered by automated unit test, and that would be valuable,
call it out. Suggest a test.

If you see copy-n-paste within the PR, or between `main` and PR,
call it out, we should DRY it up. Now is the time.
Prefer parameterizing over pasting.

If you read some code which is correct but unclear, call it out.
Maybe we need a docstring or an identifier rename,
or the comments are out of sync with the code.
It doesn't matter if you _eventually_ understood the code -- we
want source code to be immediately clear and self explanatory.
There is an iron clad rule here: "Could the intern we hire
next summer maintain this, if the author is unavailable?"
If that undergrad would find it difficult to properly add
a feature or fix a bug, then we should improve the code
prior to merging.

Finally, give the PR a thumbs-up, perhaps without waiting
to see recommend changes adopted.

If author and reviewer don't see eye-to-eye on some detail,
then author always gets the benefit of the doubt
and should merge as-is.

The PR process should not be an obstacle to getting code out the door.
It should go quickly. If reviewers raise no concerns within 24 hours
(one business day), then the PR is automatically approved and
may be merged.

Author does the merge -- not a reviewer.
Author may incorporate small fixes as part of the merge.
After merging, author should delete the feature branch.

Be sure to `--squash` merge,
as the github website UI helpfully suggests.
Often we'll configure that as a project default,
as well as auto-delete of the old branch.

## deadlines

PM picks the scope of an Epic or Feature.

Individual contributor estimates effort and decides whether to pull
a given ticket into a sprint, perhaps after breaking out sub-tickets.

## release notes

For many projects, `git log` offers adequate history,
reported at the less granular level of PRs rather than raw WIP commits.
If customers have additional documentation needs,
then use [SemVer](https://semver.org/),
[conventional commits](https://simonberner.dev/cctcs),
and/or maintain a release document within the repo.

Automate such release details as much as possible,
so that it is "hard" to mess up a release,
even if for someone new to the project.

## integration

Depending on project size there may be long-lived branches
besides `main`, e.g. `develop`.
In which case the PR process is all about merging edits into `develop`.
Author runs the usual tests and then immediately merges to `main`
for production deployment.

Similarly, some projects may adopt a bit more ceremony,
such as the gitflow process, without any effect on PRs.

Tag each release, to facilitate rollbacks.

We try to make a separate release for each feature,
rather than bundling several together.
Why? Fault isolation is much easier when only one thing changed.
