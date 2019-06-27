package usage;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;

public class Splitter {
	
	
	private final static String INPUT_DIR = "data/student-essays/original";
	private final static String TEST_DIR = "data/student-essays/split/full-essay/test";
	private final static String TRAINING_DIR = "data/student-essays/split/full-essay/training";
	
	
	
	

	public static void main(String[] args) throws IOException {
		File input = new File(INPUT_DIR);
		ArrayList<File> files = new ArrayList<File>();
		for(File file : input.listFiles()) {
			files.add(file);
		}

		int numFiles = files.size();
		int numTest = (int)(files.size() * 0.8);
		
		Random randomGenerator = new Random(123456789);
		
		ArrayList<Integer> indices = new ArrayList<Integer>();
		
		for (int i = 0; i < numTest; i++) {
			int rand = randomGenerator.nextInt(numFiles);
			while (indices.contains(new Integer(rand))) {
				rand = randomGenerator.nextInt(numFiles);
			}
			indices.add(new Integer(rand));
		}
		Collections.sort(indices, Collections.reverseOrder());
		
		for (int i : indices) {
			File file = files.remove(i);
			String fileName = file.getName();
		    Path copied = Paths.get(TRAINING_DIR + "/" + fileName);
		    Path original = Paths.get(INPUT_DIR + "/" + fileName);
		    Files.copy(original, copied, StandardCopyOption.REPLACE_EXISTING);
		}
		for (File file : files) {
			String fileName = file.getName();
		    Path copied = Paths.get(TEST_DIR + "/" + fileName);
		    Path original = Paths.get(INPUT_DIR + "/" + fileName);
		    Files.copy(original, copied, StandardCopyOption.REPLACE_EXISTING);
		}
	}

}
