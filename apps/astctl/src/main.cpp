#ifndef MAIN
#define MAIN
#include "main.hpp"
#include "parse.hpp"
#include "sqlut.hpp"
#include <memory>
#include <unordered_map>
#include <unordered_set>
#include <vector>

extern "C" {
#include "parser.h"
#include <sqlite3.h>
#include <string.h>
}
#include "Eigen/Dense"
#include <iostream>
#include <math.h>
#include <string>

int main(void) {

  // this program is ran from the daemon state machine
  // receives input ./runtime_engine <string_input> <config file (in root)>
  // tasks, zero the machine, and then read for bounds
  // read config file, apply transformations as necessary
  // put input into sequencer
  // sequencer: retrieve necessary characters from sqlite LUT
  // sequence characters to match input order (delete from cache when no longer
  // needed) stream send gcode orders confirm end

  std::unordered_map<char, uint> map;

  std::string input = "HIALL";

  for (char c : input) {
    map[c]++;
  }

  std::vector<struct gcoord> arr;

  parser_t parser;
  parser_init(&parser);
  struct sqlite3 *db_handle;
  std::unique_ptr<std::string> data;
  sqlite3_open("fontdch.db", &db_handle);
  for (uint i = 0; i < input.length(); i++) {
    struct gcoord token;
    char chr = input[i];
    map[chr]--;
    get_chars(db_handle, data, chr);
    parser_read_gcode_text(&parser, data->c_str());
    Eigen::MatrixXd mat = gcode_to_matrix(parser, *data);
    token.matrix = mat;
    std::cout << token.matrix << std::endl;
    arr.push_back(token);
  }

  for (const auto &crd : arr) {
    std::cout << crd.matrix << std::endl;
  }

  sqlite3_close(db_handle);
  parser_free(&parser);
  return 0;
}
#endif
