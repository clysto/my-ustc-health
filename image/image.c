#include <cairo/cairo.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void current_time(char *buff) {
  putenv("TZ=Asia/Shanghai");
  time_t rawtime = time(NULL);
  struct tm *ptm = localtime(&rawtime);
  strftime(buff, 32, "%Y.%m.%d %T", ptm);
}

int main(int argc, char const *argv[]) {
  cairo_surface_t *surface = cairo_image_surface_create_from_png("base.png");
  cairo_t *cr = cairo_create(surface);

  char date_str[32] = "", time_str[32] = "";
  current_time(date_str);
  strncpy(time_str, date_str + 11, 5);

  puts(date_str);

  cairo_set_source_rgb(cr, 1, 1, 1);
  cairo_rectangle(cr, 364, 881, 650, 70);
  cairo_fill(cr);

  cairo_set_font_size(cr, 56);
  cairo_set_source_rgb(cr, 148. / 256., 148. / 256., 158. / 256.);
  cairo_move_to(cr, 420, 936);
  cairo_show_text(cr, date_str);

  cairo_set_source_rgb(cr, 246.0 / 256.0, 246.0 / 256.0, 246.0 / 256.0);
  cairo_rectangle(cr, 0, 0, 249, 116);
  cairo_fill(cr);

  cairo_set_font_size(cr, 46);
  cairo_set_source_rgb(cr, 0, 0, 0);
  cairo_move_to(cr, 70, 88);
  cairo_show_text(cr, time_str);

  cairo_destroy(cr);
  cairo_surface_write_to_png(surface, "a.png");
  cairo_surface_destroy(surface);
  return 0;
}
