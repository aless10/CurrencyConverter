from convert_app.conf.config import ConvertAppConfiguration
from convert_app.app_factory import create_app, run_app


convert_app = create_app(ConvertAppConfiguration)

if __name__ == '__main__':
    run_app(convert_app)
