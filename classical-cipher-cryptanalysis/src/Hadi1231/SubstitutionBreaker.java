package Hadi1231;
import java.util.Arrays;
import java.util.Comparator;
public class SubstitutionBreaker {
	private static final String ENGLISH_FREQ = "ETAOINSHRDLCUMWFGYPBVKJXQZ";

    public static String breakSubstitution(String cipherText) {
        cipherText = cipherText.toUpperCase();

        int[] counts = FrequencyAnalyzer.countLetters(cipherText);

        
        Character[] letters = new Character[26];
        for (int i = 0; i < 26; i++) {
            letters[i] = (char) ('A' + i);
        }

       
        Arrays.sort(letters, new Comparator<Character>() {
            public int compare(Character a, Character b) {
                return counts[b - 'A'] - counts[a - 'A'];
            }
        });

        
        char[] mapping = new char[26];
        for (int i = 0; i < 26; i++) {
            mapping[letters[i] - 'A'] = ENGLISH_FREQ.charAt(i);
        }

       
        StringBuilder result = new StringBuilder();

        for (char c : cipherText.toCharArray()) {
            if (c >= 'A' && c <= 'Z') {
                result.append(mapping[c - 'A']);
            } else {
                result.append(c);
            }
        }

        return result.toString();
    }

}
