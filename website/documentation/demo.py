import inspect
import re
from typing import Callable

import isort

from nicegui import helpers, ui

from .intersection_observer import IntersectionObserver as intersection_observer
from .windows import browser_window, python_window

UNCOMMENT_PATTERN = re.compile(r'^(\s*)# ?')


def uncomment(text: str) -> str:
    """non-executed lines should be shown in the code examples"""
    return UNCOMMENT_PATTERN.sub(r'\1', text)


def demo(f: Callable) -> Callable:
    with ui.column().classes('w-full items-stretch gap-8 no-wrap min-[1500px]:flex-row'):
        code = inspect.getsource(f).split('# END OF DEMO')[0].strip().splitlines()
        code = [line for line in code if not line.endswith("# HIDE")]
        while not code[0].strip().startswith('def') and not code[0].strip().startswith('async def'):
            del code[0]
        del code[0]
        if code[0].strip().startswith('"""'):
            while code[0].strip() != '"""':
                del code[0]
            del code[0]
        indentation = len(code[0]) - len(code[0].lstrip())
        code = [line[indentation:] for line in code]
        code = ['from nicegui import ui'] + [uncomment(line) for line in code]
        code = ['' if line == '#' else line for line in code]
        if not code[-1].startswith('ui.run('):
            code.append('')
            code.append('ui.run()')
        code = isort.code('\n'.join(code), no_sections=True, lines_after_imports=1)
        with python_window(classes='w-full max-w-[44rem]'):
            def copy_code():
                ui.run_javascript('navigator.clipboard.writeText(`' + code + '`)')
                ui.notify('Copied to clipboard', type='positive', color='primary')
            ui.markdown(f'````python\n{code}\n````')
            ui.icon('content_copy', size='xs') \
                .classes('absolute right-2 top-10 opacity-10 hover:opacity-80 cursor-pointer') \
                .on('click', copy_code, [])
        with browser_window(title=getattr(f, 'tab', None),
                            classes='w-full max-w-[44rem] min-[1500px]:max-w-[20rem] min-h-[10rem] browser-window') as window:
            spinner = ui.spinner(size='lg').props('thickness=2')

            async def handle_intersection():
                window.remove(spinner)
                if helpers.is_coroutine_function(f):
                    await f()
                else:
                    f()
            intersection_observer(on_intersection=handle_intersection)
    return f