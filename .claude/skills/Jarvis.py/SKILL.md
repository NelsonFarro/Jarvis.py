```markdown
# Jarvis.py Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill covers development patterns for Jarvis.py, a Python-based personal assistant or automation system. The codebase follows informal conventions with mixed import styles and camelCase file naming, suggesting a flexible, rapid-development approach typical of AI assistant or automation projects.

## Coding Conventions

### File Naming
- Use **camelCase** for file names
- Examples: `voiceRecognition.py`, `speechSynthesis.py`, `configManager.py`

### Import Style
- Mixed import patterns are acceptable
- Use standard library imports first, then third-party, then local imports
```python
import os
import sys
from datetime import datetime

import speech_recognition as sr
import pyttsx3

from configManager import Config
```

### Export Style
- Mixed export patterns based on functionality
- Use `__all__` for public modules when appropriate
```python
# For utility modules
__all__ = ['process_command', 'get_response']

# For main modules, direct function definitions
def main_handler():
    pass
```

### Commit Style
- Freeform commit messages (average 35 characters)
- Focus on brevity and clarity
- Examples: "Add voice recognition", "Fix audio bug", "Update config handling"

## Workflows

### Adding New Voice Commands
**Trigger:** When implementing new Jarvis functionality
**Command:** `/add-voice-command`

1. Define command pattern in command parser
2. Create handler function with descriptive camelCase name
3. Add any required imports at module level
4. Test command recognition and response
5. Update help/documentation if needed

### Audio Processing Setup
**Trigger:** When working with speech recognition or synthesis
**Command:** `/setup-audio`

1. Import required audio libraries (speech_recognition, pyttsx3)
2. Initialize audio engines in setup function
3. Add error handling for audio device issues
4. Test microphone input and speaker output
5. Configure audio settings in config file

### Configuration Management
**Trigger:** When adding new settings or preferences
**Command:** `/manage-config`

1. Define configuration keys in configManager module
2. Set default values for new settings
3. Add validation for configuration values
4. Update configuration loading/saving methods
5. Test configuration persistence

## Testing Patterns

### Test File Organization
- Test files follow `*.test.*` pattern
- Examples: `voiceRecognition.test.py`, `commands.test.py`

### Testing Approach
```python
# Basic test structure (framework unknown)
def test_voice_recognition():
    # Setup test audio input
    # Process command
    # Assert expected response
    pass

def test_command_parsing():
    # Test various command formats
    # Verify correct handler selection
    pass
```

## Commands

| Command | Purpose |
|---------|---------|
| `/add-voice-command` | Add new voice command functionality |
| `/setup-audio` | Configure speech recognition and synthesis |
| `/manage-config` | Handle configuration and settings |
| `/debug-audio` | Troubleshoot audio input/output issues |
| `/test-commands` | Test command recognition and responses |
| `/update-responses` | Modify Jarvis response patterns |
```