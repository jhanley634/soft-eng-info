
# feature branches

Here is how I work with feature branches,
my expectations for code authored by myself or by colleagues.

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

Often a top level Makefile will be _as_ helpful as a ReadMe.
When someone new starts interacting with the project,
it immediately shows them the sort of commands the author
expects will be used with the code.

Most repos I work with contain some python code.
Which motivates adding .flake8 and .isort.cfg.

Create environment.yml to organize deps.
Omit the "defaults" channel, as "conda-forge" suffices.
Keep packages up-to-date.
Specify version constraints with `>=`, e.g.

    - python >= 3.10.4

Occasionally update to 3.10.5 or whatever as you notice
that new revs are released.
Remember those automated tests?
This is one reason we need them -- run tests after `conda env update`
to verify it didn't break anything.
Pin to downrev, e.g. `python == 3.10.4`, if something regressed.

## type annotations

Annotations are nice, but strictly optional.

Consider using them if it makes a signature more self-documenting,
or if it improves the usefullness of IDE auto-completion.

## docstrings

Docstrings are nice, but strictly optional.

If you write one, begin with an English sentence.
That means initial cap, verb, noun, final period.
Optionally follow it with a blank line and additional text.

If you feel you should describe the arguments,
maybe you're making the right call,
or maybe you should give an arg a more descriptive name.

Sometimes "comments lie!", so avoid this.
Better to be vague than incorrect.
Generalizations and motivations go in the comments,
while specifics belong in the code.

If it's hard to document in a
[single sentence](https://en.wikipedia.org/wiki/Single-responsibility_principle),
maybe the code is telling you it wants to be
split into multiple methods.

Avoid writing "obvious" docstrings that reveal nothing
beyond what the function signature already told us.
The more you write, the more there is to keep in sync with changing code.
Assume your audience can read both the docstring _and_ the code.

Docstrings appear after the function signature.
Don't insert string constants in the middle of a function body --
instead use `#` comments where appropriate.

## edits go in a feature branch

Initially you're in `main`, and that's fine for the first few commits.
But at some point you'll want to add a feature, and a branch is the
right place for that to happen.

Put the feature name in the branch name,
plus a Jira ticket number if applicable,
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
or simply to complete an iteration.
Now that we have a working implementation,
it is time to revisit any rough edges in the code.
People sometimes say "we'll clean it up later",
but that never happens. _Now_ is the time to clean the code,
so the project won't keep accumulating technical debt.

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
so they will see things that you didn't.

### reviewer actions

Follow [this advice](/blog/2022-08-18-code-review).

## deadlines

PM picks the scope of an Epic or Feature.

Individual contributor estimates effort and decides whether to pull
a given ticket into a sprint, perhaps after breaking out sub-tickets.

## release notes

For many projects, `$ git log` offers adequate history,
reported at the level of PRs rather than more granular raw WIP commits.
If customers have additional documentation needs,
then use [SemVer](https://semver.org/),
[conventional commits](https://simonberner.dev/cctcs),
and/or maintain a release document within the repo.

Automate such release details as much as possible,
so that it is "hard" to mess up a release,
even for someone new to the project.

## integration

Depending on project size there may be long-lived branches
besides `main`, e.g. `develop`.
In which case the PR process is all about merging edits into `develop`.
An engineer will run the usual tests and then immediately merge to `main`
for production deployment.

Similarly, some projects may adopt a bit more ceremony,
such as the gitflow process, without any effect on PRs.

Tag each release, to facilitate rollbacks.

Use [feature flags](https://en.wikipedia.org/wiki/Feature_toggle)
where possible, to facilitate rollbacks.

We try to make a separate release for each feature,
rather than bundling several together.
Why? Fault isolation is much easier when only one thing changed.
