
# clear code

Better to write source code that is clear, than obscure.
But what does that _mean_?

[![crystal clear](https://live.staticflickr.com/7361/9717711673_c57775c325.jpg)](
https://www.flickr.com/photos/flashflood/9717711673/sizes/m/)

The best operational definition I have encountered is this.
Suppose some code is going through the
[PR](https://en.wikipedia.org/wiki/Distributed_version_control#Pull_requests)
process. It used to be a bit ratty, light on tests, and so on,
but now we are tightening it up to prepare for merging to `main`.
_How do we know it is ready?_
There's a simple question to ask yourself:

> Would the undergrad intern we hire next summer
> be able to maintain this code
> _without_ speaking with the author?

That is, would the

- executable code
- docstrings
- comments
- external documents
- automated unit tests

be able to answer the intern's questions
that arise when adding a feature or fixing a bug?
Even if the author and author's team
have moved to a new department or left the company?

If "no", if the artifacts do not suffice, then keep coding.
Anticipate those questions, and answer them,
paving the way to a successful merge.
You can
[split out a new module](https://en.wikipedia.org/wiki/Single-responsibility_principle),
[DRY it up](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself),
[Extract Method](https://en.wikipedia.org/wiki/Code_refactoring#Techniques),
simplify your API,
rename identifiers,
do whatever is needed.
