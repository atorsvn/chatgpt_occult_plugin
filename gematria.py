import sqlite3

class GematriaCalculator:

    gematria_values = {
        'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5,
        'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
        'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40,
        'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80,
        'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200,
        'ש': 300, 'ת': 400,
        'α': 1, 'β': 2, 'γ': 3, 'δ': 4, 'ε': 5,
        'ζ': 7, 'η': 8, 'θ': 9, 'ι': 10, 'κ': 20,
        'λ': 30, 'μ': 40, 'ν': 50, 'ξ': 60, 'ο': 70,
        'π': 80, 'ρ': 100, 'σ': 200, 'τ': 300, 'υ': 400,
        'φ': 500, 'χ': 600, 'ψ': 700, 'ω': 800,
        'a': 1, 'l': 2, 'w': 3, 'h': 4, 's': 5, 'd': 6,
        'o': 7, 'z': 8, 'k': 9, 'v': 10, 'g': 11, 'r': 12,
        'c': 13, 'n': 14, 'y': 15, 'j': 16, 'u': 17, 'f': 18,
        'q': 19, 'b': 20, 'm': 21, 'x': 22, 'i': 23, 't': 24,
        'e': 25, 'p': 26
    }

    @staticmethod
    def get_words_by_value(value):
        conn = sqlite3.connect('data/gematria.db')
        cur = conn.cursor()
        cur.execute("SELECT Word, Meaning FROM Gematria WHERE Value=?", (value,))

        rows = cur.fetchall()
        conn.close()

        results = []
        for row in rows:
            results.append({"Word": row[0], "Meaning": row[1]})

        return results

    @classmethod
    def calculate_gematria(cls, text):
        total = 0
        for char in text:
            total += cls.gematria_values.get(char, 0)

        words_by_value = cls.get_words_by_value(total)
        return {"gematria_value": total, "words": words_by_value}
