# Licensed under a 3-clause BSD style license, see LICENSE.

"""The one tree walk in the package.

Everything that combines a parse tree or an AST bottom-up goes through `fold`,
so that depth is bounded by memory rather than by the interpreter stack. Nothing
here or in its callers may recurse: a long chain of operators comes back from
`to_root` fully parenthesized, and re-parsing that nests one level per pair.
"""

from collections.abc import Callable, Sequence
from typing import Any, TypeVar

Node = TypeVar("Node")
Result = TypeVar("Result")


def fold(
    root: Node,
    expand: Callable[[Node], tuple[Sequence[Node], Callable[..., Result]]],
) -> Result:
    """Combine a tree bottom-up into a single value.

    `expand` decomposes one node into the children still to be folded and a
    builder that turns their folded results into this node's own result. It runs
    on a node before that node's children are visited, so errors it raises come
    out in the order a recursive walk would have produced them.

    Each stack entry is either a node still to be expanded, or a
    ``(builder, child count)`` pair sitting underneath the children it is
    waiting on; finished children accumulate on `results`. Nodes therefore must
    not themselves be tuples.
    """
    results: list[Result] = []
    stack: list[Any] = [root]
    while stack:
        item = stack.pop()
        # An exact type check, not isinstance: it is what tells a pending
        # builder apart from a node, and nodes are never plain tuples. A node
        # that subclassed tuple would satisfy isinstance and be mistaken for a
        # builder, so the stricter check is the point here.
        if type(item) is tuple:  # pylint: disable=unidiomatic-typecheck
            build, nargs = item
            if nargs:
                parts = results[-nargs:]
                del results[-nargs:]
                results.append(build(*parts))
            else:
                results.append(build())
            continue
        children, build = expand(item)
        # The children are pushed in reverse so they pop left to right, and the
        # builder underneath them runs once their results are in place.
        stack.append((build, len(children)))
        stack.extend(reversed(children))
    return results[0]
