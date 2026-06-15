# Telegram Mac Controller

A Telegram-based remote administration and automation system for macOS.

## Features

- Remote mouse control
- Keyboard automation
- Shell command execution
- Application launching
- WhatsApp automation
- Clipboard interaction
- Grid-based cursor navigation

## Technologies

- Python
- Telegram Bot API
- AppleScript
- Quartz
- macOS Accessibility APIs

# TBot Controller

> Turn Telegram into a command center for your Mac.

TBot Controller is a Telegram-powered remote administration and automation system for macOS. It allows a user to control a Mac from anywhere using simple Telegram commands, eliminating the need for a traditional remote desktop interface.

The project began as a personal experiment in workstation automation and evolved into a lightweight command-driven system capable of controlling applications, executing shell commands, automating workflows, and interacting directly with macOS.

---

## Features

### Remote System Control
- Execute terminal commands
- Launch and manage applications
- Trigger custom automation workflows
- Run AppleScript actions

### Keyboard Automation
- Simulate key presses
- Execute keyboard shortcuts
- Automate repetitive tasks

### Mouse Automation
- Move cursor remotely
- Perform clicks
- Grid-based navigation system
- Precision coordinate control

### Communication Automation
- Telegram command interface
- WhatsApp automation workflows
- Text and clipboard interaction

---

## Architecture

```text
Phone
   │
   ▼
Telegram Bot
   │
   ▼
Python Automation Engine
   │
   ├── Shell Commands
   ├── AppleScript
   ├── Keyboard Events
   ├── Mouse Events
   ├── App Launching
   └── Custom Workflows
   │
   ▼
macOS
```

---

## Technologies

- Python
- Telegram Bot API
- AppleScript
- Quartz Event Services
- macOS Accessibility APIs

---

## Example Commands

```text
c          → copy
v          → paste
u5         → scroll up
d5         → scroll down
mj3        → move cursor
c50,70     → click grid coordinate
t ls       → execute terminal command
```

---

## Motivation

Most remote-control solutions focus on graphical access. This project explores a different paradigm: controlling an entire workstation through concise text commands.

Instead of streaming a desktop, TBot treats Telegram as a command interface and macOS as an automation target.

---

## Disclaimer

This software was created for personal workstation automation and remote administration of systems owned or authorized by the user.

---

## Future Work

- Screenshot capture
- File transfer
- Voice commands
- Scheduled workflows
- Multi-device support
- Plugin system

---

## Author

Navneet Priyadarshi

Built out of curiosity, automation experiments, and the desire to control a computer from anywhere through a messaging interface.
# TBot Controller

> Control your Mac from anywhere using Telegram as a lightweight command interface.

TBot Controller is a Telegram-powered remote administration and automation system for macOS. It transforms a Telegram chat into a command console capable of controlling applications, executing shell commands, automating workflows, simulating keyboard and mouse input, and interacting directly with the operating system.

Unlike traditional remote desktop software, TBot focuses on command-driven interaction. Instead of streaming a desktop environment, it allows the user to perform actions through concise Telegram commands.

---

## Features

### Remote System Control
- Execute shell commands
- Launch and manage applications
- Trigger custom automation workflows
- Run AppleScript actions

### Keyboard Automation
- Simulate key presses
- Execute keyboard shortcuts
- Automate repetitive actions

### Mouse Automation
- Move the cursor remotely
- Perform mouse clicks
- Grid-based navigation system
- Precision coordinate control

### Communication Automation
- Telegram command interface
- WhatsApp automation workflows
- Clipboard and text interaction

---

## Architecture

```text
Phone
   │
   ▼
Telegram Bot
   │
   ▼
Python Automation Engine
   │
   ├── Shell Commands
   ├── AppleScript
   ├── Keyboard Events
   ├── Mouse Events
   ├── Application Control
   └── Custom Workflows
   │
   ▼
macOS
```

---

## Technologies

- Python
- Telegram Bot API
- AppleScript
- Quartz Event Services
- macOS Accessibility APIs

---

## Example Commands

```text
c          → copy selected content
v          → paste clipboard content
u5         → scroll upward
d5         → scroll downward
mj3        → move cursor
c50,70     → click at grid coordinate
t ls       → execute shell command
```

---

## Installation

```bash
git clone https://github.com/sirluoyi/tbot-controller.git
cd tbot-controller
pip install -r requirements.txt
```

Configure your Telegram bot token through an environment variable before running the application.

---

## Motivation

This project started as a personal experiment in workstation automation. The goal was to create a lightweight system capable of controlling a Mac remotely through a messaging platform without relying on a graphical remote desktop solution.

The result is a command-driven automation layer that uses Telegram as a communication channel and macOS as the execution environment.

---

## Future Improvements

- File transfer support
- Voice command integration
- Workflow scheduling
- Multi-device support
- Plugin architecture

---

## Disclaimer

This software was developed for personal workstation automation and remote administration of systems owned by, or explicitly authorized for use by, the operator.

---

## Author

Navneet Priyadarshi

Built from curiosity, automation experiments, and the desire to control a computer from anywhere through a simple messaging interface.