#include "assembly_engine.hpp"
#include <iostream>
#include <set>
#include <sqlite3.h>
#include <string>
#include <vector>
#include <yaml.h>

class CharVMap {

  // Behavior: Take an input character, map its gcode coordinates to 2xN space,
  // where N is the set of G1 command arguments.
  //
private:
  std::string target;
  std::set<char> vmap;

  std::vector<int> vec;

public:
  CharVMap(std::string input, std::set<char> vmap)
      : target(input), vmap(vmap) {};
};

struct example {
  int x = 0;

  example operator+(int addor) {
    example temp;
    temp.x = this->x + addor;
    return temp;
  }
};

int main() {

  example p1 = {10};
  example blab = p1 + 5;
  std::cout << "Sum of points: (" << blab.x << ")" << std::endl;
}
