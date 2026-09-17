package Hadi1231;

public class SortSearch {
	   public static void bubbleSort(Student[] students) {
	        int n = students.length;
	        boolean swapped; 
	 
	       
	        for (int i = 0; i < n - 1; i++) {
	            swapped = false;
	 
	          
	            for (int j = 0; j < n - 1 - i; j++) {
	 
	               
	                if (students[j].score > students[j + 1].score) {
	                    Student temp   = students[j];       
	                    students[j]     = students[j + 1]; 
	                    students[j + 1] = temp;            
	                    swapped = true;
	                }
	            }
	 
	           
	            if (!swapped) break;
	        }
	    }
	   public static int linearSearch(Student[] students, int targetScore) {
	       
	        for (int i = 0; i < students.length; i++) {
	            if (students[i].score == targetScore) {
	                return i; 
	            }
	        }
	        return -1; 
	    }
	   
	   public static int binarySearch(Student[] students, int targetScore) {
	        int low  = 0;                     
	        int high = students.length - 1;  
	 
	        
	        while (low <= high) {
	            int mid = (low + high) / 2;  
	 
	            if (students[mid].score == targetScore) {
	                return mid;             
	            } else if (students[mid].score < targetScore) {
	                low = mid + 1;          
	            } else {
	                high = mid - 1;         
	            }
	        }
	        return -1;
	    }
	
}
