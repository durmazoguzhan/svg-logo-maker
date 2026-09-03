# Monogram and lettermark

One to three letters as a mark. The bridge between a wordmark and a symbol,
and the standard answer to "we need something square".

**Choose it when** the full name is too long for small containers, the
initials are already how people refer to the company, or a wordmark needs a
square companion for favicons and app icons.

**Do not choose it when** the initials are already taken by something larger in
the same space. Three letters is a very crowded namespace.

## Construction

**One letter is stronger than three.** Each additional letter costs legibility
at small sizes and buys almost nothing. Two letters only when both are needed
to disambiguate.

**Build the letter on the mark's grid, not the type's.** A monogram is a shape
that happens to be readable as a letter. Take the skeleton from a typeface,
then rebuild it with your own stroke weights and terminals so it belongs to the
same system as the rest of the identity.

**The counter is the design.** The enclosed space in a, e, o, g, p, R, B is
where a monogram becomes distinctive. Enlarge it, cut it open, or square it
off. Leave it alone and you have a letter in a box.

**Containers are a decision, not a default.** A circle or rounded square around
the letter guarantees a clean app icon and costs you distinctiveness, because
every app icon is a rounded square. Skip the container if the letterform itself
holds a square area.

## Ambiguity is the whole risk

Rotated, mirrored or heavily stylised letters stop being letters. Test it: show
it to somebody who does not know the company and ask what letter it is. If they
hesitate, it is a shape, and a shape has to earn its meaning the hard way.

Watch the pairs that collapse: **O/0/Q, I/l/1, S/5, Z/2, G/6, B/8, C/G, M/W**
when rotated, **b/d/p/q** when mirrored.

## Small sizes

This is the style most likely to end up at 16px, so design it there and scale
up rather than the reverse. Solid letter knocked out of a solid field survives
better than an outlined letter, every time.

    python3 scripts/check.py --favicon-size 16 monogram.svg
    scripts/legibility.sh monogram.svg 16 32

## Failure modes

*Two letters interlocked until neither reads.* The classic. Interlocking is a
craft move with a narrow window and outside it the result is a knot.

*A serif face shrunk into a small square.* Serifs are the first thing to go at
32px, so a serif monogram needs its serifs redrawn heavier than the source.

*Initials nobody uses.* If people say the full name, a monogram is a mark you
will have to teach them.
