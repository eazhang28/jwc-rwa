#ifndef SQLUT_HPP
#define SQLUT_HPP

#include <memory>
#include <string>
int get_data_callback(void *dataret, int count, char **data, char **columns);
int get_chars(struct sqlite3 *db_handle, std::unique_ptr<std::string> &data,
              char ch);
#endif
