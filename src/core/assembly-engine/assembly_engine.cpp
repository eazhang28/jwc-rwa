#include <set>
#include <sqlite3.h>
#include <string>
#include <vector>
#include <yaml.h>

#include "assembly_engine.hpp"

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

int main() { COMPOSER::Composer("farget", "./config.yaml"); }
