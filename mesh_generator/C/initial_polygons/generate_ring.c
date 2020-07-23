#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define PI acos(-1.0)

int main(int argc, char *argv[]) {
	double outter_radius = atof(argv[1]);
	double inner_radius = atof(argv[3]);
	// Center is in (0,0)
	
	int outter_points_num = atoi(argv[2]);
	int inner_points_num = atoi(argv[4]);
	
	double x = outter_radius;
	double y = 0.0;
	printf("%lf %lf\n", x, y);
	for (int i = 1; i < outter_points_num; ++i) {
		x = cos((2*PI/outter_points_num) * i) * outter_radius;
		y = sin((2*PI/outter_points_num) * i) * outter_radius;

		printf("%lf %lf\n", x, y);
	}
	
	printf("\n");

	x = inner_radius;
	y = 0.0;
	printf("%lf %lf\n", x, y);
	for (int i = 1; i < inner_points_num; ++i) {
		x = cos((-2*PI/inner_points_num) * i) * inner_radius;
		y = sin((-2*PI/inner_points_num) * i) * inner_radius;

		printf("%lf %lf\n", x, y);
	}

	printf("\n");
	
	return 0;
}
