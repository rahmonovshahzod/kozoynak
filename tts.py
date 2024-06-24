import re
import torch
from transformers import AutoTokenizer, VitsModel
from pydub import AudioSegment
import numpy as np
from playsound import playsound

LATIN_TO_CYRILLIC = {
    'a': 'а', 'A': 'А', 'b': 'б', 'B': 'Б', 'd': 'д', 'D': 'Д', 'e': 'е', 'E': 'Е',
    'f': 'ф', 'F': 'Ф', 'g': 'г', 'G': 'Г', 'h': 'х', 'H': 'Х', 'i': 'и', 'I': 'И',
    'j': 'ж', 'J': 'Ж', 'k': 'к', 'K': 'К', 'l': 'л', 'L': 'Л', 'm': 'м', 'M': 'М',
    'n': 'н', 'N': 'Н', 'o': 'о', 'O': 'О', 'p': 'п', 'P': 'П', 'q': 'қ', 'Q': 'Қ',
    'r': 'р', 'R': 'Р', 's': 'с', 'S': 'С', 't': 'т', 'T': 'Т', 'u': 'у', 'U': 'У',
    'v': 'в', 'V': 'В', 'x': 'кс', 'X': 'Кс', 'y': 'й', 'Y': 'Й', 'z': 'з', 'Z': 'З'
}

LATIN_VOWELS = (
    'a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U', 'o‘', 'O‘'
)

CYRILLIC_TO_LATIN = {
    'а': 'a', 'А': 'A', 'б': 'b', 'Б': 'B', 'в': 'v', 'В': 'V', 'г': 'g', 'Г': 'G',
    'д': 'd', 'Д': 'D', 'е': 'e', 'Е': 'E', 'ё': 'yo', 'Ё': 'Yo', 'ж': 'j', 'Ж': 'J',
    'з': 'z', 'З': 'Z', 'и': 'i', 'И': 'I', 'й': 'y', 'Й': 'Y', 'к': 'k', 'К': 'K',
    'л': 'l', 'Л': 'L', 'м': 'm', 'М': 'M', 'н': 'n', 'Н': 'N', 'о': 'o', 'О': 'O',
    'п': 'p', 'П': 'P', 'р': 'r', 'Р': 'R', 'с': 's', 'С': 'S', 'т': 't', 'Т': 'T',
    'у': 'u', 'У': 'U', 'ф': 'f', 'Ф': 'F', 'х': 'h', 'Х': 'H', 'ц': 'ts', 'Ц': 'Ts',
    'ч': 'ch', 'Ч': 'Ch', 'ш': 'sh', 'Ш': 'Sh', 'щ': 'shch', 'Щ': 'Shch', 'ы': 'y',
    'Ы': 'Y', 'ь': '', 'Ь': '', 'э': 'e', 'Э': 'E', 'ю': 'yu', 'Ю': 'Yu', 'я': 'ya',
    'Я': 'Ya'
}

CYRILLIC_VOWELS = (
    'а', 'А', 'е', 'Е', 'ё', 'Ё', 'и', 'И', 'о', 'О', 'у', 'У', 'э', 'Э', 'ю', 'Ю', 'я', 'Я'
)


def to_cyrillic(text):
    compounds_first = {
        'ch': 'ч', 'Ch': 'Ч', 'CH': 'Ч',
        'sh': 'ш', 'Sh': 'Ш', 'SH': 'Ш',
        'yo‘': 'йў', 'Yo‘': 'Йў', 'YO‘': 'ЙЎ',
    }
    compounds_second = {
        'yo': 'ё', 'Yo': 'Ё', 'YO': 'Ё',
        'yu': 'ю', 'Yu': 'Ю', 'YU': 'Ю',
        'ya': 'я', 'Ya': 'Я', 'YA': 'Я',
        'ye': 'е', 'Ye': 'Е', 'YE': 'Е',
        'o‘': 'ў', 'O‘': 'Ў', 'g‘': 'ғ', 'G‘': 'Ғ',
    }
    beginning_rules = {
        'ye': 'е', 'Ye': 'Е', 'YE': 'Е',
        'e': 'э', 'E': 'Э',
    }
    after_vowel_rules = {
        'ye': 'е', 'Ye': 'Е', 'YE': 'Е',
        'e': 'э', 'E': 'Э',
    }

    text = text.replace('ʻ', '‘')

    text = re.sub(
        r'(%s)' % '|'.join(compounds_first.keys()),
        lambda x: compounds_first[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)' % '|'.join(compounds_second.keys()),
        lambda x: compounds_second[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'\b(%s)' % '|'.join(beginning_rules.keys()),
        lambda x: beginning_rules[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)(%s)' % ('|'.join(LATIN_VOWELS),
                       '|'.join(after_vowel_rules.keys())),
        lambda x: '%s%s' % (x.group(1), after_vowel_rules[x.group(2)]),
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)' % '|'.join(LATIN_TO_CYRILLIC.keys()),
        lambda x: LATIN_TO_CYRILLIC[x.group(1)],
        text,
        flags=re.U
    )

    return text


def to_latin(text):
    beginning_rules = {
        'ц': 's', 'Ц': 'S',
        'е': 'ye', 'Е': 'Ye'
    }
    after_vowel_rules = {
        'ц': 'ts', 'Ц': 'Ts',
        'е': 'ye', 'Е': 'Ye'
    }

    text = re.sub(
        r'(сент|окт)([яЯ])(бр)',
        lambda x: '%s%s%s' % (x.group(1),
                              'a' if x.group(2) == 'я' else 'A', x.group(3)),
        text,
        flags=re.IGNORECASE | re.U
    )

    text = re.sub(
        r'\b(%s)' % '|'.join(beginning_rules.keys()),
        lambda x: beginning_rules[x.group(1)],
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)(%s)' % ('|'.join(CYRILLIC_VOWELS),
                       '|'.join(after_vowel_rules.keys())),
        lambda x: '%s%s' % (x.group(1), after_vowel_rules[x.group(2)]),
        text,
        flags=re.U
    )

    text = re.sub(
        r'(%s)' % '|'.join(CYRILLIC_TO_LATIN.keys()),
        lambda x: CYRILLIC_TO_LATIN[x.group(1)],
        text,
        flags=re.U
    )

    return text


def transliterate(text, to_variant):
    if to_variant == 'cyrillic':
        text = to_cyrillic(text)
    elif to_variant == 'latin':
        text = to_latin(text)
    return text


def tts_full(text):
    text = transliterate(text, 'cyrillic')
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-uzb-script_cyrillic")
    model = VitsModel.from_pretrained("facebook/mms-tts-uzb-script_cyrillic")
    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        output = model(**inputs).waveform

    data_numpy = output.squeeze().detach().cpu().numpy()
    if data_numpy.dtype != np.int16:
        data_numpy = (data_numpy * 32767).astype(np.int16)

    audio_data = data_numpy.tobytes()
    audio_segment = AudioSegment(
        data=audio_data,
        frame_rate=model.config.sampling_rate,
        sample_width=2,
        channels=1
    )
    audio_segment.export("result_211.wav", format="mp3")

tts_full("Assalomu alaykum Nodir!")
playsound("result_211.wav")