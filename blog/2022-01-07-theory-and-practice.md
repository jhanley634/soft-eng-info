
# theory & practice

Teaching a receptive student is a joy.

It is very rewarding to see a colleague abandon sloppy old habits
in favor of new ones recently learned,
and to see the practice continue to be followed even in your absence.

Learning theory, such as coupling, cohesion,
[DbC](https://en.wikipedia.org/wiki/Design_by_contract),
is essential.
But successfully applying theory is also important.
At least two points in the software lifecycle
offer excellent teaching moments for this:

1. project planning / architecture / design
2. pull requests

The first can seem a bit nebulous or theoretical,
at least for interns not yet accustomed to the cycle.

![2021 interns](asset/2022-01-07/sfo-interns.jpg)

The second comes up repeatedly, at each of these stages:

- initial implementation
- refactoring / maintenance
- feature addition
- bug fix

Never squander an opportunity to connect theory to practice in a PR.
It is at this point that you have a motivated student in a position
to critique a _particular_ software artifact in service of making it
the best merge possible.
Authors _will_ be receptive to constructive criticism.

Common themes for PR remarks include:

- [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) (extract Helper)
- replace obscure constant with a nicely named symbol
- more generally, rename so identifier speaks the truth and is more helpful
- "comments lie!", see above, delete or improve comment that once was right but by now has [bit rotted](https://en.wikipedia.org/wiki/Software_rot)
- use appropriate data structure so we see linear rather than quadratic performance
- handle corner cases
- add unit test that exercises corner case
- make logging or assertion more helpful by revealing inputs when we fail
