
# zone offset

tl;dr: Specify tzinfo=utc when creating a python datetime.

        stamp = dt.datetime(yr, mo, dy, hr, mi, sec, tzinfo=tz.utc)

And the obligatory imports:

        from datetime import timezone as tz
        import datetime as dt

![reliable timekeeper](https://live.staticflickr.com/157/333622277_b19c1ba642_b.jpg){ width=1024px height=683px }

## time is continuous

Time is continuous, but ASCII representations aren't.
Not in general.
They may skip an hour, or repeat an hour,
through the magic of Daylight Saving.

Python supports so-called naïve datetimes. Avoid them.
Usually they're more trouble than they're worth.
Take care to specify `tzinfo` each and every time you create a new datetime.

Attempting to mix the two, mixing datestamps with / without tzinfo,
will often result in an error, and that's a Good Thing,
a reminder that there's one more place in your code where you should fill them in.

## daylight saving

My system's default zone is America/Los_Angeles,
which is a way of saying that Congress can change next year's clock readings
in ways I cannot predict right now.
Perhaps they will get around to going the Arizona route,
no twice-a-year change, but I'm not holding my breath.
Meantime, better to write correct code.
You don't want to see fresh bug reports against it twice annually.

True story:
I recently examined four years of `+08:00` hourly timestamps,
from a locale that never uses Daylight Saving.
I was briefly convinced there were four one-hour gaps.
Until I noticed I had accidentally interpreted them using local DS rules,
which produced both the gap artifacts and four dup timestamps.

## serializing

Consider serializing all timestamps with
an explicit `+00:00` suffix (UTC),
or perhaps with "local" hours + suffix like `-07:00` (PDT).
There's certainly more than one way to do it correctly,
but explicit tends to be least error prone and most self documenting.

(Image credit: [codyr](https://www.flickr.com/photos/codyr/333622277/sizes/l/))

----

[They call it Arizona](https://www.youtube.com/watch?v=jTaQYa6szcA)

----
