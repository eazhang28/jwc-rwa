#ifndef MAIN_JWC
#define MAIN_JWC

extern "C" {
#include "cstdio"
#include "parser.h"
#include <sqlite3.h>
}
#include "Eigen/Dense"
#include <iostream>
#include <math.h>
#include <string>

int get_data_callback(void *dataret, int count, char **data, char **columns);

#endif
