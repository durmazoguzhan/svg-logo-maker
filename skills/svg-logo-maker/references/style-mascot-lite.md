# Mascot, built from primitives

A character mark constrained to what can be drawn with circles, rounded
rectangles, arcs and a small number of paths. Not illustration.

**Be honest about the ceiling.** A drawn or painted mascot is a specialist
illustration job and this module does not replace one. What it does is produce
a friendly, geometric character that holds up as an icon — the register of
Twitch, Reddit and GitHub's Octocat rather than a brand character with a
personality and poses.

**Choose it when** the brand is consumer-facing, addresses a non-technical
audience, or wants warmth that a geometric mark cannot supply. Also when the
product genuinely has a creature attached to it already.

**Do not choose it when** the brand is enterprise, financial or regulated. A
character reads as informal whether or not you want it to.

## Construction

**One creature, one expression, front on.** Three-quarter views and multiple
poses belong to illustration systems. A logo is one drawing.

**Build from a silhouette.** Get the outline recognisable with everything
filled black before adding a single feature. If the silhouette does not read as
the animal, no amount of detail will rescue it, and the silhouette is what
survives to 16px.

**Two features carry recognition, at most three.** Ears and eyes for most
mammals; beak and eyes for birds; the shell for a turtle. Whiskers, eyebrows,
nostrils and fur texture are all detail you will delete later, so do not add
them now.

**Eyes decide the character.** Two solid dots read as calm and neutral. Adding
a white catchlight reads as alert and friendly. Enlarging the eye relative to
the head reads younger. This is the single highest-leverage adjustment in the
whole style and it is worth three or four variants on its own.

**Keep symmetry with one break.** A perfectly symmetric face is inert. Tilt the
head slightly, or make one ear different, and it becomes alive.

## Palette

Two to four flat colours. Mascots are the style most tempted into gradients and
shading, and shading is exactly what stops the mark surviving one colour.

Run `scripts/legibility.sh` and expect this style to score lower than a
geometric mark. If it scores under 0.25, the features are separated by colour
alone — put real gaps between them, or knock the features out of the head shape
rather than laying them on top.

## Failure modes

*Cute as the entire idea.* A round animal with big eyes is a template. What
makes a mascot memorable is one specific thing about it, and it is usually a
proportion, not an accessory.

*Detail that vanishes.* Check at 32px early and often; mascots lose their faces
before geometric marks lose their strokes.

*Hard to draw twice.* If nobody in the company can approximate it on a
whiteboard, it will not become part of the culture.
