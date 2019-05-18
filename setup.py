from distutils.core import setup, Extension
setup(name="rclib", version="1.0",
      ext_modules=[Extension("rclib", ["rclibmodule.c", "RadioControlProtocolC/rc_lib.c"])])
