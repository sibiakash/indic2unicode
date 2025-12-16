import regex
import sys


def kruti_dev_to_unicode(text):
    """
    Converts Kruti Dev (and similar legacy Indic fonts) encoded text to standard Unicode Hindi.

    This function handles:
    1. Multi-character conjuncts (e.g., 'tra', 'ksha')
    2. Single character mappings
    3. Reordering of the 'i' matra (which appears before the consonant in legacy fonts)
    4. Detection of unconverted characters for corpus expansion
    """

    # CRITICAL: Multi-character sequences MUST be processed first
    # These need to be matched before their component parts
    multi_char_mapping = {
        # Nukta characters (appear with +)
        "[+k": "ख़", "[+": "ख़्", "x+": "ग़", "T+": "ज़्", "t+": "ज़",
        "M+": "ड़", "<+": "ढ़", "Q+": "फ़", ";+": "य़", "j+": "ऱ",
        "u+": "ऩ", "¶+": "फ़्", "d+": "क़",

        # Consonant + vowel combinations (MUST come before single chars)
        "[k": "ख", "Xk": "ग", "Dk": "क", "?k": "घ", "Pk": "च",
        "Tk": "ज", "Fk": "थ", "/k": "ध", "'k": "श", "\"k": "ष",
        "Hk": "भ", ".k": "ण",

        # Vowel combinations
        "vks": "ओ", "vkS": "औ", "vk": "आ", "bZ": "ई", ",s": "ऐ",

        # Complex conjuncts
        "{k": "क्ष", "=k": "त्र", "Ùk": "त्त",
        "nzZ": "र्द्र", ")Z": "र्द्ध",
        "Nî": "छ्य", "Vî": "ट्य", "Bî": "ठ्य", "Mî": "ड्य", "<î": "ढ्य",
        "Vª": "ट्र", "Mª": "ड्र", "<ªª": "ढ्र", "Nª": "छ्र",
        "xz": "ग्र", "ºz": "ह्र",
        "èQs": "द्ध",

        # Special sequences
        "pkS": "चौ", "=kk": "त्रा", "f=k": "त्रि",
    }

    # Single character mappings - Based on frequency analysis of Parlimentary docs
    single_char_mapping = {
        # TOP FREQUENCY CHARACTERS
        "É": "ा", "®": "र", "Ê": "ि", "à": "म", "º": "स",
        "ª": "य", "Ò": "ी", "ã": "े", "å": "न", "è": "ु",
        "¤": "ब", "´": "ृ", "Æ": "ं", "Ö": "ु", "¶": "फ्",
        "£": "भ", "Ç": "र्", "Ú": "ूं", "½": "ल", "­": "ष",
        "Ó": "ों", "â": "ू", "ó": "ृ", "Å": "ऊ", "§": "ू",
        "Ë": "ू", "Î": "ी", "Ã": "ई", "Ì": "ि", "ß": "्",
        "Í": "िं", "Ô": "ौ", "È": "इ", "°": "॰", "æ": "द्र",
        "ì": "ड्ड", "ô": "क्क", "é": "न्न", "ä": "क्त",

        # Basic consonants
        "d": "क", "D": "क्", "[": "ख्", "x": "ग", "X": "ग्",
        "Ä": "घ", "?": "घ्", "³": "ङ",
        "p": "च", "P": "च्", "N": "छ", "t": "ज", "T": "ज्",
        ">": "झ", "÷": "झ्", "¥": "ञ",
        "V": "ट", "B": "ठ", "M": "ड", "<": "ढ", ".": "ण्",
        "r": "त", "R": "त्", "F": "थ्", ")": "द्ध", "n": "द",
        "/": "ध्", "u": "न", "U": "न्",
        "i": "प", "I": "प्", "Q": "फ", "c": "ब", "C": "ब्",
        "H": "भ्", "e": "म", "E": "म्",
        ";": "य", "¸": "य्", "j": "र", "y": "ल", "Y": "ल्",
        "G": "ळ", "o": "व", "O": "व्",
        "'": "श्", "\"": "ष्", "l": "स", "L": "स्", "g": "ह",

        # Vowel signs
        "k": "ा", "s": "ी", "h": "ु", "w": "ू", "S": "े", "a": "ै",
        "¨": "ॅ", "‚": "ॉ",

        # Modifiers
        "^": "ँ", "~": "्", "Z": "़",

        # Conjuncts
        "{": "क्ष्", "=": "त्र्", "«": "त्र्",
        "K": "ज्ञ", "J": "श्र", "Ø": "क्र", "Ý": "फ्र", "ç": "प्र",
        "Á": "प्र", "í": "द्द", "|": "द्य", "}": "द्व",

        # Special
        "#": "रु", ":": "रू", "–": "दृ", "—": "कृ",

        # Independent vowels
        "v": "अ", "b": "इ", "m": "उ", ",": "ए", "_": "ऋ",

        # Numbers
        "0": "०", "1": "१", "2": "२", "3": "३", "4": "४",
        "5": "५", "6": "६", "7": "७", "8": "८", "9": "९",

        # Punctuation
        "ñ": "॰", "*": "।",
        "'": "'", "'": "'", """: "\"", """: "\"",
    }

    converted = text

    # Step 1: Apply multi-character mappings first (longest to shortest)
    for pattern in sorted(multi_char_mapping.keys(), key=len, reverse=True):
        converted = converted.replace(pattern, multi_char_mapping[pattern])

    # Step 2: Apply single character mappings
    for pattern in sorted(single_char_mapping.keys(), key=len, reverse=True):
        converted = converted.replace(pattern, single_char_mapping[pattern])

    # Step 3: Handle 'f' to 'ि' reordering (i-matra goes before consonant in Unicode)
    chars = list(converted)
    i = 0
    while i < len(chars):
        if chars[i] == 'f' and i + 1 < len(chars):
            char_to_move = chars[i + 1]
            chars[i] = char_to_move
            chars[i + 1] = 'ि'
            i += 1
        i += 1

    result = "".join(chars)

    # Debug: Check for remaining unconverted characters
    # Useful for expanding the corpus when parsing new government docs
    unconverted = regex.findall(r"[^\u0900-\u097F\u0020-\u007E\s\u0964-\u0965\u0A00-\u0A7F]", result)
    if unconverted:
        unique = set(unconverted)
        print(f"\n[DEBUG] ⚠️  Unconverted characters detected: {len(unique)} type(s)", file=sys.stderr)
        for char in sorted(unique)[:10]:
            print(f"  '{char}' (U+{ord(char):04X})", file=sys.stderr)

    return result


if __name__ == "__main__":
    # Test string: "Beti ko rakha hai"
    test_text = """¤ÉÉiÉ +ÉÉè® BÉDªÉÉ cÉä """

    print("=" * 70)
    print("INDIC FONT LEGACY CONVERTER")
    print("=" * 70)
    print(f"\nOriginal (Kruti Dev):\n{test_text}\n")

    result = kruti_dev_to_unicode(test_text)

    print(f"\n{'=' * 70}")
    print("CONVERTED (Unicode Hindi):")
    print("=" * 70)
    print(result)
    print("\n" + "=" * 70)