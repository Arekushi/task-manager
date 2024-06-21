
from dynaconf import Dynaconf

dynaconf_settings = Dynaconf(
    settings_files=[
        'settings.json'
    ],
    load_dotenv=True,
    envvar_prefix=False
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
