//Include libraries imported to path
#include "gdef.h"
#include "swrite.h"
#include "bbattery.h"
#include "stdlib.h"

int main(int argc, char *argv[]) {
	//Check if the program received a file in the positional parameter list
    if (argc > 1) {
		//Write only the results of the tests to the command line
		//No logs of the individual tests in the battery
		swrite_Basic = FALSE;
		//Run the bbattery module on SmallCrush
		//Takes a file input from the positional parameter list
		bbattery_SmallCrushFile(argv[1]);
	} else {
		//If no file is detected, output to the console
		printf("Please include a file.");
	}
}