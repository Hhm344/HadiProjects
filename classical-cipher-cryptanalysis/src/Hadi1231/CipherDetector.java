package Hadi1231;

public class CipherDetector {
	public static String detectCipher(String cipherText) {
        int bestScore = -1;

        for (int shift = 1; shift < 26; shift++) {
            String decrypted = CaesarBreaker.decrypt(cipherText, shift);
            int score = CaesarBreaker.scoreText(decrypted);

            if (score > bestScore) {
                bestScore = score;
            }
        }

       
        if (bestScore >= 10) {
            return "Caesar";
        } else {
            return "Unknown";
        }
	}
}
