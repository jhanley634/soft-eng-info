
# code review

This illustrates how I review source code.

![](https://live.staticflickr.com/3901/14761251984_4cedfba074_m.jpg)

[//]: # (https://www.flickr.com/photos/internetarchivebookimages/14761251984/sizes/o/)

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

Are attacker-controlled bytes being accepted from internet
and evaluated? [Call it out](https://xkcd.com/327).

If coverage report shows some target code is not
covered by automated unit test, and that would be valuable,
call it out. Suggest a test.

If you see copy-n-paste within the PR, or between `main` and PR, call it out,
we should [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) it up.
Now is the time.
Prefer parameterizing over pasting.

If you read some code which is correct but unclear, call it out.
Maybe we need a docstring, or an identifier rename,
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
as well as auto-deletion of the old branch.
