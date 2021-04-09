from __future__ import annotations

import asyncio
import signal
from collections.abc import Awaitable
from typing import TypeVar

_T = TypeVar("_T")

__all__ = ("asyncio_run",)


def _cancel_all_tasks(loop: asyncio.AbstractEventLoop) -> None:
    to_cancel = asyncio.all_tasks(loop)
    if not to_cancel:
        return
    for task in to_cancel:
        task.cancel()
    loop.run_until_complete(asyncio.gather(*to_cancel, return_exceptions=True))
    for task in to_cancel:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler(
                {
                    "message": "unhandled exception during asyncio.run() shutdown",
                    "exception": task.exception(),
                    "task": task,
                }
            )


def asyncio_run(coro: Awaitable[_T]) -> _T:
    # asyncio.run() would have really been fine if not for lack of signal handlers...
    try:
        import uvloop
    except ImportError:
        pass
    else:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.add_signal_handler(signal.SIGTERM, lambda s: loop.stop())
    loop.add_signal_handler(signal.SIGINT, lambda s: loop.stop())

    task = loop.create_task(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()
    finally:
        try:
            _cancel_all_tasks(loop)
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.run_until_complete(loop.shutdown_default_executor())
        finally:
            asyncio.set_event_loop(None)
            loop.close()

    return task.result()
