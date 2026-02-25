#include "sqlut.hpp"
#include <memory>
#include <string>

extern "C" {
#include <sqlite3.h>
}

int get_data_callback(void *dataret, int count, char **data, char **columns) {
  std::string &d = *static_cast<std::string *>(dataret);
  if (data[0]) {
    d.append(data[0]);
  }
  return 0;
}

int get_chars(struct sqlite3 *db_handle, std::unique_ptr<std::string> &data,
              char ch) {

  data = std::make_unique<std::string>();
  void *data_handle = static_cast<void *>(data.get());
  char *errmsg_cstr = nullptr;
  std::string handle;

  char query[50];
  snprintf(query, sizeof(query), "SELECT data FROM FCLOOKUP WHERE char == '%c'",
           ch);
  int return_status = sqlite3_exec(db_handle, query, get_data_callback,
                                   data_handle, &errmsg_cstr);
  if (return_status != SQLITE_OK) {
    sqlite3_free(errmsg_cstr);
  }

  return return_status;
}
