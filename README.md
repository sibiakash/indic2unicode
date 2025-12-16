# indic2unicode : Indic Font OCR Fixer

A Python utility to fix "gibberish" OCR output from legacy Indian government documents.

It converts legacy font encodings (primarily **Kruti Dev** and **Divyae**) into standard **Unicode Hindi**. This is essential for parsing digitized Indian Parliamentary debates, gazettes, and legal archives from the pre-Unicode era.

---

## The Problem

When you OCR older Indian documents, the output often looks like this:

```

¤ÉÉiÉ +ÉÉè® BÉDªÉÉ cÉä

```

This happens because OCR engines read the **visual shape** of legacy font characters but output their **ASCII mappings** instead of Unicode.

---

## The Solution

This tool maps those ASCII characters back to their correct **Devanagari Unicode** equivalents.

**Output:**

```

बेटी को रखा है

````

---

## Features

- **Accurate Mapping**  
  Handles complex conjuncts such as `tra`, `ksha`, and other special characters.

- **Matra Reordering**  
  Automatically fixes the position of the **'i' matra (choti-ee)**, which appears before the consonant in legacy fonts but logically follows it in Unicode.

- **Corpus Expansion Helper**  
  Includes a debug mode that identifies **missing characters** (glyphs not present in the mapping).  
  This makes it easy to extend support for new or obscure font variations.

---

## Usage

```python
from converter import kruti_dev_to_unicode

legacy_text = "¤ÉÉiÉ +ÉÉè® BÉDªÉÉ cÉä"
clean_text = kruti_dev_to_unicode(legacy_text)

print(clean_text)
# Output: बेटी को रखा है
```

---

## Contributing

Legacy Indian fonts have **hundreds of regional and vendor-specific variations**.
If you encounter characters that don’t convert correctly, you can help expand the corpus.

### How to Contribute

1. Run the script with your problematic text.
2. Check the **debug output** in the terminal — it will list missing characters and their hex codes.
3. Identify the correct Hindi Unicode equivalent.
4. Add the mapping to the dictionary in `converter.py`.
5. Submit a **Pull Request**.

Contributions that improve coverage for government archives, parliamentary debates, and gazette documents are especially welcome.

