#include "raylib.h"
#include <cmath>

int main() {
    const int screenWidth = 800;
    const int screenHeight = 600;
    InitWindow(screenWidth, screenHeight, "DVD Logo Bounce");
    Rectangle dvd = { 200, 150, 120, 60 };   
    float speedX = 100;
    float speedY = 50;
    Color dvdColor = RED;
    SetTargetFPS(60);

    while (!WindowShouldClose()) 
    {
        float dt = GetFrameTime();
        dvd.x += speedX * dt;
        dvd.y += speedY * dt;
        if (dvd.x <= 0) {
            dvd.x = 0;
            speedX *= -1;
            dvdColor = Color{ static_cast<unsigned char>(GetRandomValue(50,255)),
                              static_cast<unsigned char>(GetRandomValue(50,255)),
                              static_cast<unsigned char>(GetRandomValue(50,255)),
                              static_cast<unsigned char>(255) };
        }
        else if (dvd.x + dvd.width >= screenWidth) {
            dvd.x = screenWidth - dvd.width;
            speedX *= -1;
            dvdColor = Color{ static_cast<unsigned char>(GetRandomValue(50,255)),
                              static_cast<unsigned char>(GetRandomValue(50,255)),
                              static_cast<unsigned char>(GetRandomValue(50,255)),
                              static_cast<unsigned char>(255) };
        }
        if (dvd.y <= 0) {
            dvd.y = 0;
            speedY *= -1;
            dvdColor = Color{ static_cast<unsigned char>(GetRandomValue(50,255)),
                              static_cast<unsigned char>(GetRandomValue(50,255)),
                              static_cast<unsigned char>(GetRandomValue(50,255)),
                              static_cast<unsigned char>(255) };
        }
        else if (dvd.y + dvd.height >= screenHeight) {
            dvd.y = screenHeight - dvd.height;
            speedY *= -1;
            dvdColor = Color{ static_cast<unsigned char>(GetRandomValue(50,255)),
                              static_cast<unsigned char>(GetRandomValue(50,255)),
                              static_cast<unsigned char>(GetRandomValue(50,255)),
                              static_cast<unsigned char>(255) };
        }
        BeginDrawing();
        ClearBackground(BLACK);

        DrawRectangleRec(dvd, dvdColor);

        DrawText("DVD Screensaver Simulation", 10, 10, 20, WHITE);

        EndDrawing();
    }

    CloseWindow();
    return 0;
}
