#include <stdio.h>

//Function to convert ascii chars from random output stream to binary
int asctobin(int character) {
	int result = 0, i = 1, remainder;

	//Convert to binary
	while (character > 0) {
		remainder = character % 2;
		result = result + (remainder * i);
		character = character / 2;
		i = i * 10;
	}

	return(result);
}

// Test the binary against the monobit specifications
void monobit_test(int binary[]) {
	//initialise number of ones to zero.
	int ones = 0;

	//iterate through the output stream.
	for (int i = 0; i < 2500; i++) {
		int rem;
		int numOfOcc = 0;
		int temp = binary[i];

		//Check the current binary string. If it is a 1, add to the number of ones.
		while(temp > 0) {
			//Check the last bit of the binary string
			rem = temp % 10;
			//Check if it is a 1
			if (rem == 1) {
				numOfOcc++;
			}
			//Remove the last bit from the binary to check the next one
			temp /= 10;
		}

		//Add to the number of ones found in the binary output stream.
		ones += numOfOcc;
	}

	//Print results
	printf("Total 1's\t%d\n\n", ones);
	//If the number of ones is between 9725 & 10275 it passes FIPS 140-2
	if (ones >= 9725 && ones <= 10275) {printf("FIPS 140-2\tMonobit-Test\tPassed\n");} else {printf("FIPS 140-2\tMonobit-Test\tFailed\n");}
	//If the number of ones is between 9654 & 10346 it passes FIPS 140-2
	if (ones >= 9654 && ones <= 10346) {printf("FIPS 140-1\tMonobit-Test\tPassed\n");} else {printf("FIPS 140-1\tMonobit-Test\tFailed\n");}
}

//Main function
int main(int argc, char *argv[]) {
	//Open the randomly generated output
	FILE *f = fopen("random.txt", "r");

	int c, i=0;
	int final_binary[2500];

	//read the file into final_binary while converting the input to binary
	while ((c = fgetc(f)) != EOF) {
		final_binary[i] = asctobin(c);
		i++;

	}

	printf("%s", (((i*8)==20000)) ? "File is a 20000 bit block\n":"File needs to be a 20000 bit block\n");

	monobit_test(final_binary);
}
