#include <cairo/cairo.h>
#include <cairo/cairo-ft.h>
#include <freetype2/ft2build.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include FT_SFNT_NAMES_H
#include FT_FREETYPE_H
#include FT_GLYPH_H
#include FT_OUTLINE_H
#include FT_BBOX_H
#include FT_TYPE1_TABLES_H

void current_time(char *buff) {
  putenv("TZ=Asia/Shanghai");
  time_t rawtime = time(NULL);
  struct tm *ptm = localtime(&rawtime);
  strftime(buff, 32, "%Y.%m.%d %T", ptm);
}

int main(int argc, char const *argv[]) {
  FT_Library value;
  FT_Face face;
  cairo_surface_t *surface = cairo_image_surface_create_from_png("base.png");
  cairo_t *cr = cairo_create(surface);
  cairo_font_face_t *ct;

  char date_str[32] = "", time_str[32] = "";
  current_time(date_str);
  strncpy(time_str, date_str + 11, 5);

  puts(date_str);

  FT_Init_FreeType(&value);
  FT_New_Face(value, "Roboto-Bold.ttf", 0, &face);
  ct = cairo_ft_font_face_create_for_ft_face(face, 0);

  cairo_set_source_rgb(cr, 1, 1, 1);
  cairo_rectangle(cr, 364, 881, 650, 70);
  cairo_fill(cr);

  // 设置字体
  cairo_set_font_face(cr, ct);

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
