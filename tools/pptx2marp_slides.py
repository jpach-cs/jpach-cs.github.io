'''
Slide-structure helpers for pptx2marp: walking a slide's shape tree, choosing
between the branches of <mc:AlternateContent>, and reading PowerPoint's autofit
scale. Kept apart from the renderer so each module stays readable on its own.
'''

from __future__ import annotations

_NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
}


def _qn(prefix: str, tag: str) -> str:
    return '{%s}%s' % (_NS[prefix], tag)


P_SP, P_PIC, P_GRAPHICFRAME, P_CXNSP, P_GRPSP, P_SPPR = (
    _qn('p', tag) for tag in ('sp', 'pic', 'graphicFrame', 'cxnSp', 'grpSp', 'spPr')
)
MC_ALTERNATECONTENT, MC_FALLBACK, MC_CHOICE = (
    _qn('mc', tag) for tag in ('AlternateContent', 'Fallback', 'Choice')
)
A_T, A_BLIPFILL, A_NORMAUTOFIT = (_qn('a', tag) for tag in ('t', 'blipFill', 'normAutofit'))
M_OMATH = _qn('m', 'oMath')


def iter_shapes_with_group_flag(container, in_group: bool = False):
    '''
    Like `iter_shapes`, but also yields whether each shape is nested inside a <p:grpSp>
    group: a group has its own <a:xfrm> with a chOff/chExt child coordinate space, so a
    picture's own <a:xfrm> inside one is not directly in slide coordinates. Composing the
    group's transform chain (recursively, for nested groups, with rotation) is more than
    this converter attempts - callers instead use this flag to skip that picture's size
    and warn instead of emitting a wrong one.
    '''
    for child in container:
        tag = child.tag
        if tag == MC_ALTERNATECONTENT:
            branch = pick_alternate_branch(child)
            if branch is not None:
                yield from iter_shapes_with_group_flag(branch, in_group)
        elif tag == P_GRPSP:
            yield from iter_shapes_with_group_flag(child, True)
        elif tag in (P_SP, P_PIC, P_GRAPHICFRAME, P_CXNSP):
            yield child, in_group


def pick_alternate_branch(alternate_content):
    '''
    Choose which branch of an <mc:AlternateContent> to render. Office writes a text
    box that contains equations as a Choice holding the real paragraphs (prose runs
    plus <m:oMath>) and a Fallback holding a picture-filled <p:sp> of the box as
    rendered, with a single-space text body. The picture is the faithful form of a
    paragraph with equations - flattening OMML to text loses fractions, subscripts
    and sums - so it wins whenever the Choice has math. Otherwise the Choice is
    used when it has text and the Fallback carries none of its own (an empty
    shape), and the Fallback, being schema-plain OOXML, in every remaining case.
    '''
    choice = alternate_content.find(MC_CHOICE)
    fallback = alternate_content.find(MC_FALLBACK)
    if choice is None or fallback is None:
        return choice if fallback is None else fallback
    if choice.find(f'.//{M_OMATH}') is not None and fallback.find(f'.//{P_SPPR}/{A_BLIPFILL}') is not None:
        return fallback
    choice_has_text = any((t.text or '').strip() for t in choice.iter(A_T))
    fallback_has_text = any((t.text or '').strip() for t in fallback.iter(A_T))
    if choice_has_text and not fallback_has_text:
        return choice
    return fallback


def iter_shapes(container):
    '''
    Yield the content-bearing shapes (<p:sp>, <p:pic>, <p:graphicFrame>, <p:cxnSp>)
    inside `container` in document order, flattening <p:grpSp> groups and
    <mc:AlternateContent> (preferring Fallback, guaranteed schema-plain OOXML).
    '''
    for shape, _in_group in iter_shapes_with_group_flag(container):
        yield shape


def autofit_scale(slide_root) -> int:
    '''
    The smallest font scale PowerPoint's "shrink text on overflow" autofit applied
    to any text box on the slide, as a percentage (100 when no box was shrunk).
    Stored as <a:normAutofit fontScale="77500"/> in thousandths of a percent.
    '''
    scales = []
    for autofit in slide_root.iter(A_NORMAUTOFIT):
        try:
            scales.append(int(autofit.get('fontScale', '100000')) // 1000)
        except ValueError:
            continue
    return min(scales, default=100)
