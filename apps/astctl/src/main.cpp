extern "C" {
#include "cstdio"
#include "parser.h"
}
#include "Eigen/Dense"
#include <iostream>
#include <math.h>
#include <sqlite3.h>
#include <string>
#include <vector>

static int special_callback(void *dataret, int count, char **data,
                            char **columns);

static int special_callback(void *dataret, int count, char **data,
                            char **columns) {
  std::string &d = *static_cast<std::string *>(dataret);
  d.append(data[0]);
  return 0;
}

int main(void) {
  struct sqlite3 *db_handle;
  sqlite3_open("fontdch.db", &db_handle);

  char query[100] = "SELECT * FROM FCLOOKUP";
  std::string errmsg(1000, '\0');
  char *errmsg_cstr = &errmsg[0];
  std::string clock;
  void *data_handle = static_cast<void *>(&clock);
  sqlite3_exec(db_handle, "SELECT data FROM FCLOOKUP WHERE char == 'C'",
               special_callback, data_handle, &errmsg_cstr);
  std::string &d = *static_cast<std::string *>(data_handle);
  // std::cout << d << std::endl;
  //  std::string &data = *static_cast<std::string *>(data_handle);
  sqlite3_close(db_handle);

  parser_t parser;
  parser_init(&parser);
  parser_read_gcode_text(&parser, d.c_str());
  gcode_points_t *point = parser.gcode;
  std::vector<float> vector;

  int dim = 0;
  gcode_points_t *temp = parser.gcode;
  do {
    dim++;
  } while ((temp = (gcode_points_t *)temp->next) != NULL);

  int i = 0;
  Eigen::MatrixXd m(dim, 2);
  do {
    m(i, 0) = point->ideal.x;
    m(i, 1) = point->ideal.y;
    i++;
  } while ((point = (gcode_points_t *)point->next) != NULL);

  std::cout << m.array() * 200 << std::endl;

  parser_free(&parser);
  return 0;
}
