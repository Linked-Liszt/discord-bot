import discord
import discord_module as dm
import textstat
import math
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

FLESCH = {
    8: 'easy',
    7: 'fairly easy',
    6: 'standard',
    5: 'fairly difficult',
    4:'difficult',
    3:'difficult'
}

class Rate(dm.DiscordModule):
    def __init__(self):
        self.info = ("This module uses various stastical tests and tools to "
                     "rate and analyze messages sent in chat.")
        self.abbrev = 'rate'
        self.commands = {
            "!rate": "Rate a message's sentiment and complexity."
        }
        self.vader = SentimentIntensityAnalyzer()

    async def handle_message(self, message: discord.Message):
        if message.content.lower().startswith('!rate'):
            rating = self._rate_message(await self._get_previous_content(message))
            await message.channel.send(rating)

    async def _get_previous_content(self, message: discord.message) -> str:
        messages = await message.channel.history(before=message, limit=1).flatten()
        return messages[0].content

    def _rate_message(self, text):
        return (f"--Sentiment Analysis--{self._get_sentament(text)}\n\n"
                f"--Complexity--{self._get_complexity(text)}")

    def _get_sentament(self, text: str) -> str:
        rating = self.vader.polarity_scores(text)
        return (f"\n{rating['neg']*100:.1f} % Negative | "
                f"{rating['neu']*100:.1f} % Neutral | "
                f"{rating['pos']*100:.1f} % Positive")

    def _get_complexity(self, text: str) -> str:
        warning = ""
        if textstat.lexicon_count(text) < 50:
            warning = " (Warning: <50 words. YMMV)"

        return (f" {warning}\n"
                f"{self._dale_chall_test(text)} | {self._linsear(text)}\n"
                f"{self._flesch(text)} | Ensemble: {textstat.text_standard(text)}")

    def _flesch(self, text: str) -> str:
        fle = textstat.flesch_reading_ease(text)
        fle_round = math.floor(fle / 10)
        if fle_round >= 9:
            descr = 'very easy'
        elif fle_round in FLESCH:
            descr = FLESCH[fle_round]
        else:
            descr = 'very confusing'
        return f"Flesch: {fle} ({descr})"

    def _linsear(self, text: str) -> str:
        return f"Linsear: {round(textstat.linsear_write_formula(text))} grade"

    def _dale_chall_test(self, text: str) -> str:
        dc = textstat.dale_chall_readability_score(text)
        if dc < 4.9:
            descr = "< 4th grade"
        elif dc < 9.0:
            grade = math.floor(dc) + (math.floor(dc) - 5)
            descr = f"{grade}-{grade + 1} grade"
        else:
            descr = "college level"
        return f"Dale-Chall: {dc} ({descr})"
