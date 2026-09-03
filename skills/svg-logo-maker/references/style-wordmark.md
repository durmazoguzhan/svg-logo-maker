# Wordmark and logotype

The name, set and adjusted. The most under-used answer, because it is the least
fun to make and the most likely to be right.

**Choose it when** the company is young, the name is short and pronounceable,
or the brand will always appear with its name anyway. Most B2B companies should
start here.

**Do not choose it when** the name is long, hard to read, or needs to work in a
square container without the name being legible.

## Setting it

Start from a real typeface rather than drawing letters. Drawing letterforms
from scratch is a specialist skill and the result of doing it casually is
always visible.

Then adjust, because a wordmark is not just type set at a size:

**Tighten the tracking.** Display sizes need less letter spacing than body
text. A logotype set at default tracking looks like a placeholder.

**Kern the pairs, not the string.** The gaps that break are the ones with a
diagonal or an open counter: **AV, AW, LT, To, Ta, Ya, P.** Even out the
*apparent* space, which is area, not distance.

**Decide about case deliberately.** All caps reads as institutional, lowercase
as approachable, mixed as neutral. Small caps is a real option and is almost
never considered.

**Change one thing, at most two.** A single altered letter is a logotype; four
altered letters is a typeface you did not design.

## The font is a legal object

Before anything ships: what is the licence, does it permit use in a logo, does
it permit outlining, is a desktop licence enough or does the brand need a
foundry agreement. This gets skipped constantly and it is the part that
produces letters from a lawyer.

Safe starting points are the open families with permissive licences — Inter,
Source Sans, IBM Plex, Libre Franklin, Public Sans, EB Garamond. Check the
specific licence anyway; "open source" is not one licence.

## Delivery, and this is where wordmarks die

The live-text SVG is the master and it never leaves the repository. Everything
delivered is outlined:

    scripts/outline.sh wordmark.svg wordmark-outlined.svg

Read the font audit it prints. If it says SUBSTITUTED, you are about to freeze
a font you did not choose. On a machine without your typeface installed, the
outlines are whatever fontconfig picked, the metrics may even match, and the
letterforms will be wrong in a way that only shows up on press.

## Failure modes

*Arial or Helvetica straight out of the box.* Not because they are bad, but
because unadjusted default type is the visual signature of no decision.

*Tracking left at defaults.* The single most common tell.

*A wordmark used as a favicon.* Seven letters in a 16px cell is a grey bar.
Extract or design a separate lettermark — see `style-monogram.md`.
