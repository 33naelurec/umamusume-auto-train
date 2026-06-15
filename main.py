import sys
import subprocess
import warnings
import os
warnings.filterwarnings(
  "ignore",
  category=UserWarning,
  module=r"torch\.utils\.data\.dataloader"
)
MIN = (3, 10)
MAX = (3, 14)

if not (MIN <= sys.version_info < MAX):
  # ask the launcher what it has
  out = subprocess.check_output(
    ["py", "--list"],
    text=True,
    stderr=subprocess.DEVNULL
  )

  candidates = []
  for line in out.splitlines():
    line = line.strip()
    if line.startswith("-V:"):
      v = line.split()[0][3:]
      try:
        major, minor = map(int, v.split("."))
        if (major, minor) >= MIN and (major, minor) < MAX:
          candidates.append(v)
      except ValueError:
        pass

  if not candidates:
    raise RuntimeError("No compatible Python 3.10-3.13 installed")

  best = sorted(candidates)[-1]

  p = subprocess.Popen(
    ["py", f"-{best}", *sys.argv],
    stdin=sys.stdin,
    stdout=sys.stdout,
    stderr=sys.stderr
  )
  p.wait()
  sys.exit(p.returncode)

from utils.tools import sleep
import pygetwindow as gw
import threading
import uvicorn
import keyboard

import time
import sys
import socket

import utils.constants as constants
from utils.log import info, warning, error, debug, args, init_logging

from core.skeleton import career_lobby
import core.config as config
import core.bot as bot
from server.main import app
from update_config import update_config
from utils.notifications import on_started

bot.windows_window = None

def focus_umamusume():
  if bot.use_adb:
    info("Using ADB no need to focus window.")
    constants.adjust_constants_x_coords(offset=-155)
    return True
  try:
    import pyautogui
    from utils.pyautogui_actions import screen_to_world_conversion_init
    win = gw.getWindowsWithTitle("Umamusume")
    target_window = next((w for w in win if w.title.strip() == "Umamusume"), None)
    if not target_window:
      info(f"Couldn't get the steam version window, trying {config.WINDOW_NAME}.")
      if not config.WINDOW_NAME:
        error("Window name cannot be empty! Please set window name in the config.")
        return False
      win = gw.getWindowsWithTitle(config.WINDOW_NAME)
      target_window = next((w for w in win if w.title.strip() == config.WINDOW_NAME), None)
      if not target_window:
        error(f"Couldn't find target window named \"{config.WINDOW_NAME}\". Please double check your window name config.")
        return False

      constants.adjust_constants_x_coords()
      if target_window.isMinimized:
        target_window.restore()
      else:
        target_window.minimize()
        sleep(0.2)
        target_window.restore()
        sleep(0.5)
      pyautogui.press("esc")
      pyautogui.press("f11")
      time.sleep(5)
      close_btn = pyautogui.locateCenterOnScreen("assets/buttons/bluestacks/close_btn.png", confidence=0.8, minSearchTime=2)
      if close_btn:
        pyautogui.click(close_btn)
      return True

    if target_window.width < 1920 or target_window.height < 1080:
      error(f"Your resolution is {target_window.width} x {target_window.height}. Minimum expected size is 1920 x 1080.")
      return
    if target_window.isMinimized:
      target_window.restore()
    else:
      target_window.minimize()
      sleep(0.2)
      target_window.restore()
      sleep(0.5)
    bot.windows_window = target