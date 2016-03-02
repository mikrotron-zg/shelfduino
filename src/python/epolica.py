#!/usr/bin/env python

import lcd

import cherrypy
import os.path
import sys
import time
from cherrypy.lib.static import serve_file
from cherrypy import log

# web app
class WebRoot:
    @cherrypy.expose
    def default( self, *args, **kwargs ):
        filename = os.path.join(rootdir, 'epolicademo.html')
        lcd = ''
        msg = []
        if 'lcd' in kwargs: lcd = kwargs['lcd']
        
        if ( len( args ) > 0 ):
          #ucitavanje stanje LCD-a - TODO: tijekom inicijalizacije
          try:
            readContent( lcd )
          except:
            print sys.exc_info()
          #TODO: ovaj sadrzaj LCD-a dodati nekako u url
          if ( 'lcd16x2.html' == args[0] ):
            log.error("lcdsmall")
            filename=os.path.join(rootdir, 'lcd16x2.html')
          elif ( 'lcd20x4.html' == args[0] ):
            log.error("lcdbig")
            filename=os.path.join(rootdir, 'lcd20x4.html')

        if 'row1' in kwargs: msg.append( kwargs['row1'] )
        if 'row2' in kwargs: msg.append( kwargs['row2'] )
        if 'row3' in kwargs: msg.append( kwargs['row3'] )
        if 'row4' in kwargs: msg.append( kwargs['row4'] )
        
        if len(lcd) > 0:
				try:
					screen = lcds['lcd%s'%lcd]
					if len(msg) > 0:
						# we have the message - print it
						screen.write( msg )
						
						#snimanje stanja LCD-a!
						lcdfile = 'lcd%s.txt'%lcd
						print lcdfile, msg
						f = open( lcdfile, 'w' )
						for line in msg:
						  f.write(line)
						  f.write('\n')
						f.close()
					#else:
						# read existing screen content and add it to web form
						# TODO: process serving file!!!
						#kwargs['row1']="aman"
				except KeyError:
					log.error("lcd%s not found"%lcd)
            
        log.error("Serving %s" % filename)
        return serve_file(filename, content_type='text/html')

def readContent( lcd ):
    lcdfile = 'lcd%s.txt'%lcd
    f = open( lcdfile, 'r' )
    msg = []
    for line in f:
      print lcdfile, line.strip()
      msg.append(unicode(line.strip()))
    f.close()
    return msg

# main
lcds = {}

if __name__ == '__main__':

    lcds = lcd.scan()

    for i in range (1, len(lcds)+1):
      msg = readContent(i)
      print msg
      screen = lcds['lcd%s'%i]
      screen.write( msg )
      #time.sleep(1)
      
    #web app setup
    rootdir = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'html' )
    picdir = os.path.join(rootdir, 'pic')

    log.error( "Root dir: "+rootdir )
    log.error( "Pic dir: "+picdir )

    conf = {'/pic': {'tools.staticdir.on': True,
                     'tools.staticdir.dir': picdir,
                     'tools.staticdir.content_types': {'png': 'image/png',
                                                       'jpg': 'image/jpg'}}}

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 80,'log.screen': True})

    cherrypy.quickstart(WebRoot(), "/", config=conf)
