#! /usr/bin/python
'''
Copyright (C) 2015

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''
import sys, os
sys.path.append(os.path.dirname(sys.argv[0]))  #?

import inkex, simplestyle

default = { 'display':'inline','enable-background':'accumulate',
            'fill':'#000000', 'fill-opacity':'1', 'fill-rule':'nonzero',
            'marker':'none',
            'opacity':'1', 'overflow':'visible',
            'stroke':'none', 'stroke-width':'1', 'stroke-linecap':'butt', 'stroke-linejoin':'miter', 'stroke-miterlimit':'4',
            'stroke-opacity':'1', 'stroke-dasharray':'none', 'stroke-dashoffset':'0',
            'visibility':'visible'}

class reduceStyle(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
    def effect(self):
        if len(self.selected)==0:
            self.getAttribs(self.document.getroot())
        else:
            for id,node in self.selected.iteritems():
                self.getAttribs(node)

    def getAttribs(self,node):
        self.changeStyle(node)
        for child in node:
            self.getAttribs(child)

    def changeStyle(self,node):
        if 'style' in node.attrib:
            style=node.get('style')
            if style!='':
                declarations = style.split(';')
                new_declarations = []
                for i,decl in enumerate(declarations):
                    parts = decl.split(':', 2)
                    if len(parts) == 2:
                        (prop, val) = parts
                        prop = prop.strip().lower()
                        insert = True
                        if prop in default:
                            d = default[prop]
                            if d == val:
                                insert = False
                        if insert:
                            new_declarations.append(prop + ':' + val)
                node.set('style', ';'.join(new_declarations))


if __name__ == '__main__':   #pragma: no cover
    e = reduceStyle()
    e.affect()

