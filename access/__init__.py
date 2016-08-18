from pyramid.renderers import JSONP
from pyramid.config import Configurator
from pyramid.settings import aslist, asbool

from access import controller


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_renderer('jsonp', JSONP(param_name='callback', indent=4))

    hosts = aslist(settings['elasticsearch'])

    def add_index(request):
        return controller.stats(
            hosts=hosts
        )

    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('stats', '/api/v1/stats')
    config.add_route('document', '/api/v1/document')
    config.add_request_method(add_index, 'index', reify=True)
    config.scan()
    return config.make_wsgi_app()
