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

import inkex, simplepath, simplestyle, simpletransform, sys, cubicsuperpath, math

class Dots(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
	def effect(self):
		for id, node in self.selected.iteritems():
			if node.tag == '{http://www.w3.org/2000/svg}path':
				path=node
				break
		else:
			sys.stderr.write('Need one path selected\n')
			return

		pts = cubicsuperpath.parsePath(path.get('d'))

		if 'transform' in path.keys():
			trans = path.get('transform')
			trans = simpletransform.parseTransform(trans)
			simpletransform.applyTransformToPath(trans, pts[i])

		gtext = inkex.etree.SubElement(path.xpath('..')[0], inkex.addNS('g','svg'), {} )
		gdots = inkex.etree.SubElement(path.xpath('..')[0], inkex.addNS('g','svg'), {} )

		size = 10
		if 'style' in path.attrib:
			style=path.get('style')
			if style!='':
				styles=style.split(';')
            			for i in range(len(styles)):
					if styles[i].startswith('stroke-width'):
						if ( styles[i].endswith('px') or styles[i].endswith('cm') ) :
							size=float(styles[i][len('stroke-width:'):-2])*2
						else:
							size=float(styles[i][len('stroke-width:'):])*2
#		if len(pts[0])>2:
#			size = math.sqrt(math.pow(pts[0][0][0][0]-pts[0][1][0][0],2)+math.pow(pts[0][0][0][1]-pts[0][1][0][1],2))/10

		it = 0
		for sub in pts:
			for p in sub:
				if it == 0:
					style = { 'stroke': 'none', 'fill': 'black' }
					x0 = p[0][0]
					y0 = p[0][1]
					circ_attribs = {'id':'pt0','style':simplestyle.formatStyle(style),'cx':str(x0), 'cy':str(y0),'r':str(size)}
					circle = inkex.etree.SubElement(gdots, inkex.addNS('circle','svg'), circ_attribs )
				else:
					clone_attribs = { 'x':'0', 'y':'0', 'transform':'translate(%f,%f)' % (p[0][0]-x0,p[0][1]-y0) }
					clone = inkex.etree.SubElement(gdots, inkex.addNS('use','svg'), clone_attribs )
					xlink = inkex.addNS('href','xlink')
					clone.set(xlink, '#pt0')

				text_style = { 'font-size':'%dpx' % (size*2.4), 'fill':'black', 'font-family':'DejaVu Sans', 'text-anchor':'middle' }
				text_attribs = { 'x':str(p[0][0]), 'y':str(p[0][1]-size*1.8), 'style':simplestyle.formatStyle(text_style) }
				text = inkex.etree.SubElement(gtext, inkex.addNS('text','svg'), text_attribs)
				tspan = inkex.etree.SubElement(text , 'tspan', {inkex.addNS('role','sodipodi'): 'line'})
            			tspan.text = '%d' % ( it+1 )

				it+=1


if __name__ == '__main__':   #pragma: no cover
    e = Dots()
    e.affect()

