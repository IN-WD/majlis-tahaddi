"""مركاز العمدة — stencil-style portrait badge (original artwork).
Two-tone woodcut look: indigo shapes, cream face, inside a Hejazi arch with a Sadu band."""
import math
INK = "#2B2D6E"; RED = "#B3261E"; SAFF = "#F2A900"; CREAM = "#FBF3E4"; SAND = "#F4E9D8"


def _stripes(cid, col):
    dx, dy = 1 / math.hypot(1, 1.1), -1.1 / math.hypot(1, 1.1)
    px, py = -dy, dx
    out = ''
    for o in range(-60, 70, 22):
        cx, cy = 100 + o * px, 64 + o * py
        x0, y0, x1, y1 = cx - 80 * dx, cy - 80 * dy, cx + 80 * dx, cy + 80 * dy
        out += (f'<path d="M{x0:.0f} {y0:.0f} Q{cx - 10 * px:.0f} {cy - 10 * py:.0f} {x1:.0f} {y1:.0f}" '
                f'stroke="{col}" stroke-width="11" stroke-linecap="round" fill="none"/>')
    return f'<g clip-path="url(#{cid})">{out}</g>'


def portrait(p='m3', ink=INK, face=CREAM, accent=RED):
    turban = 'M38 122 C26 90 34 48 64 32 C84 20 116 20 136 32 C166 48 174 90 162 122 C150 104 128 96 100 96 C72 96 50 104 38 122 Z'
    folds = ''.join(f'<path d="{d}" fill="{face}"/>' for d in (
        'M46 110 C52 78 74 54 100 46 C80 60 62 82 54 112 Z',
        'M60 100 C68 76 86 62 104 58 C90 70 76 86 70 102 Z',
        'M44 82 C52 58 70 42 94 34 C76 46 60 62 52 86 Z',
        'M104 42 C128 46 148 64 156 94 C144 74 126 60 104 52 Z',
        'M108 60 C126 64 142 78 148 102 C138 86 124 74 106 68 Z',
        'M110 28 C132 30 150 42 160 64 C146 50 130 42 110 36 Z'))
    return f'''
<path d="M60 186 L100 220 L140 186 L150 236 L50 236 Z" fill="{face}"/>
<path d="M100 220 L92 236 L108 236 Z" fill="{ink}"/>
<path d="M64 104 C64 84 78 76 100 76 C122 76 136 84 136 104 L136 140 C136 168 120 186 100 186 C80 186 64 168 64 140 Z" fill="{face}"/>
<path d="M128 112 C134 132 132 160 114 180 C122 158 126 136 123 114 Z" fill="{ink}"/>
<path d="{turban}" fill="{ink}"/>
{folds}
<path d="M40 120 C58 104 80 99 100 99 C120 99 142 104 160 120 C142 110 120 106 100 106 C80 106 58 110 40 120 Z" fill="{accent}"/>
<path d="M70 110 C80 101 90 101 97 107 C88 105 80 107 72 114 Z" fill="{ink}"/>
<path d="M103 105 C111 94 124 93 133 99 C124 99 114 102 106 111 Z" fill="{ink}"/>
<ellipse cx="84" cy="120" rx="6.5" ry="3.8" fill="{ink}"/><ellipse cx="117" cy="118" rx="6.5" ry="3.8" fill="{ink}"/>
<circle cx="86" cy="119" r="1.3" fill="{face}"/><circle cx="119" cy="117" r="1.3" fill="{face}"/>
<path d="M101 120 C100 132 97 141 92 147 C98 150 105 150 110 146 C105 145 102 142 101 139 Z" fill="{ink}"/>
<path d="M100 154 C90 145 72 145 62 153 C56 157 53 151 57 144 C50 151 51 162 62 164 C74 166 88 160 100 160 C112 160 126 166 138 164 C149 162 150 151 143 144 C147 151 144 157 138 153 C128 145 110 145 100 154 Z" fill="{ink}"/>
<path d="M88 168 Q100 176 112 168" stroke="{ink}" stroke-width="4" stroke-linecap="round" fill="none"/>'''


def arch(p='m3', w=220, bg=RED, face=CREAM, accent=INK, saff=SAFF, ink=INK):
    arch_d = 'M18 250 V104 A82 82 0 0 1 182 104 V250 Z'
    sadu = ''.join(f'<path d="M{x} 250 L{x + 11} 236 L{x + 22} 250 Z" fill="{saff}"/>' for x in range(18, 182, 22))
    return (f'<svg viewBox="0 0 200 262" width="{w}" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="M8 260 V104 A92 92 0 0 1 192 104 V260 Z" fill="{accent}"/>'
            f'<clipPath id="{p}a"><path d="{arch_d}"/></clipPath>'
            f'<path d="{arch_d}" fill="{bg}"/>'
            f'<g clip-path="url(#{p}a)"><g transform="translate(-8,14) scale(1.08)">{portrait(p, ink, face, RED if bg != RED else SAFF)}</g>'
            f'<rect x="0" y="234" width="200" height="30" fill="{accent}"/>{sadu}</g></svg>')
