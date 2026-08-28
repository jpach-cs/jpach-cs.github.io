#!/usr/bin/env python3
'''
Picture and OLE-preview rendering for tools/pptx2marp.py: resolving a <p:pic>'s media and
displayed size, sizing it onto the Marp canvas, deduplicating a picture referenced more
than once on one slide, and pulling an OLE object's preview picture out of its
graphicData subtree. Split out of pptx2marp.py to keep that module under its line cap -
see its module docstring. Self-contained (its own namespace/qualified-name constants) so
it never needs to import back from pptx2marp.py at runtime; `SlideContext` is only used as
a (lazily-evaluated, `from __future__ import annotations`) type hint, resolved for static
analysis under `TYPE_CHECKING`.
'''

from __future__ import annotations

import posixpath
import re
import zipfile
from typing import TYPE_CHECKING
from xml.etree import ElementTree as ET

from pptx2marp_text import (
    DEFAULT_SLIDE_HEIGHT_EMU,
    DEFAULT_SLIDE_WIDTH_EMU,
    compute_image_size_prefix,
    uncropped_extent,
)

if TYPE_CHECKING:
    from pptx2marp import SlideContext

_NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def _qn(prefix: str, tag: str) -> str:
    '''Build a Clark-notation qualified tag name (see pptx2marp.qn).'''
    return '{%s}%s' % (_NS[prefix], tag)


P_PIC, P_BLIPFILL, P_NVPICPR, P_CNVPR, P_SPPR, P_SLDSZ = (
    _qn('p', tag) for tag in ('pic', 'blipFill', 'nvPicPr', 'cNvPr', 'spPr', 'sldSz')
)
A_BLIP, A_XFRM, A_EXT, A_SRCRECT, A_BLIPFILL = (
    _qn('a', tag) for tag in ('blip', 'xfrm', 'ext', 'srcRect', 'blipFill')
)
P_NVSPPR = _qn('p', 'nvSpPr')


def blip_fill_of(shape):
    '''
    The <a:blipFill> of a picture, wherever the shape keeps it: a <p:pic> holds it as
    <p:blipFill>; a picture-filled <p:sp> (Office's fallback rendering of a text box
    with equations) holds it inside <p:spPr>. None when the shape has no picture.
    '''
    fill = shape.find(P_BLIPFILL)
    if fill is None:
        fill = shape.find(f'{P_SPPR}/{A_BLIPFILL}')
    return fill
R_EMBED, R_LINK = (_qn('r', tag) for tag in ('embed', 'link'))

IMAGE_EXTS = {'.png', '.gif', '.svg', '.jpg', '.jpeg'}


def handle_pic(picture_el, context: 'SlideContext'):
    '''
    Render one <p:pic> shape into an image reference, returning
    (alt_text, package_media_path) or None if it could not be resolved.
    '''
    fill = blip_fill_of(picture_el)
    blip = fill.find(A_BLIP) if fill is not None else None
    cnv_pr = picture_el.find(f'{P_NVPICPR}/{P_CNVPR}')
    if cnv_pr is None:
        cnv_pr = picture_el.find(f'{P_NVSPPR}/{P_CNVPR}')
    alt = ''
    if cnv_pr is not None:
        alt = cnv_pr.get('descr') or cnv_pr.get('name') or ''
    alt = re.sub(r'[\[\]()]', '', alt).strip() or 'image'
    if blip is None:
        return None
    embed = blip.get(R_EMBED)
    if embed:
        entry = context.relationships.get(embed)
        if not entry or entry[1] not in context.names:
            context.warnings.append(
                f'slide {context.slide_index}: image relationship {embed} could not be resolved'
            )
            return None
        return (alt, entry[1])
    link = blip.get(R_LINK)
    if link:
        entry = context.relationships.get(link)
        url = entry[1] if entry else 'unknown'
        context.warnings.append(f'slide {context.slide_index}: linked (non-embedded) image skipped: {url}')
        return None
    return None


def get_picture_extent(picture_el) -> tuple[int, int] | None:
    '''Return a <p:pic>'s displayed (cx, cy) EMU size from <p:spPr><a:xfrm><a:ext>, or
    None when the size is inherited from the layout (no <a:xfrm> present).'''
    ext = picture_el.find(f'{P_SPPR}/{A_XFRM}/{A_EXT}')
    if ext is None:
        return None
    try:
        return int(ext.get('cx', '')), int(ext.get('cy', ''))
    except ValueError:
        return None


def get_src_rect(picture_el) -> tuple[int, int, int, int] | None:
    '''Return a <p:pic>'s <a:srcRect> crop as (left, top, right, bottom) percentages in
    thousandths of a percent, or None if the picture is not cropped.'''
    fill = blip_fill_of(picture_el)
    src_rect = fill.find(A_SRCRECT) if fill is not None else None
    if src_rect is None:
        return None
    try:
        left, top, right, bottom = (int(src_rect.get(side, '0')) for side in ('l', 't', 'r', 'b'))
    except ValueError:
        return None
    sides = (left, top, right, bottom)
    return sides if any(sides) else None


def get_slide_size(archive: zipfile.ZipFile) -> tuple:
    '''
    Read the deck's real slide size in EMU from ppt/presentation.xml's <p:sldSz>, falling
    back to the standard 16:9 12192000 x 6858000 EMU (1280x720px) size on any failure.
    '''
    try:
        pres = ET.fromstring(archive.read('ppt/presentation.xml'))
        sld_sz = pres.find(P_SLDSZ)
        if sld_sz is not None:
            return int(sld_sz.get('cx', '')), int(sld_sz.get('cy', ''))
    except (ET.ParseError, KeyError, ValueError):
        pass
    return DEFAULT_SLIDE_WIDTH_EMU, DEFAULT_SLIDE_HEIGHT_EMU


def build_image_markdown_line(alt: str, asset_name: str, size_prefix: str, context: 'SlideContext') -> str:
    '''Build one already-registered image's Markdown line, flagging a non-web format.'''
    ext = posixpath.splitext(asset_name)[1].lower()
    img_line = f'![{size_prefix}{alt}](assets/{asset_name})'
    if ext not in IMAGE_EXTS:
        img_line += (
            f'\n<!-- pptx2marp: {asset_name} is a {ext.lstrip(".").upper()} file; many '
            'browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if '
            'this slide looks blank. -->'
        )
        context.warnings.append(f'slide {context.slide_index}: non-web image format kept as-is: {asset_name}')
    return img_line


def image_size_prefix(extent: tuple[int, int] | None, context: 'SlideContext', in_group: bool) -> str:
    '''
    Compute a picture's Marp size prefix from its (cx, cy) EMU extent, or '' when there is
    none to size from. A picture nested inside a <p:grpSp> group gets no size either - its
    own <a:xfrm> is in the group's untransformed child coordinate space - and a warning is
    logged instead, since silently sizing it from the wrong space would be worse than not
    sizing it at all.
    '''
    if extent is None:
        return ''
    if in_group:
        context.warnings.append(
            f'slide {context.slide_index}: image size ignored (nested inside a group; '
            'group transform not applied)'
        )
        return ''
    return compute_image_size_prefix(*extent, context.slide_width_emu, context.slide_height_emu)


def render_image_shape(shape, context: 'SlideContext', in_group: bool = False) -> str | None:
    '''
    Render a <p:pic> shape into a Markdown image line, sized from its own <a:xfrm> when
    present (`w:NNNpx`, scaled to the 1280px Marp canvas, or `bg` when it covers >= 85% of
    the slide's area), or None if the picture could not be resolved.
    '''
    picture = handle_pic(shape, context)
    if picture is None:
        return None
    alt, media_path = picture
    asset_name = context.registry.register(context.archive, media_path, context.warnings, context.slide_index)
    if asset_name is None:
        return None
    size_prefix = image_size_prefix(get_picture_extent(shape), context, in_group)
    return build_image_markdown_line(alt, asset_name, size_prefix, context)


def widest_extent(
    first: tuple[int, int] | None, second: tuple[int, int] | None,
) -> tuple[int, int] | None:
    '''Component-wise max of two optional (cx, cy) extents, keeping whichever side is set.'''
    if first is None:
        return second
    if second is None:
        return first
    return max(first[0], second[0]), max(first[1], second[1])


def uncrop(
    extent: tuple[int, int] | None, src_rect: tuple[int, int, int, int] | None,
) -> tuple[int, int] | None:
    '''Un-crop `extent` by `src_rect` when both are known, otherwise pass `extent` through.'''
    if extent is None or src_rect is None:
        return extent
    return uncropped_extent(*extent, src_rect)


def render_picture(shape, context: 'SlideContext', in_group: bool, body_blocks: list) -> None:
    '''
    Append one <p:pic>'s Markdown to `body_blocks`, deduplicating a picture referenced
    more than once on this slide (context.seen_pictures, fresh per slide): an exact repeat
    (same media path and the same, or no, <a:srcRect> crop) is dropped silently; a repeat
    cropped differently is treated as another slice of one source image - the slide keeps
    its single existing reference, resized to the widest un-cropped extent implied by any
    slice seen so far, with one warning that the crop was dropped.
    '''
    picture = handle_pic(shape, context)
    if picture is None:
        return
    alt, media_path = picture
    src_rect = get_src_rect(shape)
    extent = get_picture_extent(shape)
    seen = context.seen_pictures.get(media_path)
    if seen is None:
        img_line = render_image_shape(shape, context, in_group)
        if img_line is None:
            return
        body_blocks.append(img_line)
        context.seen_pictures[media_path] = {
            'srcrects': {src_rect}, 'block_index': len(body_blocks) - 1,
            'extent': uncrop(extent, src_rect), 'alt': alt, 'warned': False,
        }
        return
    if src_rect in seen['srcrects']:
        return
    seen['srcrects'].add(src_rect)
    if not seen['warned']:
        context.warnings.append(
            f'slide {context.slide_index}: image {posixpath.basename(media_path)} is '
            'cropped in the source (srcRect); shown uncropped'
        )
        seen['warned'] = True
    seen['extent'] = widest_extent(seen['extent'], uncrop(extent, src_rect))
    asset_name = context.registry.path_to_asset.get(media_path)
    if seen['extent'] is not None and asset_name is not None:
        size_prefix = image_size_prefix(seen['extent'], context, in_group)
        body_blocks[seen['block_index']] = build_image_markdown_line(seen['alt'], asset_name, size_prefix, context)


def render_ole_preview(graphic_data, frame_xfrm, context: 'SlideContext') -> str | None:
    '''
    Render an OLE-embedded object's preview picture - found anywhere in its graphicData
    subtree, typically inside <mc:Fallback><p:oleObj><p:pic> - as a normal image, sized
    from the graphicFrame's own <p:xfrm> (the preview <p:pic> does not carry its own).
    Returns None when the subtree holds no preview picture to fall back to.
    '''
    preview_pic = next(graphic_data.iter(P_PIC), None)
    if preview_pic is None:
        return None
    picture = handle_pic(preview_pic, context)
    if picture is None:
        return None
    alt, media_path = picture
    asset_name = context.registry.register(context.archive, media_path, context.warnings, context.slide_index)
    if asset_name is None:
        return None
    extent = None
    if frame_xfrm is not None:
        ext = frame_xfrm.find(A_EXT)
        if ext is not None:
            try:
                extent = int(ext.get('cx', '')), int(ext.get('cy', ''))
            except ValueError:
                extent = None
    size_prefix = compute_image_size_prefix(
        *extent, context.slide_width_emu, context.slide_height_emu
    ) if extent else ''
    return build_image_markdown_line(alt, asset_name, size_prefix, context)
