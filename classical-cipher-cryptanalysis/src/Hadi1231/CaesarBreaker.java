package Hadi1231;

public class CaesarBreaker {
	public static String decrypt(String text, int shift) {
	    StringBuilder result = new StringBuilder();

	    for (char c : text.toCharArray()) {
	        if (Character.isLetter(c)) {
	            char base = Character.isUpperCase(c) ? 'A' : 'a';
	            char decrypted = (char) ((c - base - shift + 26) % 26 + base);
	            result.append(decrypted);
	        } else {
	            result.append(c);
	        }
	    }
	    return result.toString();
	}
	public static int scoreText(String text) {
	    String[] commonWords = {"THE", "AND", "IS", "IN", "TO", "OF"};
	    int score = 0;

	    String upperText = text.toUpperCase();

	    for (String word : commonWords) {
	        if (upperText.contains(word)) {
	            score += 10;
	        }
	    }

	    return score;
	}
	public static void breakCipher(String cipherText) {
	    int bestScore = -1;
	    String bestDecryption = "";
	    int bestKey = 0;

	    for (int shift = 1; shift < 26; shift++) {
	        String decrypted = decrypt(cipherText, shift);
	        int score = scoreText(decrypted);

	        if (score > bestScore) {
	            bestScore = score;
	            bestDecryption = decrypted;
	            bestKey = shift;
	        }
	    }

	    System.out.println("Detected Cipher: Caesar");
	    System.out.println("Best Key: " + bestKey);
	    System.out.println("Decrypted Text: " + bestDecryption);
	    System.out.println("Confidence Score: " + bestScore);
	}

}
