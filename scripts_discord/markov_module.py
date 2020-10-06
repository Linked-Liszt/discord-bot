import discord_module as dm
import markovify
import discord
import os
import json

DEFAULT_N = 3
DEFAULT_NUM_SENTENCES = 5

class Markov(dm.DiscordModule):
    def __init__(self, models_dir: str):
        self.models_dir = models_dir
        self.module_abbrev = 'markov'
        self._find_models()
        self.info = ("These models are word tokenized, n-gram markov models.\n"
            + "For more info see: <https://en.wikipedia.org/wiki/Language_model#n-gram>\n"
            + "In non-math speak, the model looks at the [n] previous words and attempts "
            + "to guess what the next word is. Rinse and repeat to create sentences and paragraphs.")

        self.commands = {
            "!sim [name]": "Simulate a goon with a standard tri-gram model",
            "!sim#[n] [name]": "Simulate a goon with a [n]-gram model",
            "!list": "List avaliable models and n",
            "!info:": "Info about n-gram markov models"
        }

    async def handle_message(self, message: discord.Message):
        if message.content.lower().startswith("!list"):
            await message.channel.send(self._list_models())

        elif (message.content.lower().startswith("!sim ")
            or message.content.lower().startswith("!sim#")):
            await message.channel.send(self._serve_model(message.content.lower()))

    def _find_models(self) -> None:
        self.models = []
        self.max_n = 0
        self.min_n = 1000
        for fp in os.listdir(self.models_dir):
            if fp.endswith('.json'):
                name = fp.split('_')[0]
                # Remove .json
                n_value = int(fp.split('_')[1][:-5])

                if name not in self.models:
                    self.models.append(name)

                self.max_n = max(n_value, self.max_n)
                self.min_n = min(n_value, self.min_n)

    def _list_models(self) -> str:
        return ', '.join(self.models) + "\n2 <= n <= 10"

    def _serve_model(self, command: str) -> str:
        try:
            model_name, n = self._parse_command(command)
        except ValueError as e:
            return str(e)

        return self._generate_text(model_name, n)

    def _generate_text(self, model_name: str, n: int) -> str:
        model_fp = os.path.join(self.models_dir, f'{model_name}_{n}.json')
        with open(model_fp, 'r') as model_f:
            model_json = model_f.read()
        model = markovify.Text.from_json(model_json)
        output = ""
        for _ in range(DEFAULT_NUM_SENTENCES):
            sentence = model.make_sentence(tries=100, test_output=False)
            if sentence is not None:
                output += sentence + ' '
        return output


    def _parse_command(self, command: str) -> (str, int):
        split_command = command.split(' ')
        if len(split_command) < 1:
            raise ValueError('Error: !sim missing model command.')

        if split_command[0].startswith('!sim#'):
            try:
                n = int(split_command[0].split('#')[1].strip())
            except ValueError:
                raise ValueError('Error: Malformed n value for !sim#')

            print(self.min_n)

            if n > self.max_n:
                raise ValueError(f'Error: n > max n. Max n is {self.max_n}')
            if n < self.min_n:
                raise ValueError(f'Error: n < min n. Min n is {self.min_n}')

        else:
            n = DEFAULT_N

        model = split_command[1].strip()
        if model not in self.models:
            raise ValueError('Error: Unknown Model. See !models')

        return model, n