# -*- coding: utf-8 -*-
"""
    Módulo de Usuarios

    Autor: Jorge Toro [jolthgs@gmail.com]
"""
import web
import sys
from common import Sesion
from view import render
from config import DB

urls = (
  "", "re",
  "/", "monitoreo",
  "/eventos", "eventos",
  "/reporte", "reporte",
  "/updateevent", "updateevent",
  "/reportdayjson", "reportdayjson",
  "/listeventjson", "listeventjson",
)

class re:
    def GET(self):
        raise web.seeother('/')

class monitoreo:
    @Sesion
    def GET(self):
        from db import listingVehicleClient
        return render.user.monitoreo(web.ctx.session, listingVehicleClient(web.ctx.session.clienteId)) 

class eventos:
    @Sesion
    def GET(self):
        from db import eventsClient
        return render.user.eventos(web.ctx.session, eventsClient(web.ctx.session.clienteId))

class reporte:
    @Sesion
    def GET(self):
        from db import listingVehicleClient
        return render.user.reporte(web.ctx.session, listingVehicleClient(web.ctx.session.clienteId)) 

class updateevent:
    @Sesion
    def GET(self):
        i = web.input(id=None)
        try:
            DB.update('eventos', where='id=$i.id', user_state='t', vars=locals())
        except:
            print "Error Inesperado /user/updateevent:", sys.exc_info()    
        raise web.seeother('/eventos')

class reportdayjson:
    @Sesion
    def GET(self):
        import simplejson as json 
        from db import reportday
        i = web.input(id=None, fecha=None)
        print "VEHICLE ID: ", i.id
        print "FECHA: ", i.fecha
        web.header('content-Type', 'application/json')
        def dthandler(obj):
            obj.fecha = obj.fecha.strftime("%F %H:%M:%S")
            return obj
        return json.dumps([dthandler(row) for row in reportday(i.id, i.fecha)])

class listeventjson:
    @Sesion
    def GET(self):
        import simplejson as json 
        from db import countEventClient
        web.header('content-Type', 'application/json')
        return json.dumps([row for row in countEventClient(web.ctx.session.clienteId)])
 

app_user = web.application(urls, locals())
