#ifndef COMPOSER
#define COMPOSER

#include <libfyaml.h>
#include <memory>
#include <queue>
#include <set>
#include <sqlite3.h>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <valarray>
#include <variant>
#include <vector>
#include <yaml.h>
#include <g

using config_types = std::variant<float, std::string, int>;

class Composer {
private:
  std::string target;
  std::set<char> chset;
  std::queue<char> active_window;
  std::string font;
  std::valarray<float> transform = {0.00, 0.00};
  int spacing;
  int white_space;
  int top_margin;
  int left_margin;
  int right_margin;
  int bottom_margin;
  struct fy_document *fyd;
  std::unique_ptr<sqlite3, decltype(&sqlite3_close)> db;

  void initialize_chset(std::set<char> *chset);
  void get_config(std::string config_path, struct fy_document *config);
  void initialize_db();
  void apply_transforms();
  void concat_gcode();

public:
  Composer(std::tring target) {
    initialize_chset(&chset);
    get_config("config.yaml", fyd);
    // Spin up database connection
    sqlite3 *db;
    int response = sqlite3_open("fontdch.db", &db);
    if (response != SQLITE_OK) {
      std::string errmsg = sqlite3_errmsg(db);
      sqlite3_close(db);
      throw std::runtime_error(
          "Failed to open Font Delineated Character database!" + errmsg);
    }

    // Apply Top and Left margin transforms
    // Key Assumption, always reset to top left of page, referred to as (0,0)

    // Create an unordered_map of dict(char: std::string) that maps the canon
  }
};
#endif // !COMPOSER
