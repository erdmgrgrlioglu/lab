// File: blank_xorg_client.c
#include <X11/Xlib.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    Display *display;
    Window window;
    int screen;

    // Open connection to the X server
    display = XOpenDisplay(NULL);
    if (display == NULL) {
        fprintf(stderr, "Unable to open X display\n");
        exit(1);
    }

    screen = DefaultScreen(display);

    // Create a simple window
    window = XCreateSimpleWindow(display, RootWindow(display, screen), 
                                 10, 10, 640, 480, 1,
                                 BlackPixel(display, screen),
                                 WhitePixel(display, screen));

    // Select kind of events we are interested in
    XSelectInput(display, window, ExposureMask | KeyPressMask);

    // Map (show) the window
    XMapWindow(display, window);

    XGCValues xgcv;
    xgcv.line_style = LineSolid;
    xgcv.line_width = 1;

    unsigned long valuemask = GCLineStyle | GCLineWidth;
    GC gc = XCreateGC(display, window, valuemask, &xgcv);

    // Event loop
    XEvent event;
    while (1) {
        XNextEvent(display, &event);
        if (event.type == ButtonPress) {
            XDrawPoint(display, event.xbutton.window, gc, event.xbutton.x, event.xbutton.y);
        }
    }

    // Cleanup
    XDestroyWindow(display, window);
    XCloseDisplay(display); 

    return 0;
}
