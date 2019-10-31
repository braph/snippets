#include <stdio.h>
#include <xcb/xcb.h>
#include <xcb/xcb_aux.h>

xcb_connection_t *xconn;
xcb_screen_t *xscreen;

int main(int argc, char **argv)
{
  int screen_no = 0;
  xcb_generic_event_t *e;

  xconn = xcb_connect(NULL, &screen_no);
  if (xcb_connection_has_error(xconn)) {
    printf("Error!\n");
    return 1;
  }

  xscreen = xcb_aux_get_screen(xconn, screen_no);
  if (! xscreen) {
    printf("Error getting screen\n");
    return 1;
  }

  for (int i = 0; i < 3; ++i) {
    e = xcb_wait_for_event(xconn);
    if (e) {
      printf("ev->response_type = %X\n", e->response_type);
    }
  }

  xcb_disconnect(xconn);
  return 0;
}

