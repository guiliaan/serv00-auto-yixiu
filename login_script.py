2025-10-19 11:23:27,399 - INFO - 🟢 脚本启动！
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\logging\__init__.py", line 1103, in emit
    stream.write(msg + self.terminator)
UnicodeEncodeError: 'gbk' codec can't encode character '\U0001f7e2' in position 33: illegal multibyte sequence
Call stack:
  File "E:\桌面\脚本\serv00\1.py", line 260, in <module>
    asyncio.run(main())
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\asyncio\runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\asyncio\base_events.py", line 636, in run_until_complete
    self.run_forever()
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\asyncio\base_events.py", line 603, in run_forever
    self._run_once()
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\asyncio\base_events.py", line 1909, in _run_once
    handle._run()
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\asyncio\events.py", line 80, in _run
    self._context.run(self._callback, *self._args)
  File "E:\桌面\脚本\serv00\1.py", line 204, in main
    logger.info('🟢 脚本启动！')
Message: '🟢 脚本启动！'
Arguments: ()
2025-10-19 11:23:27,404 - ERROR - ❌ accounts.json 不存在！
--- Logging error ---
Traceback (most recent call last):
  File "E:\桌面\脚本\serv00\1.py", line 207, in main
    async with aiofiles.open('accounts.json', mode='r', encoding='utf-8') as f:
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\site-packages\aiofiles\base.py", line 73, in __aenter__
    return await self
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\site-packages\aiofiles\base.py", line 69, in __await__
    self._obj = yield from self._coro.__await__()
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\site-packages\aiofiles\threadpool\__init__.py", line 93, in _open
    f = await loop.run_in_executor(executor, cb)
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\concurrent\futures\thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
FileNotFoundError: [Errno 2] No such file or directory: 'accounts.json'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\logging\__init__.py", line 1103, in emit
    stream.write(msg + self.terminator)
UnicodeEncodeError: 'gbk' codec can't encode character '\u274c' in position 34: illegal multibyte sequence
Call stack:
  File "E:\桌面\脚本\serv00\1.py", line 260, in <module>
    asyncio.run(main())
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\asyncio\runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\asyncio\base_events.py", line 636, in run_until_complete
    self.run_forever()
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\asyncio\windows_events.py", line 321, in run_forever
    super().run_forever()
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\asyncio\base_events.py", line 603, in run_forever
    self._run_once()
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\asyncio\base_events.py", line 1909, in _run_once
    handle._run()
  File "C:\Users\pc\AppData\Local\Programs\Python\Python310\lib\asyncio\events.py", line 80, in _run
    self._context.run(self._callback, *self._args)
  File "E:\桌面\脚本\serv00\1.py", line 213, in main
    logger.error('❌ accounts.json 不存在！')
Message: '❌ accounts.json 不存在！'
Arguments: ()
