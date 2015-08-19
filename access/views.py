from pyramid.view import view_config
from pyramid.response import Response
import pyramid.httpexceptions as exc

@view_config(route_name='index', request_method='GET')
def index(request):
    return Response('Access Stats API by SciELO')
