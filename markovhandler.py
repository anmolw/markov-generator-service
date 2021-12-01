from asyncio.locks import Lock
from typing import Union
import markovify
import asyncio


class InitializationError(Exception):
    """Error thrown when the model is not initialized"""

    pass


class MarkovHandler:
    """
    Manages the state of the internal markov model
    """

    def __init__(self):
        self._markov = None
        self._lock = Lock()

    async def add(self, text: str) -> None:
        """
        Add a list of strings to the markov model's corpus
        """
        async with self._lock:
            if self._markov is None:
                self._markov = await asyncio.get_event_loop().run_in_executor(
                    None, markovify.Text, text
                )
            else:
                new_model = await asyncio.get_event_loop().run_in_executor(
                    None, markovify.Text, text
                )
                self._markov = await asyncio.get_event_loop().run_in_executor(
                    None, markovify.utils.combine, (new_model, self._markov)
                )

    async def generate(self) -> Union[str, None]:
        """
        Generate sentences using the markov model
        """
        if self._markov is not None:
            return await asyncio.get_event_loop().run_in_executor(
                None, self._markov.make_sentence
            )
        else:
            raise InitializationError("Model not initialized")

    async def info(self) -> dict:
        """
        Returns some stats about the state of the markov model
        """

    async def reset(self):
        """
        Reset the internal markov model
        """
        self._markov = markovify.NewlineText()
