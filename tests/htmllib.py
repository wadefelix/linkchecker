# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2014 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
Default HTML parser handler classes.
"""

import sys


class HtmlPrinter:
    """
    Handles all functions by printing the function name and attributes.
    """

    def __init__ (self, fd=sys.stdout):
        """
        Write to given file descriptor.

        @param fd: file like object (default=sys.stdout)
        @type fd: file
        """
        self.fd = fd

    def _print (self, *attrs):
        """
        Print function attributes to stored file descriptor.

        @param attrs: list of values to print
        @type attrs: tuple
        @return: None
        """
        self.fd.write(self.mem)
        self.fd.write(str(attrs))

    def __getattr__ (self, name):
        """
        Remember the called method name in self.mem.

        @param name: attribute name
        @type name: string
        @return: method which just prints out its arguments
        @rtype: a bound function object
        """
        self.mem = name
        return self._print


class HtmlPrettyPrinter:
    """
    Print out all parsed HTML data in encoded form.
    Also stores error and warnings messages.
    """

    def __init__ (self, fd=sys.stdout, encoding="iso8859-1"):
        """
        Write to given file descriptor in given encoding.

        @param fd: file like object (default=sys.stdout)
        @type fd: file
        @param encoding: encoding (default=iso8859-1)
        @type encoding: string
        """
        self.fd = fd
        self.encoding = encoding

    def start_element (self, tag, attrs, element_text=None):
        """
        Print HTML start element.

        @param tag: tag name
        @type tag: string
        @param attrs: tag attributes
        @type attrs: dict
        @return: None
        """
        self._start_element(tag, attrs, ">", element_text)

    def start_end_element (self, tag, attrs, element_text=None):
        """
        Print HTML start-end element.

        @param tag: tag name
        @type tag: string
        @param attrs: tag attributes
        @type attrs: dict
        @return: None
        """
        self._start_element(tag, attrs, "/>", element_text)

    def _start_element (self, tag, attrs, end, element_text=None):
        """
        Print HTML element with end string.

        @param tag: tag name
        @type tag: string
        @param attrs: tag attributes
        @type attrs: dict
        @param end: either > or />
        @type end: string
        @return: None
        """
        self.fd.write("<%s" % tag.replace("/", ""))
        for key, val in sorted(attrs.items()):
            if val is None:
                self.fd.write(" %s" % key)
            else:
                self.fd.write(' %s="%s"' % (key, quote_attrval(val)))
        self.fd.write(end)
        if element_text:
            self.fd.write(element_text)

    def end_element (self, tag):
        """
        Print HTML end element.

        @param tag: tag name
        @type tag: string
        @return: None
        """
        self.fd.write("</%s>" % tag)


def quote_attrval (s):
    """
    Quote a HTML attribute to be able to wrap it in double quotes.

    @param s: the attribute string to quote
    @type s: string
    @return: the quoted HTML attribute
    @rtype: string
    """
    res = []
    for c in s:
        if ord(c) <= 127:
            # ASCII
            if c == '&':
                res.append("&amp;")
            elif c == '"':
                res.append("&quot;")
            else:
                res.append(c)
        else:
            res.append("&#%d;" % ord(c))
    return "".join(res)