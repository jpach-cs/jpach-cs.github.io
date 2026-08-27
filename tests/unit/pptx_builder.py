'''
Build minimal but structurally honest .pptx archives in memory for the unit
tests. A .pptx is a zip of OOXML parts, so a handful of hand-written XML parts
is enough to exercise every code path in tools/pptx2marp.py without shipping
binary fixtures.
'''

from __future__ import annotations

import io
import zipfile
from collections.abc import Mapping
from pathlib import Path
from xml.sax.saxutils import escape

A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
MC_NS = 'http://schemas.openxmlformats.org/markup-compatibility/2006'
DGM_NS = 'http://schemas.openxmlformats.org/drawingml/2006/diagram'
REL_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'
REL_TYPE = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

XMLNS = (
    f'xmlns:a="{A_NS}" xmlns:p="{P_NS}" xmlns:r="{R_NS}" '
    f'xmlns:mc="{MC_NS}" xmlns:dgm="{DGM_NS}"'
)


def run(text: str, bold: bool = False, italic: bool = False, link_rel_id: str | None = None,
        typeface: str | None = None) -> str:
    '''
    One <a:r> run with optional bold/italic/hyperlink properties and an optional
    <a:latin typeface="..."> (set to a monospace font name to simulate pasted code).
    '''
    attrs = ''
    if bold:
        attrs += ' b="1"'
    if italic:
        attrs += ' i="1"'
    inner = f'<a:latin typeface="{typeface}"/>' if typeface is not None else ''
    if link_rel_id:
        inner += f'<a:hlinkClick r:id="{link_rel_id}"/>'
    run_props = f'<a:rPr{attrs}>{inner}</a:rPr>' if (attrs or inner) else ''
    return f'<a:r>{run_props}<a:t>{escape(text)}</a:t></a:r>'


def para(*children: str, lvl: int | None = None, bullet: bool = True) -> str:
    '''
    One <a:p> paragraph wrapping already-rendered run/br children.
    '''
    para_props = ''
    if lvl is not None or not bullet:
        lvl_attr = f' lvl="{lvl}"' if lvl is not None else ''
        bunone = '<a:buNone/>' if not bullet else ''
        para_props = f'<a:pPr{lvl_attr}>{bunone}</a:pPr>'
    return f'<a:p>{para_props}{"".join(children)}</a:p>'


def shape_xml(*paragraphs: str, ph_type: str | None = None, has_placeholder: bool = True,
              txbody: bool = True, tx_box: bool = False) -> str:
    '''
    One <p:sp> shape. ph_type=None with has_placeholder=True gives an index-only
    placeholder (a body); has_placeholder=False gives a freeform text box. tx_box=True adds
    <p:cNvSpPr txBox="1"/>, as PowerPoint marks a pasted-in text box (e.g. pasted code).
    '''
    placeholder_xml = ''
    if has_placeholder:
        type_attr = f' type="{ph_type}"' if ph_type else ''
        placeholder_xml = f'<p:ph{type_attr} idx="1"/>'
    cnv_sp_pr = '<p:cNvSpPr txBox="1"/>' if tx_box else '<p:cNvSpPr/>'
    body = f'<p:txBody>{"".join(paragraphs)}</p:txBody>' if txbody else ''
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="1" name="s"/>{cnv_sp_pr}'
        f'<p:nvPr>{placeholder_xml}</p:nvPr></p:nvSpPr>{body}</p:sp>'
    )


def xfrm_xml(ext: tuple[int, int] | None) -> str:
    '''An <a:xfrm> with a zero offset and the given (cx, cy) EMU <a:ext>, or '' if None.'''
    if ext is None:
        return ''
    cx, cy = ext
    return f'<a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'


def pic(embed: str | None = None, link: str | None = None, descr: str = '', name: str = 'Picture',
        **appearance) -> str:
    '''
    One <p:pic> shape referencing media by relationship id. `appearance` may hold `ext`
    (its displayed (cx, cy) EMU size, via <p:spPr><a:xfrm>) and/or `src_rect` (an
    <a:srcRect l t r b> crop).
    '''
    ext: tuple[int, int] | None = appearance.get('ext')
    src_rect: tuple[int, int, int, int] | None = appearance.get('src_rect')
    blip_attrs = ''
    if embed:
        blip_attrs += f' r:embed="{embed}"'
    if link:
        blip_attrs += f' r:link="{link}"'
    descr_attr = f' descr="{descr}"' if descr else ''
    src_rect_xml = ''
    if src_rect is not None:
        left, top, right, bottom = src_rect
        src_rect_xml = f'<a:srcRect l="{left}" t="{top}" r="{right}" b="{bottom}"/>'
    sp_pr = f'<p:spPr>{xfrm_xml(ext)}</p:spPr>' if ext is not None else ''
    return (
        f'<p:pic><p:nvPicPr><p:cNvPr id="2" name="{name}"{descr_attr}/></p:nvPicPr>'
        f'<p:blipFill><a:blip{blip_attrs}/>{src_rect_xml}</p:blipFill>{sp_pr}</p:pic>'
    )


def pic_without_blip() -> str:
    '''
    A <p:pic> with no <a:blip> at all - malformed but seen in the wild.
    '''
    return '<p:pic><p:nvPicPr><p:cNvPr id="2" name="x"/></p:nvPicPr><p:blipFill/></p:pic>'


def table(rows: list[list[str]]) -> str:
    '''
    A <p:graphicFrame> holding an <a:tbl>. Each cell is one paragraph of plain text;
    an empty string leaves the cell without text.
    '''
    row_xml = ''
    for row in rows:
        cell_xml = ''
        for cell in row:
            body = f'<a:txBody>{para(run(cell))}</a:txBody>' if cell else ''
            cell_xml += f'<a:tc>{body}</a:tc>'
        row_xml += f'<a:tr>{cell_xml}</a:tr>'
    return graphic_frame(
        'http://schemas.openxmlformats.org/drawingml/2006/table', f'<a:tbl>{row_xml}</a:tbl>'
    )


def graphic_frame(uri: str, inner: str = '', ext: tuple[int, int] | None = None) -> str:
    '''
    A <p:graphicFrame> with the given graphicData uri and inner XML, and an optional
    <p:xfrm> (the graphicFrame's own transform, a sibling of <a:graphic> - distinct from a
    <p:pic>'s <p:spPr><a:xfrm>) sizing it to the given (cx, cy) EMU.
    '''
    frame_xfrm = f'<p:xfrm><a:off x="0" y="0"/><a:ext cx="{ext[0]}" cy="{ext[1]}"/></p:xfrm>' \
        if ext is not None else ''
    return (
        f'<p:graphicFrame>{frame_xfrm}<a:graphic><a:graphicData uri="{uri}">{inner}</a:graphicData>'
        '</a:graphic></p:graphicFrame>'
    )


def ole_graphic_frame(preview_pic_xml: str, ext: tuple[int, int] | None = None,
                       choice_xml: str = '') -> str:
    '''
    A <p:graphicFrame> embedding an OLE object, in the real-world shape PowerPoint emits:
    an <mc:AlternateContent> whose <mc:Fallback> wraps a preview picture (a complete
    `pic(...)`-built <p:pic> element) in <p:oleObj>.
    '''
    inner = (
        f'<mc:AlternateContent><mc:Choice xmlns:v="urn:x">{choice_xml}</mc:Choice>'
        f'<mc:Fallback><p:oleObj>{preview_pic_xml}</p:oleObj></mc:Fallback>'
        '</mc:AlternateContent>'
    )
    return graphic_frame(
        'http://schemas.openxmlformats.org/presentationml/2006/ole', inner, ext=ext
    )


def diagram(dm_rel_id: str) -> str:
    '''
    A SmartArt <p:graphicFrame> pointing at a data part through r:dm.
    '''
    return graphic_frame(
        'http://schemas.openxmlformats.org/drawingml/2006/diagram',
        f'<dgm:relIds r:dm="{dm_rel_id}" r:lo="" r:qs="" r:cs=""/>',
    )


def slide_xml(*shapes: str, sptree: bool = True) -> str:
    '''
    A complete slide part wrapping the given shapes in <p:cSld><p:spTree>.
    '''
    tree = f'<p:spTree>{"".join(shapes)}</p:spTree>' if sptree else ''
    return f'<?xml version="1.0"?><p:sld {XMLNS}><p:cSld>{tree}</p:cSld></p:sld>'


def notes_xml(*paragraphs: str, body: bool = True, txbody: bool = True) -> str:
    '''
    A notesSlide part whose body placeholder holds the given paragraphs.
    '''
    shape = shape_xml(*paragraphs, ph_type='body' if body else 'sldImg', txbody=txbody)
    return f'<?xml version="1.0"?><p:notes {XMLNS}><p:cSld><p:spTree>{shape}</p:spTree></p:cSld></p:notes>'


def rels_xml(relationships: list[tuple[str, str, str]], external: set[str] | None = None) -> str:
    '''
    A .rels part from (rId, type-suffix, target) triples.
    '''
    external = external or set()
    items = ''
    for rel_id, rtype, target in relationships:
        mode = ' TargetMode="External"' if rel_id in external else ''
        items += f'<Relationship Id="{rel_id}" Type="{REL_TYPE}/{rtype}" Target="{target}"{mode}/>'
    return f'<?xml version="1.0"?><Relationships xmlns="{REL_NS}">{items}</Relationships>'


def presentation_xml(rel_ids: list[str], sld_size: tuple[int, int] | None = None) -> str:
    '''
    ppt/presentation.xml with the slide id list in the given order, and an optional
    <p:sldSz cx cy> (defaults, when omitted, to the converter's own 16:9 fallback).
    '''
    ids = ''.join(f'<p:sldId id="{256 + i}" r:id="{rel_id}"/>' for i, rel_id in enumerate(rel_ids))
    sld_sz = f'<p:sldSz cx="{sld_size[0]}" cy="{sld_size[1]}"/>' if sld_size is not None else ''
    return (
        f'<?xml version="1.0"?><p:presentation {XMLNS}><p:sldIdLst>{ids}</p:sldIdLst>{sld_sz}'
        '</p:presentation>'
    )


def build_pptx(parts: Mapping[str, str | bytes]) -> bytes:
    '''
    Zip arbitrary parts into an in-memory .pptx. Keys are package paths.
    '''
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as archive:
        for name, data in parts.items():
            archive.writestr(name, data.encode('utf-8') if isinstance(data, str) else data)
    return buf.getvalue()


def simple_deck(slides: list[str], extra: dict[str, str | bytes] | None = None,
                slide_rels: dict[int, str] | None = None,
                sld_size: tuple[int, int] | None = None) -> bytes:
    '''
    A well-formed deck: ppt/presentation.xml ordering slide1..N, plus any extra parts,
    optional per-slide .rels (1-based index -> rels xml), and an optional <p:sldSz>.
    '''
    parts: dict[str, str | bytes] = {}
    rel_ids = []
    presentation_rels = []
    for i, xml in enumerate(slides, start=1):
        parts[f'ppt/slides/slide{i}.xml'] = xml
        rel_ids.append(f'rId{i}')
        presentation_rels.append((f'rId{i}', 'slide', f'slides/slide{i}.xml'))
    parts['ppt/presentation.xml'] = presentation_xml(rel_ids, sld_size=sld_size)
    parts['ppt/_rels/presentation.xml.rels'] = rels_xml(presentation_rels)
    for i, xml in (slide_rels or {}).items():
        parts[f'ppt/slides/_rels/slide{i}.xml.rels'] = xml
    parts.update(extra or {})
    return build_pptx(parts)


def write_pptx(path: Path, data: bytes) -> Path:
    '''
    Write deck bytes to disk and return the path, for tests that go through Path APIs.
    '''
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path
