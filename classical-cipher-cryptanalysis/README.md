# Automated Cryptanalysis System for Classical Ciphers

Computer Security course project (CMPS455), written in Java.

The program takes a piece of ciphertext and tries to recover the original
message without knowing the key. It first checks whether the text looks like
a Caesar cipher. If it does, it tries all 25 shifts and picks the best one.
If not, it attempts a substitution attack and a transposition attack and shows
the best guess for each. At the end it prints the letter frequencies of the text.

## How it works

- **Caesar:** brute force over every shift, scoring each result by how many
  common English words (THE, AND, IS, ...) appear in it.
- **Substitution:** frequency analysis. The most common letters in the
  ciphertext are mapped to the most common letters in English (E, T, A, O, ...).
- **Transposition:** tries column keys from 2 to 6 and keeps the result with
  the best word score.

## Files

- `main.java` – entry point, reads the ciphertext and runs the attacks
- `CipherDetector.java` – guesses whether the text is a Caesar cipher
- `CaesarBreaker.java` – Caesar decryption, brute force and word scoring
- `SubstitutionBreaker.java` – frequency-based substitution attack
- `TranspositionBreaker.java` – columnar transposition attack
- `FrequencyAnalyzer.java` – counts and prints letter frequencies

## How to run

```
javac -d out src/Hadi1231/*.java
java -cp out Hadi1231.main
```

Then paste a ciphertext, for example: `WKH TXLFN EURZQ IRA`
