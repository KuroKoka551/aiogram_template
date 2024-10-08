from aiogram_i18n.cores import BaseCore, Jinja2Core
from dishka import AnyOf, Provider, Scope, provide
from jinja2 import BaseLoader, Environment

from aiogram_template.enums import Locale


class StubLoader(BaseLoader):
    def get_source(self, environment, template):
        del environment  # unused
        return template, template, lambda: True


class JinjaProvider(Provider):
    scope = Scope.APP

    @provide
    def get_jinja_env(
        self,
    ) -> Environment:
        return Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
            loader=StubLoader(),
        )

    @provide
    def get_jinja_core(self, env: Environment) -> AnyOf[BaseCore, Jinja2Core]:
        return Jinja2Core(
            path="translations/{locale}",
            default_locale=Locale.DEFAULT,
            environment=env,
            raise_key_error=False,
        )
