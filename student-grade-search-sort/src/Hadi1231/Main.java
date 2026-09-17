package Hadi1231;
import java.util.*;
public class Main {
 
 
    static void printStudents(Student[] students) {
        System.out.println("------------------------------------");
        System.out.printf("%-5s %-20s %s%n", "No.", "Name", "Score");
        System.out.println("------------------------------------");
        for (int i = 0; i < students.length; i++) {
            
            System.out.printf("%-5d %-20s %d%n", i + 1, students[i].name, students[i].score);
        }
        System.out.println("------------------------------------");
    }
 
 
   
    public static void main(String[] args) {
 
        Scanner scanner = new Scanner(System.in);
 
        System.out.println("========================================");
        System.out.println("   STUDENT GRADE SEARCH & SORT SYSTEM  ");
        System.out.println("   Algorithms: Bubble Sort, Linear &    ");
        System.out.println("               Binary Search            ");
        System.out.println("========================================\n");
 
 
        // --- STEP 1: Collect student data from the user ---
        System.out.print("How many students do you want to enter? ");
        int n = scanner.nextInt();
        scanner.nextLine(); // clear the leftover newline after the number
 
        Student[] students = new Student[n]; // create an array with n slots
 
        System.out.println("\nEnter each student's name and score:");
        for (int i = 0; i < n; i++) {
            System.out.print("  Student " + (i + 1) + " name : ");
            String name = scanner.nextLine();
 
            System.out.print("  Student " + (i + 1) + " score: ");
            int score = scanner.nextInt();
            scanner.nextLine(); 
 
            
            students[i] = new Student(name, score);
            System.out.println();
        }
 
 
       
        System.out.println("\n--- ORIGINAL LIST (unsorted) ---");
        printStudents(students);
 
 
        
        System.out.print("\nEnter the score you want to search for: ");
        int target = scanner.nextInt();
 
 
        
        System.out.println("\n--- LINEAR SEARCH (on unsorted list) ---");
 
       
        long startTime    = System.nanoTime();
        int linearResult  = SortSearch.linearSearch(students, target);
        long linearTime   = System.nanoTime() - startTime; 
 
        if (linearResult != -1) {
            System.out.println("Found! " + students[linearResult].name +
                               " has a score of " + target +
                               " (position " + (linearResult + 1) + " in unsorted list)");
        } else {
            System.out.println("Score " + target + " was NOT found using Linear Search.");
        }
        System.out.println("Time taken: " + linearTime + " nanoseconds");
 
 
        System.out.println("\n--- BUBBLE SORT (sorting by score, low to high) ---");
        SortSearch.bubbleSort(students); // sorts the array in place
        System.out.println("Sorted list:");
        printStudents(students);
 
 
       
        System.out.println("--- BINARY SEARCH (on sorted list) ---");
 
       
        startTime        = System.nanoTime();
        int binaryResult = SortSearch.binarySearch(students, target);
        long binaryTime  = System.nanoTime() - startTime; // time taken in nanoseconds
 
        if (binaryResult != -1) {
            System.out.println("Found! " + students[binaryResult].name +
                               " has a score of " + target +
                               " (position " + (binaryResult + 1) + " in sorted list)");
        } else {
            System.out.println("Score " + target + " was NOT found using Binary Search.");
        }
        System.out.println("Time taken: " + binaryTime + " nanoseconds");
 
 
       
        System.out.println("\n========================================");
        System.out.println("        PERFORMANCE COMPARISON          ");
        System.out.println("========================================");
        System.out.printf("%-20s %-15s %-15s%n", "Algorithm", "Complexity", "Time (ns)");
        System.out.println("----------------------------------------");
        System.out.printf("%-20s %-15s %-15s%n", "Bubble Sort",   "O(n^2)",   "N/A (sort step)");
        System.out.printf("%-20s %-15s %-15d%n", "Linear Search", "O(n)",     linearTime);
        System.out.printf("%-20s %-15s %-15d%n", "Binary Search", "O(log n)", binaryTime);
        System.out.println("----------------------------------------");
 
        System.out.println("\nDISCUSSION:");
        System.out.println("  Linear Search checks students one by one — no sorting needed.");
        System.out.println("  Binary Search is faster but ONLY works on a sorted list.");
        System.out.println("  For small lists the time difference is tiny, but as the");
        System.out.println("  number of students grows, Binary Search (O log n) becomes");
        System.out.println("  significantly faster than Linear Search (O n).");
        System.out.println("  Bubble Sort has an O(n^2) cost upfront, but it is worth it");
        System.out.println("  when you need to search the same list many times.");
 
        scanner.close();
    }
}