from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import subprocess
import time
from Quartz import (
    CGEventCreateScrollWheelEvent,
    CGEventPost,
    kCGScrollEventUnitPixel,
    kCGHIDEventTap
)
from Quartz import (
    CGDisplayBounds,
    CGMainDisplayID,
    CGEventCreateMouseEvent,
    CGEventPost,
    kCGEventMouseMoved,
    kCGEventLeftMouseDown,
    kCGEventLeftMouseUp,
    kCGMouseButtonLeft,
    kCGHIDEventTap
)

def move_grid(x, y):
    display = CGMainDisplayID()
    bounds = CGDisplayBounds(display)

    W = bounds.size.width
    H = bounds.size.height

    px = (x - 0.5) * (W / 9)
    py = H - (y - 0.5) * (H / 9)

    point = (px, py)

    CGEventPost(
        kCGHIDEventTap,
        CGEventCreateMouseEvent(None, kCGEventMouseMoved, point, kCGMouseButtonLeft)
    )

def click_grid(x, y):
    display = CGMainDisplayID()
    bounds = CGDisplayBounds(display)

    W = bounds.size.width
    H = bounds.size.height

    px = (x - 0.5) * (W / 9)
    py = H - (y - 0.5) * (H / 9)

    point = (px, py)

    # Move
    CGEventPost(
        kCGHIDEventTap,
        CGEventCreateMouseEvent(None, kCGEventMouseMoved, point, kCGMouseButtonLeft)
    )

    # Click
    CGEventPost(
        kCGHIDEventTap,
        CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, point, kCGMouseButtonLeft)
    )
    CGEventPost(
        kCGHIDEventTap,
        CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, point, kCGMouseButtonLeft)
    )

def grid101_point(x, y):
    display = CGMainDisplayID()
    bounds = CGDisplayBounds(display)

    W = bounds.size.width
    H = bounds.size.height

    px = (x / 100) * W
    py = H - (y / 100) * H   # invert Y axis

    return (px, py)

def click_point(point):
    CGEventPost(
        kCGHIDEventTap,
        CGEventCreateMouseEvent(None, kCGEventMouseMoved, point, kCGMouseButtonLeft)
    )
    CGEventPost(
        kCGHIDEventTap,
        CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, point, kCGMouseButtonLeft)
    )
    CGEventPost(
        kCGHIDEventTap,
        CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, point, kCGMouseButtonLeft)
    )

def smooth_scroll(delta, steps, delay=0.01):
    for _ in range(steps):
        event = CGEventCreateScrollWheelEvent(
            None,
            kCGScrollEventUnitPixel,
            1,
            delta
        )
        CGEventPost(kCGHIDEventTap, event)
        time.sleep(delay)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

# ──────────────── BASIC COMMANDS ────────────────


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_text = update.message.text
    text = raw_text.lower()

# ──────────────── DICTIONARIES ────────────────

    ARROW_KEYS = {
        "h": 123,  # left
        "k": 124,  # right
        "u": 126,  # up
        "j": 125   # down
    }


    TAB_KEYCODE = 48




# ========================= SIMPLE COMMANDS LIST =============================

# ──────────────── SELECTION COMMANDS ────────────────

# COPY (⌘ + C)
    if text == "c":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "c" using command down'
        ])
        await update.message.reply_text("📋 Copied")

# PASTE (⌘ + V)
    elif text == "v":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "v" using command down'
        ])
        await update.message.reply_text("📥 Pasted")

# CUT (⌘ + X)
    elif text == "x":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "x" using command down'
        ])
        await update.message.reply_text("✂️ Cut")

# SELECT ALL (⌘ + A)
    elif text == "a":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "a" using command down'
        ])
        await update.message.reply_text("🖱️ Selected all")

# UNDO (⌘ + Z)
    elif text == "z":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "z" using command down'
        ])
        await update.message.reply_text("↩️ Undo")

# xx → Select all text and delete (Cmd + A → Backspace)
    elif text == "xx":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "a" using {command down}',
            "-e", 'delay 0.1',
            "-e", 'tell application "System Events" to keystroke "x" using {command down}'
        ])
        await update.message.reply_text("🗑️ Cleared all text")

# bb → Select all text and delete (Cmd + A → Backspace)
    elif text == "bb":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "a" using {command down}',
            "-e", 'delay 0.1',
            "-e", 'tell application "System Events" to key code 51'
        ])
        await update.message.reply_text("🗑️ Cleared all text")


# cc → Select all text and copy (Cmd + A → Cmd + C)
    elif text == "cc":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "a" using {command down}',
            "-e", 'delay 0.1',
            "-e", 'tell application "System Events" to keystroke "c" using {command down}'
        ])
        await update.message.reply_text("📋 Copied all text")


# ──────────────── TYPE TEXT COMMANDS ────────────────

# TYPE + ENTER 
    elif text.endswith(" p"):
        to_type = raw_text[:-2]  # remove " .e"
        to_type = to_type.replace('"', '\\"')

        subprocess.run([
            "osascript",
            "-e", f'tell application "System Events" to keystroke "{to_type}"'
        ])

        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key code 36'
        ])

        await update.message.reply_text("📝 Typed text and pressed Enter")


# TYPE TEXT (n ...)
    elif text.startswith("n "):
        to_type = raw_text[2:]  # keep original case
        to_type = to_type.replace('"', '\\"')

        script = f'''
        set the clipboard to "{to_type}"
        tell application "System Events"
            keystroke "v" using command down
        end tell
        '''

        subprocess.run(["osascript", "-e", script])
        await update.message.reply_text("📝 Pasted text via clipboard")

   
# OPTION (ALT) + Q pressed 3 times
    elif text == "brightness":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "q" using option down',
            "-e", 'tell application "System Events" to keystroke "q" using option down',
            "-e", 'tell application "System Events" to keystroke "q" using option down'
        ])
        await update.message.reply_text("⌥Q ⌥Q ⌥Q (Alt+Q x3)")

# ──────────────── SCREENSHOTS ────────────────

    # s → SCREENSHOT (Alt + D)
    elif text == "s":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "d" using option down'
        ])
        await update.message.reply_text("📸 Screenshot triggered")


    # sr → Screen recording panel (Cmd + Shift + 5)
    elif text == "sr":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "5" using {command down, shift down}'
        ])
        await update.message.reply_text("🎥 Screen recording panel opened")

    # sc → Screenshot to clipboard (Cmd + Shift + Option + S)
    elif text == "sc":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "s" using {command down, shift down, option down}'
        ])
        await update.message.reply_text("📋 Screenshot copied to clipboard")

    # sa → Screenshot selected area (Option + S)
    elif text == "sa":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "s" using {option down}'
        ])
        await update.message.reply_text("✂️ Select area for screenshot")

# ──────────────── SYSTEM-WIDE ZOOM COMMANDS ────────────────
# Uses Cmd + Option + + / -
# System Zoom RESET (Cmd + Option + 0)
    elif text == "io":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key code 29 using {command down, option down}'
        ])
        await update.message.reply_text("🔄 Screen zoom reset")

# Zoom RESET (Cmd + 0)
    elif text == "zio":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "0" using command down'
        ])
        await update.message.reply_text("🔄 Zoom reset")

# ──────────────── OTHER COMMANDS ────────────────

# ALT + X
    elif text == "aa":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "x" using option down'
        ])
        await update.message.reply_text("⌥X pressed")

# ALT + I
    elif text == "invert":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "i" using option down'
        ])
        await update.message.reply_text("⌥I pressed")

# Search Inside VS code
    elif text == "ff":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "f" using {command down}'
        ])
        await update.message.reply_text("🔍 Find (Cmd+F)")
        
# Fullscreen YouTube video (press F) (ff)
    elif text == "f":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "f"'
        ])
        await update.message.reply_text("⛶ Fullscreen toggled (YouTube)")

# Fullscreen Mode On (fs)
    elif text == "fs":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "f" using {command down, control down}'
        ])
        await update.message.reply_text("🎬 Fullscreen video")       

# Minimize Screen (ms)
    elif text == "ms":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "m" using {command down}'
        ])
        await update.message.reply_text("🧹 Window minimized (Cmd + M)")

# Get IP address of Wi-Fi
    elif text == "ip":
        result = subprocess.run(
            ["osascript", "-e", 'do shell script "ipconfig getifaddr en1"'],
            capture_output=True,
            text=True
        )
        netip = result.stdout.strip()
        await update.message.reply_text(f"{netip}")

# Lock Mac Screen (Cmd + Ctrl + Q)
    elif text == "lock":
        subprocess.run([
            "osascript",
            "-e",
            'tell application "System Events" to keystroke "q" using {command down, control down}'
        ])
        await update.message.reply_text("🔒 Mac locked successfully")


# ──────────────── APP SHORTCUT COMMANDS ────────────────

# CTRL + ALT + W
    elif text == "wp":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "w" using {control down, option down}'
        ])
        await update.message.reply_text("Whatsapp Open")

# CTRL + ALT + L
    elif text == "cg":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "l" using {control down, option down}'
        ])
        await update.message.reply_text("ChatGPT Open")

# CTRL + ALT + C
    elif text == "gc":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "c" using {control down, option down}'
        ])
        await update.message.reply_text("Chrome Open")

# CTRL + ALT + S
    elif text == "st":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "s" using {control down, option down}'
        ])
        await update.message.reply_text("Settings Open")

# ──────────────── FILE COMMANDS ────────────────

# CTRL + SPACE
    elif text == "fl":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key code 49 using {control down}'
        ])
        await update.message.reply_text("Files Open")

# CMD + SHIFT + H
    elif text == "fh":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "h" using {shift down, command down}'
        ])
        await update.message.reply_text("Home Open")
    
# ──────────────── OTHER COMMANDS ────────────────

# CMD + L
    elif text == "lc":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "l" using command down'
        ])
        await update.message.reply_text("Location selected")

# CMD + S
    elif text == "sv":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "s" using command down'
        ])
        await update.message.reply_text("File saved")

# CMD + SHIFT + T
    elif text == "hst":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "t" using {shift down, command down}'
        ])
        await update.message.reply_text("History Tab open")

# Close app command
    elif text == "q":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key down command',
            "-e", 'tell application "System Events" to keystroke "q"',
            "-e", 'delay 0.3',  # holds the key for 0.3 seconds
            "-e", 'tell application "System Events" to key up command'
        ])
        await update.message.reply_text("App closed (CMD+Q)")

# Window left and right (cmd+left/right arrow)
    elif text == "wh":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key down control',
            "-e", 'tell application "System Events" to key code 123',
            "-e", 'tell application "System Events" to key up control'
        ])
        await update.message.reply_text("Ctrl + Left Arrow")

    elif text == "wk":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key down control',
            "-e", 'tell application "System Events" to key code 124',
            "-e", 'tell application "System Events" to key up control'
        ])
        await update.message.reply_text("Ctrl + Right Arrow")

# pd → Cmd + Delete (Permanently Delete)
    elif text == "pd":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key code 51 using {command down}'
        ])
        await update.message.reply_text("⌫ Cmd + Delete")

# ──────────────── NEW CODES ────────────────

# Cmd + Option + D (Dark Mode)
    elif text == "dark":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "d" using {control down, option down}'
        ])
        await update.message.reply_text("Dark Mode Toggle")

# Open Terminal (Cmd + Space)
    elif text == "t":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke space using {command down}'
        ])
        await update.message.reply_text("🖥️ Terminal opened")

# Open Bluestack App
    elif text == "bs":
        subprocess.run(["open", "-a", "BlueStacks"])
        await update.message.reply_text("📱 BlueStacks opened")

# ──────────────── SHUTDOWN/RESTART COMMANDS ────────────────

# Shutdown Mac
    elif text == "shutdown":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to shut down'
        ])
        await update.message.reply_text("🛑 Shutting down Mac")

# Restart Mac
    elif text == "restart":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to restart'
        ])
        await update.message.reply_text("🔁 Restarting Mac")

# ──────────────── WEBSITE SHORTCUT COMMANDS ────────────────

# YouTube
    elif text == "yb":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "youtube.com"'
        ])
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key code 36'
        ])
        await update.message.reply_text("🌐 YouTube opened")

# Telegram Web
    elif text == "tg":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "web.telegram.org"'
        ])
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key code 36'
        ])
        await update.message.reply_text("🌐 Telegram Web opened")


# GeeksForGeeks
    elif text == "gfg":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "geeksforgeeks.org"'
         ])
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key code 36'
        ])
        await update.message.reply_text("🌐 GeeksForGeeks opened")

# Udemy
    elif text == "ud":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "udemy.com"'
        ])
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key code 36'
        ])
        await update.message.reply_text("🌐 Udemy opened")

# 100xDevs
    elif text == "hx":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "100xdevs.com"'
        ])
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key code 36'
        ])
        await update.message.reply_text("🌐 100xDevs opened")

# Coursera
    elif text == "cs":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "coursera.org"'
        ])
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key code 36'
        ])
        await update.message.reply_text("🌐 Coursera opened")

# Open new tab in Chrome (Cmd + T)
    elif text == "nt":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "t" using {command down}'
        ])
        await update.message.reply_text("🆕 New tab opened")

# Close current tab in Chrome (Cmd + W)
    elif text == "ct":
        subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to keystroke "w" using {command down}'
        ])
        await update.message.reply_text("❌ Tab closed")



# ──────────────── CODE UPDATE ────────────────

    elif text == "cdu":
        subprocess.run([
            "bash",
            "-c",
            'pkill -f "/Users/navneetpriyadarshi/tbot.py" && '
            'pkill -f "bash -c source ~/tbot_env/bin/activate && python3 ~/tbot.py" && '
            'source ~/tbot_env/bin/activate && '
            'nohup python3 ~/tbot.py > ~/tbot.log 2>&1 &'
        ])
        await update.message.reply_text("♻️ Bot updated & restarted successfully")
    

# ──────────────── TERMINAL ────────────────
# t command
    elif text.startswith("t "):
        cmd = text[2:].strip()

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )

            output = result.stdout.strip()
            error = result.stderr.strip()

            if not output and not error:
                reply = "✅ Command executed (no output)"
            else:
                reply = f"🖥️ Output:\n{output or error}"

            # Telegram has message length limits
            await update.message.reply_text(reply[:4000])

        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")




# ========================= GENERIC COMMANDS LIST =============================

# Zoom IN (i, i<n>)
    elif text.startswith("i"):
        num = text[1:]

        if num == "":
            count = 8          # i → zoom in 8x
        elif num.isdigit() and 1 <= int(num) <= 9:
            count = int(num)
        else:
            await update.message.reply_text("❌ Use i or i1–i9 only")
            return

        script = f'''
        tell application "System Events"
            repeat {count} times
                keystroke "+" using {{command down, option down}}
                delay 0.05
            end repeat
        end tell
        '''
        subprocess.run(["osascript", "-e", script])

        await update.message.reply_text(f"🔍 Screen zoomed IN ×{count}")

# Zoom OUT (o, o<n>)
    elif text.startswith("o"):
        num = text[1:]

        if num == "":
            count = 8          # o → zoom out 8x
        elif num.isdigit() and 1 <= int(num) <= 9:
            count = int(num)
        else:
            await update.message.reply_text("❌ Use o or o1–o9 only")
            return

        script = f'''
        tell application "System Events"
            repeat {count} times
                keystroke "-" using {{command down, option down}}
                delay 0.05
            end repeat
        end tell
        '''
        subprocess.run(["osascript", "-e", script])

        await update.message.reply_text(f"🔎 Screen zoomed OUT ×{count}")


# ──────────────── Whatsapp Automatic Screenshot Send ────────────────

# scw <name> (navneet priyadarshi for scw without name)
    elif text.startswith("scw"):
        parts = text.split(maxsplit=1)

        # Default name
        name = "Navneet Priyadarshi"

        # If user typed a name after scw
        if len(parts) > 1:
            name = parts[1]

        script = f'''
        tell application "System Events"

            -- Screenshot to clipboard (Cmd + Shift + Option + S)
            keystroke "s" using {{command down, shift down, option down}}
            delay 1

            -- Open WhatsApp
            tell application "WhatsApp" to activate
            delay 2

            -- Search (Cmd + F)
            keystroke "f" using {{command down}}
            delay 0.5

            -- Type contact name
            keystroke "{name}"
            delay 0.6

            -- Down arrow twice
            key code 125
            delay 0.2
            key code 125
            delay 0.2

            -- Enter to open chat
            key code 36
            delay 0.6

            -- Paste screenshot
            keystroke "v" using {{command down}}
            delay 0.3

            -- Send
            key code 36

            -- Wait before closing
            delay 10

            -- Quit WhatsApp
            keystroke "q" using {{command down}}

        end tell
        '''
        subprocess.run(["osascript", "-e", script])
        await update.message.reply_text(f"📸 Screenshot sent to {name}")


# ──────────────── Whatsapp Automatic TEXT ────────────────

# tw <name>/<text>
    elif text.startswith("tw "):
        content = text[3:].strip()  # Remove "tw " from start
        if "/" in content:
            name, message = content.split("/", 1)  # Split at first /
            name = name.strip()
            message = message.strip()
        else:
            # If no /, treat the whole thing as name and use default message
            name = content
            message = "Hello!"  # Default message

        script = f'''
        tell application "WhatsApp"
            activate
        end tell
        delay 2
        tell application "System Events"
            keystroke "f" using {{command down}}
            delay 1
            keystroke "{name}"
            delay 1
            key code 125  -- down arrow
            delay 0.2
            key code 125  -- down arrow again
            delay 0.2
            key code 36   -- enter
            delay 0.5
            keystroke "{message}"
            delay 0.5
            key code 36   -- enter to send
        end tell
        '''
        subprocess.run(["osascript", "-e", script])
        await update.message.reply_text(f"📩 Message sent to {name}")


# ──────────────── ARROW KEYS (1–100 SUPPORT) ────────────────

    elif text and text[0] in ARROW_KEYS:
        key = text[0]
        num = text[1:]

        if num == "":
            count = 6   # default
        elif num.isdigit() and 1 <= int(num) <= 100:
            count = int(num)
        else:
            await update.message.reply_text("❌ Use h/k/u/j or h1–h100")
            return

        key_code = ARROW_KEYS[key]

        for _ in range(count):
            subprocess.run([
                "osascript",
                "-e", f'tell application "System Events" to key code {key_code}'
            ])

        direction = {
            "h": "⬅️ Left",
            "k": "➡️ Right",
            "u": "⬆️ Up",
            "j": "⬇️ Down"
        }[key]

        await update.message.reply_text(f"{direction} ×{count}")

# ──────────────────── MOUSE ────────────────────────
# mu<n> → scroll up n seconds
# mj<n> → scroll down n seconds
# mu   → scroll up 1 second
# mj   → scroll down 1 second
# muu  → scroll to top
# mjj  → scroll to bottom
# cxy  → mouse click at (x,y)
# cx,y   precise click

# SCROLL TO TOP — very fast
    elif text == "muu":
        smooth_scroll(12, 120)   # strong + short
        await update.message.reply_text("⬆️ Jumped to top")

# SCROLL TO BOTTOM — very fast
    elif text == "mjj":
        smooth_scroll(-12, 120)  # strong + short
        await update.message.reply_text("⬇️ Jumped to bottom")

# SCROLL UP
    elif text.startswith("mu"):
        num = text[2:]

        if num == "":
            seconds = 1
        elif num.isdigit() and 1 <= int(num) <= 9:
            seconds = int(num)
        else:
            await update.message.reply_text("❌ Use mu or mu1–mu9")
            return

        smooth_scroll(8, seconds * 60)  # 1.5× faster
        await update.message.reply_text(f"🧈 Smooth scroll up for {seconds}s")

# SCROLL DOWN
    elif text.startswith("mj"):
        num = text[2:]

        if num == "":
            seconds = 1
        elif num.isdigit() and 1 <= int(num) <= 9:
            seconds = int(num)
        else:
            await update.message.reply_text("❌ Use mj or mj1–mj9")
            return

        smooth_scroll(-8, seconds * 60)  # 1.5× faster
        await update.message.reply_text(f"🧈 Smooth scroll down for {seconds}s")

# GRID CLICK (cXY)
    elif text.startswith("c") and len(text) == 3 and text[1].isdigit() and text[2].isdigit():
        x = int(text[1])
        y = int(text[2])

        if 1 <= x <= 9 and 1 <= y <= 9:
            click_grid(x, y)
            await update.message.reply_text(f"🖱️ Clicked at grid ({x},{y})")
        else:
            await update.message.reply_text("❌ Use c11–c99 (1–9 only)")

# GRID MOVE (mXY)
    elif text.startswith("m") and len(text) == 3 and text[1].isdigit() and text[2].isdigit():
        x = int(text[1])
        y = int(text[2])

        if 1 <= x <= 9 and 1 <= y <= 9:
            move_grid(x, y)
            await update.message.reply_text(f"🖱️ Moved to grid ({x},{y})")
        else:
            await update.message.reply_text("❌ Use m11–m99 (1–9 only)")

# c<x>,<y> → click using 101×101 grid (0–100)
    elif text.startswith("c") and "," in text:
        try:
            coords = text[1:].split(",", 1)
            x = int(coords[0])
            y = int(coords[1])

            if not (0 <= x <= 100 and 0 <= y <= 100):
                raise ValueError

            point = grid101_point(x, y)
            click_point(point)

            await update.message.reply_text(f"🖱️ Clicked at ({x},{y})")

        except Exception:
            await update.message.reply_text(
                "❌ Use format: c<x>,<y> where x,y ∈ 0–100\nExample: c50,50"
            )


# ──────────────── CHROME TAB COMMANDS (VIM STYLE) ────────────────
# ct<n> for right tab move/ sct<n> for left tab move
    elif text.startswith("ct") and len(text) == 3 and text[2].isdigit():
        count = int(text[2])

        if 1 <= count <= 9:
            script = f'''
            tell application "System Events"
                repeat {count} times
                    key code 48 using {{control down}}
                    delay 0.05
                end repeat
            end tell
            '''
            subprocess.run(["osascript", "-e", script])
            await update.message.reply_text(f"➡️ Ctrl+Tab pressed {count} time(s)")

    elif text.startswith("sct") and len(text) == 4 and text[3].isdigit():
        count = int(text[3])

        if 1 <= count <= 9:
            script = f'''
            tell application "System Events"
                repeat {count} times
                    key code 48 using {{control down, shift down}}
                    delay 0.05
                end repeat
            end tell
            '''
            subprocess.run(["osascript", "-e", script])
            await update.message.reply_text(f"⬅️ Ctrl+Shift+Tab pressed {count} time(s)")

# ──────────────── VOLUME CONTROL (VIM STYLE) ────────────────

# Volume mute
    elif text == "vm":
        subprocess.run([
            "osascript",
            "-e", 'set volume with output muted'
        ])
        await update.message.reply_text("🔇 Volume muted")

#v<n> volume n0%  
    elif text.startswith("v") and len(text) == 2 and text[1].isdigit():
        level = int(text[1])

        if level == 0:
            volume = 100
        elif 1 <= level <= 9:
            volume = level * 10
        else:
            await update.message.reply_text("❌ Use v0–v9 only")
            return

        subprocess.run([
            "osascript",
            "-e", f'set volume output volume {volume}'
        ])

        await update.message.reply_text(f"🔊 Volume set to {volume}%")

# ──────────────── TAB KEY ────────────────
# Press Tab key
    elif text.startswith("t") and len(text) == 2 and text[1].isdigit():
        count = int(text[1])

        if 1 <= count <= 9:
            script = f'''
            tell application "System Events"
                repeat {count} times
                    key code {TAB_KEYCODE}
                    delay 0.05
                end repeat
            end tell
            '''
            subprocess.run(["osascript", "-e", script])
            await update.message.reply_text(f"↹ Tab pressed {count} time(s)")

    elif text.startswith("st") and len(text) == 3 and text[2].isdigit():
        count = int(text[2])

        if 1 <= count <= 9:
            script = f'''
            tell application "System Events"
                repeat {count} times
                    key code 48 using {{shift down}}
                    delay 0.05
                end repeat
            end tell
            '''
            subprocess.run(["osascript", "-e", script])
            await update.message.reply_text(f"↩️ Shift+Tab pressed {count} time(s)")

# ──────────────── CHROME ZOOM ────────────────
# Zoom IN (zi, zi<n>)
    elif text.startswith("zi"):
        num = text[2:]

        if num == "":
            count = 4          # zi → 4x zoom in
        elif num.isdigit() and 1 <= int(num) <= 9:
            count = int(num)
        else:
            await update.message.reply_text("❌ Use zi or zi1–zi9 only")
            return

        for _ in range(count):
            subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key code 24 using {command down}'
        ])

        await update.message.reply_text(f"🔍 Zoomed IN ×{count}")

# Zoom OUT (zo, zo<n>)
    elif text.startswith("zo"):
        num = text[2:]

        if num == "":
            count = 4          # zo → 4x zoom out
        elif num.isdigit() and 1 <= int(num) <= 9:
            count = int(num)
        else:
            await update.message.reply_text("❌ Use zo or zo1–zo9 only")
            return

        for _ in range(count):
            subprocess.run([
            "osascript",
            "-e", 'tell application "System Events" to key code 27 using {command down}'
        ])

        await update.message.reply_text(f"🔎 Zoomed OUT ×{count}")

# ──────────────── SPACE/BACKSPACE/ENTER VIP COMMANDS ────────────────

# b<n> (Backspace key)
    elif text.startswith("b"):
        num = text[1:]

        if num == "":
            count = 1
        elif num.isdigit() and 1 <= int(num) <= 9:
            count = int(num)
        else:
            await update.message.reply_text("❌ Use b or b1–b9 only")
            return

        for _ in range(count):
            subprocess.run([
                "osascript",
                "-e", 'tell application "System Events" to key code 51'
            ])

        await update.message.reply_text(f"⌫ Backspace ×{count}")    

 # m<n> (Space key)
    elif text.startswith("m"):
        num = text[1:]

        if num == "":
            count = 1
        elif num.isdigit() and 1 <= int(num) <= 9:
            count = int(num)
        else:
            await update.message.reply_text("❌ Use m or m1–m9 only")
            return

        for _ in range(count):
            subprocess.run([
                "osascript",
                "-e", 'tell application "System Events" to key code 49'
            ])

        await update.message.reply_text(f"␣ Space pressed ×{count}")

# p<n> (Enter key)
    elif text.startswith("p"):
        num = text[1:]

        if num == "":
            count = 1
        elif num.isdigit() and 1 <= int(num) <= 9:
            count = int(num)
        else:
            await update.message.reply_text("❌ Use p or p1–p9 only")
            return

        for _ in range(count):
            subprocess.run([
                "osascript",
                "-e", 'tell application "System Events" to key code 36'
            ])

        await update.message.reply_text(f"⏎ Enter pressed ×{count}")








# ──────────────── BUG DETECTOR ────────────────
    else:
        await update.message.reply_text("❓ Unknown command")

# ──────────────── BOT SETUP ────────────────

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))


app.run_polling()
