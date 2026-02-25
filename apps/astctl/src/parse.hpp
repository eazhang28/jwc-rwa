#ifndef PARSE_HPP
#define PARSE_HPP

#include "Eigen/Dense"
#include "main.h"
#include <memory>
#include <string>
extern "C" {

#include "parser.h"
}

struct gcoord {
  parser_t points;
  Eigen::MatrixXd matrix;
};

Eigen::MatrixXd gcode_to_matrix(parser_t parser, std::string data);

#endif
