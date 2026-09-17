package Hadi1231;
import java.util.*;
public class main {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner s=new Scanner(System.in);
		 System.out.println("======================================");
	        System.out.println(" Automated Cryptanalysis System ");
	        System.out.println("======================================\n");

	        System.out.println("Enter the ciphertext:");
	        String cipherText = s.nextLine();

	        System.out.println("\n--- ANALYZING CIPHERTEXT ---");

	        // Step 1: Detect cipher type
	        String detected = CipherDetector.detectCipher(cipherText);
	        System.out.println("\nDetected Cipher Type: " + detected);

	        System.out.println("\n--- ATTACKING CIPHER ---");

	        // Step 2: Handle based on detection
	        if (detected.equals("Caesar")) {

	            System.out.println("\n[Caesar Cipher Attack]");
	            CaesarBreaker.breakCipher(cipherText);

	        } else {

	            System.out.println("\n[Substitution Cipher Attempt]");
	            String subResult = SubstitutionBreaker.breakSubstitution(cipherText);
	            System.out.println("Approx. Decryption (Substitution):");
	            System.out.println(subResult);

	            System.out.println("\n[Transposition Cipher Attempt]");
	            String transResult = TranspositionBreaker.breakTransposition(cipherText);
	            System.out.println("Approx. Decryption (Transposition):");
	            System.out.println(transResult);
	        }

	        System.out.println("\n======================================");
	        System.out.println(" Analysis Completed ");
	        System.out.println("======================================");
	        FrequencyAnalyzer.printFrequencies(cipherText);
	      

	        s.close();
	    }


}
