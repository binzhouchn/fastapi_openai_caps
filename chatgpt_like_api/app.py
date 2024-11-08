from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException

from exceptions.http_error import http_error_handler
from exceptions.validation_error import http422_error_handler

class App(FastAPI):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
        self.add_exception_handler(HTTPException, http_error_handler)
        self.add_exception_handler(RequestValidationError, http422_error_handler)

    def include_router(self, router, prefix='', **kwargs):
        """
            from fastapi import FastAPI, APIRouter
            router = APIRouter(route_class=LoggingRoute)

        :param router:
        :param prefix:
        :param kwargs:
        :return:
        """

        super().include_router(router, prefix=prefix, **kwargs)

    def run(self, app=None, host="0.0.0.0", port=8000, workers=1, access_log=True, reload=False, **kwargs):
        """

        :param app:
            f"{Path(__file__).stem}:{app}"
            app字符串可开启热更新 reload
        :param host:
        :param port:
        :param workers:
        :param access_log:
        :param kwargs:
        :return:
        """

        import uvicorn

        uvicorn.config.LOGGING_CONFIG['formatters']['access']['fmt'] = f"""
        🔥 %(asctime)s - %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s
        """.strip()
        uvicorn.run(
            app if app else self,  #
            host=host, port=port, workers=workers, access_log=access_log, reload=reload, app_dir=None,
            **kwargs
        )

if __name__ == '__main__':
    from routes import base, completions #embeddings
    app = App()
    app.include_router(base.router, tags=["baseinfo"])
    app.include_router(completions.router, tags=["completions"])
    # app.include_router(embeddings.router, tags=["embeddings"])
    app.run(host='localhost', port=8899)
