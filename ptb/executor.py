import importlib
import inspect
import logging
import os
import pkgutil
import sys
import types
from typing import Callable, Dict, NamedTuple, Set, Type, cast
from ptb import utils
from ptb.interfaces import Intent
from telegram.ext import Application


logger = logging.getLogger(__name__)


class TimestampModule(NamedTuple):
    timestamp: float
    module: types.ModuleType


class IntentExecutor:
    def __init__(self) -> None:
        self._modules: Dict[str, TimestampModule] = {}
        self._loaded: Set[Type[Intent]] = set()
        self.intents: Dict[str, Callable] = {}

    def register(self, package: str | types.ModuleType, app: Application) -> None:
        self.register_package(package)
        for _, handler in self.intents.items():
            app.add_handler(handler())

    def register_package(self, package: str | types.ModuleType) -> None:
        try:
            self._import_submodules(package)
        except ImportError:
            logger.exception(f"Failed to register package `{package}`")
            sys.exit(1)

        self._register_all_intents()

    def register_intent(self, intent: Type[Intent] | Intent) -> None:
        if inspect.isclass(intent):
            intent = cast(Type[Intent], intent)
            if intent in self._loaded:
                return

            self._loaded.add(intent)
            intent = intent()

            if isinstance(intent, Intent):
                self.register_function(intent.name(), intent.handler)
            else:
                raise Exception(
                    "You can only register instances or subclasses of "
                    "type Intent. If you want to directly register "
                    "a function, use `register_function` instead."
                )

    def register_function(self, name: str, f: Callable) -> None:
        if name in self.intents:
            logger.info(f"Re-registed handler for `{name}`")
        else:
            logger.info(f"Registed handler for `{name}`")

        self.intents[name] = f

    def reload(self) -> None:
        to_reload = self._find_modules_to_reload()
        any_module_reloaded = False

        for path, (timestamp, module) in to_reload.items():
            try:
                new_module = importlib.reload(module)
                self._modules[path] = TimestampModule(timestamp, new_module)
                logger.info(
                    f"Reloaded module/package: '{module.__name__}' "
                    f"(file: '{os.path.relpath(path)}')"
                )
                any_module_reloaded = True
            except (SyntaxError, ImportError):
                logger.exception(
                    f"Error while reloading module/package: '{module.__name__}' "
                    f"(file: '{os.path.relpath(path)}'):"
                )
                logger.info("Please fix the error(s) in the Python file and try again.")

        if any_module_reloaded:
            self._register_all_intents()

    def _import_module(self, name: str) -> types.ModuleType:
        module = importlib.import_module(name)
        module_file = getattr(module, "__file__", None)
        if module_file:
            # If the module we're importing is a namespace package (a package
            # without __init__.py), then there's nothing to watch for the
            # package itself.
            timestamp = os.path.getmtime(module_file)
            self._modules[module_file] = TimestampModule(timestamp, module)
        return module

    def _import_submodules(
        self, package: str | types.ModuleType, recursive: bool = True
    ) -> None:
        if isinstance(package, str):
            package = self._import_module(package)

        # check a py file or directory
        if not getattr(package, "__path__", None):
            return

        for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = ".".join([package.__name__, name])
            self._import_module(full_name)
            if recursive and is_pkg:
                self._import_submodules(full_name)

    def _register_all_intents(self) -> None:
        intents = utils.all_subclasses(Intent)
        for intent in intents:
            self.register_intent(intent)

    def _find_modules_to_reload(self) -> Dict[str, TimestampModule]:
        to_reload = {}
        for path, (timestamp, module) in self._modules.items():
            try:
                new_timestamp = os.path.getmtime(path)
            except OSError:
                # ignore  missing file
                continue
            if new_timestamp > timestamp:
                to_reload[path] = TimestampModule(new_timestamp, module)
        return to_reload
