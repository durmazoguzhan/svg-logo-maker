# Emblem and badge

Text locked inside a shape: seals, crests, roundels, shields. The type and the
container are one object and cannot be separated.

**Choose it when** the brand wants heritage, craft, officialdom or membership —
breweries, coffee, outdoor gear, universities, clubs, guarantees.

**Do not choose it when** the logo has to live in a 24px UI header or a
favicon. An emblem is a display mark. It needs a simplified companion, and
planning for that companion from the start is the difference between an emblem
that works and one that gets replaced in a year.

## Construction

**Concentric bands.** Emblems are read from the outside in: outer rule, a ring
of type, an inner rule, then the central device. Keep the bands to three or
fewer. Five bands is a coin, not a logo.

**Curved type has rules.** Set the top arc reading left to right along the
outside of the curve, and the bottom arc reading left to right along the
*inside* so it is not upside down. Letter spacing has to open up on a curve or
the letters collide at the baseline. Small text on a tight curve is unreadable
at any size, so keep the arc radius large relative to the type.

**One central device, and it should be simple.** The container is already
carrying complexity. The device inside it should be something you could draw
from memory.

**Weight has to survive reduction.** Emblems die at small sizes because their
rules are hairlines. Set the outer rule at 8 to 12 units in a 512 viewBox, not
2.

## The simplified companion is mandatory

Design three versions at once and treat them as one deliverable:

  full emblem, for packaging, signage and anywhere over about 40mm
  reduced emblem, outer ring of type dropped, for medium sizes
  device only, square, for favicons and app icons

Say where the cutover is, in millimetres for print and pixels for screen. If
you do not, somebody will scale the full emblem into a 32px avatar and the
identity will look bad through no fault of the drawing.

## Failure modes

*Text so small it is texture.* If nobody can read "EST. 2019", it is not
information, it is a grey band. Either set it large enough or leave it out.

*Vintage as a substitute for an idea.* A banner, a laurel and a sunburst are
signifiers of craft, not evidence of it.

*One-colour collapse.* Emblems with tonal fills between bands become a solid
disc in one ink. Run `scripts/legibility.sh` early; this style fails that test
more than any other.
