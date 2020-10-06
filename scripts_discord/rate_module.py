import discord
import discord_module as dm
import textstat
import math
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Rate(dm.DiscordModule):
    def __init__(self):
        self.info = ("This module uses various stastical tests and tools to "
                     "rate and analyze messages sent in chat.")
        self.module_abbrev = 'rate'
        self.commands = {
            "!rate": "Rate a message's sentiment and complexity."
        }
        self.vader = SentimentIntensityAnalyzer()

    async def handle_message(self, message: discord.Message):
        if message.content.lower().startswith('!rate'):
            rating = self._rate_message(self._get_previous_content(message))

    def _get_previous_content(self, message: discord.message) -> str:
        return message.channel.history(before=message, limit=1)[0].content

    def _rate_message(self, text):
        return (f"--Sentiment Analysis--\n{self._get_sentament(text)}\n\n"
                f"--Complexity--\n{self._get_complexity(text)}")

    def _get_sentament(self, text: str) -> str:
        rating = self.vader.polarity_scores(text)
        return (f"Sentiment Analysis\n{rating['neg']*100:.1f} % Negative |"
                + f"{rating['neu']*100:.1f} % Neutral |"
                + f"{rating['pos']*100:.1f} % Positive")

    def _get_complexity(self, text: str) -> str:
        warning = ""
        if textstat.lexicon_count(text) < 50:
            warning = " (Warning: Less than 50 words. YMMV)

        return (f"Complexity Analysis: {warning}\n"
                f"{self._dale_chall_test(text)} | {self._linsear(text)}\n")
                f"{self._flesch(text)} | Ensemble: {textstat.text_standard(text)} grade")

    def _flesch(self, text: str) -> str:
        fle = textstat.flesch_reading_ease(text)
        fle_round = math.floor(fle / 10)
        if fle_round >= 9:
            descr = 'very easy'
        elif fle_round == 8:
            descr = 'easy'
        elif fle_round == 7:
            descr = 'fairly easy'
        elif fle_round == 6:
            descr = 'standard'
        elif fle_round == 5:
            descr = 'fairly difficult'
        elif fle_round == 3 or fle_round == 4:
            descr = 'difficult'
        else:
            descr = 'confusing'
        return f"Flesch: {fle} ({descr})"

    def _linsear(text: str) -> str:
        return f"Linsear: {round(textstat.linesar_write_formula(text))} grade"

    def _dale_chall_test(self,, text: str) -> str:
        dc = textstat.dale_chall_readability_score(text)
        if dc < 4.9:
            descr = "< 4th grade"
        elif dc < 9.0:
            grade = math.floor(dc) + (math.floor(dc) - 5)
            descr = f"{grade}-{grade + 1} grade"
        else:
            descr = "college level"
        return f"Dale-Chall: {dc} ({dsecr})"
