package Hadi1231;

public class FrequencyAnalyzer {
	public static int[] countLetters(String text) {
        int[] counts = new int[26];

        text = text.toUpperCase();

        for (char c : text.toCharArray()) {
            if (c >= 'A' && c <= 'Z') {
                counts[c - 'A']++;
            }
        }

        return counts;
    }

    public static void printFrequencies(String text) {
        int[] counts = countLetters(text);

        System.out.println("\nLetter Frequencies:");

        for (int i = 0; i < 26; i++) {
            char letter = (char) ('A' + i);
            System.out.println(letter + ": " + counts[i]);
        }
    }
    public static char getMostFrequentLetter(String text) {
        int[] counts = countLetters(text);

        int maxIndex = 0;

        for (int i = 1; i < 26; i++) {
            if (counts[i] > counts[maxIndex]) {
                maxIndex = i;
            }
        }

        return (char) ('A' + maxIndex);
    }

}
