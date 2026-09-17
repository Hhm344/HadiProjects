package Hadi1231;

public class TranspositionBreaker {
	public static String breakTransposition(String cipherText) {
        String bestResult = cipherText;
        int bestScore = -1;

        for (int key = 2; key <= 6; key++) { 
            String attempt = decrypt(cipherText, key);
            int score = CaesarBreaker.scoreText(attempt);

            System.out.println("Key " + key + ": " + attempt + " | Score: " + score);

            if (score > bestScore) {
                bestScore = score;
                bestResult = attempt;
            }
        }

        return bestResult;
    }

    public static String decrypt(String text, int key) {
        int numRows = (int) Math.ceil((double) text.length() / key);
        char[][] grid = new char[numRows][key];

        int index = 0;

        
        for (int col = 0; col < key; col++) {
            for (int row = 0; row < numRows; row++) {
                if (index < text.length()) {
                    grid[row][col] = text.charAt(index++);
                }
            }
        }

        StringBuilder result = new StringBuilder();
        for (int row = 0; row < numRows; row++) {
            for (int col = 0; col < key; col++) {
                if (grid[row][col] != '\0') {
                    result.append(grid[row][col]);
                }
            }
        }

        return result.toString();
    }

}
