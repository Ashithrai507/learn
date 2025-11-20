#include "raylib.h"

int main() {
    InitWindow(800, 600, "Hello from Raylib!");

    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(RAYWHITE);

        DrawText("Hello, Raylib!", 350, 280, 20, BLACK);

        EndDrawing();
    }

    CloseWindow();
    return 0;
}
