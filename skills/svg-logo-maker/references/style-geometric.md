# Geometric mark

An abstract or semi-abstract symbol built from primitives. The default answer
for software, infrastructure and anything whose product is not a physical
object.

**Choose it when** the name is long or hard to set, the brand needs a symbol
that works without the name, or the category expects a mark (developer tools,
APIs, protocols).

**Do not choose it when** the company is unknown and will stay unknown for a
while. An abstract mark carries no meaning until people learn it, and a small
brand usually cannot pay for that education. A wordmark is the honest default
for a young company.

## Construction

Work in a 512 viewBox and put the mark inside a 384 circle centred at
(256, 256). That leaves 64 units of margin on every side, which becomes your
clear space later instead of being invented at handoff time.

Pick one unit — 8 or 16 works — and place every coordinate on it. Radii come
from a set of three or four values, not from wherever the cursor landed.

Strokes: use 2 or 3 weights across the whole mark, never 5. In a 512 viewBox,
24 to 40 units is a confident primary stroke and 16 is a secondary. Under 12
you are drawing something that will not survive a favicon.

## The four moves that carry most marks

**Overlap and knock out.** Two shapes overlap; the intersection is removed
rather than tinted. Reads in one colour, which most tinting does not.

**Rotate a repeated element.** One shape, copied at 60° or 90°, is a symbol.
The same shape copied at 37° is a mistake.

**Cut a counter.** Remove a circle or a rounded rectangle from a solid shape.
Keep the cut rounded unless the whole mark is sharp; a sharp notch in an
otherwise soft form reads as damage.

**Interrupt a regular series.** Five bars where the third is shorter, or a ring
with one gap. The interruption is the idea, so it has to be large enough to be
obviously deliberate.

## Failure modes

*The node graph.* Circles joined by lines. It is the visual cliché of the
2020s software industry and it says nothing.

*The gradient rescue.* A weak silhouette given a purple-to-pink gradient. Turn
the gradient off; if the mark dies, the gradient was the design.
`scripts/legibility.sh` will tell you before a reviewer does.

*Detail that only exists at 512.* If you added something you cannot see at
64px, you added it for yourself.

## SVG shape

Primitives beat paths wherever a primitive will do: `<circle>`, `<rect rx>`,
`<polygon>`. They stay readable and editable, and a reviewer can change a
radius without touching a bezier. Reach for `<path>` when the form genuinely
needs a curve you cannot get otherwise.
