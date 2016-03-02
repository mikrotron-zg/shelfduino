#!/usr/bin/env python

import cherrypy
import os.path
from cherrypy.lib.static import serve_file
from cherrypy import log

class Root:
    @cherrypy.expose
    def default( self, *args, **kwargs ):
        filename = os.path.join(rootdir, 'epolicademo.html')
        if ( len( args ) > 0 ):
          if ( 'lcd16x2.html' == args[0] ):
            log.error("lcdsmall")
            filename=os.path.join(rootdir, 'lcd16x2.html')
          elif ( 'lcd20x4.html' == args[0] ):
            log.error("lcdbig")
            filename=os.path.join(rootdir, 'lcd20x4.html')

        row1 = ''
        row2 = ''
        row3 = ''
        row4 = ''
        lcd = ''
        try:
          lcd = kwargs['lcd']
          row1 = kwargs['row1']
          row2 = kwargs['row2']
          row3 = kwargs['row3']
          row4 = kwargs['row4']
        except KeyError:
          log.error( "no key" )
        log.error("Serving %s" % filename)
        log.error("lcd %s:\n%s\n%s\n%s\n%s" % (lcd, row1,row2,row3,row4) )
        return serve_file(filename, content_type='text/html')

if __name__ == '__main__':
    rootdir = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'html' )
    picdir = os.path.join(rootdir, 'pic')

    log.error( "Root dir: "+rootdir )
    log.error( "Pic dir: "+picdir )

    conf = {'/pic': {'tools.staticdir.on': True,
                     'tools.staticdir.dir': picdir,
                     'tools.staticdir.content_types': {'png': 'image/png',
                                                       'jpg': 'image/jpg'}}}

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 80,'log.screen': True})

    cherrypy.quickstart(Root(), "/", config=conf)
