"""Provides AI-assisted bash magic commands by combining bashnb and aimagic functionality"""

from aimagic.core import AiMagic
from .core import BashMagic

class BashAiMagic(BashMagic):
    def __init__(self, model='claude-2'):
        """Initialize bash session with AI capabilities"""
        super().__init__()
        self.ai = AiMagic(model=model)

    def _build_context(self, command, output):
        return {
            'cell_type': 'code',
            'source': command,
            'outputs': [{
                'output_type': 'stream',
                'text': output
            }]
        }

    def bash_with_ai(self, line, cell=None):
        """Execute bash command with AI assistance"""
        try:
            result = self.bash(line, cell)
            if line.startswith('explain'):
                context = self._build_context(cell, result)
                return self.ai.explain([context])
            return result
        except Exception as e:
            return f"Error: {str(e)}"
