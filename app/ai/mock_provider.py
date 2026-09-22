from app.ai.provider import AIProvider


class MockProvider(AIProvider):

    def generate(self, prompt: str) -> str:
        return (
            '{"summary": "Generated engineering proposal", '
            '"requirements": [], '
            '"systems": [], '
            '"components": [], '
            '"connections": []}'
        )
