#include "raylib.h"
#include "player.h"

int main() {
    InitWindow(1200, 700, "Platformer Base");
    SetTargetFPS(60);

    // Player
    Player player;
    player.Init("assets/player.png", {100, 400});

    // Background
    Texture2D bg = LoadTexture("assets/bg.png");

    // Camera
    Camera2D cam = {0};
    cam.offset = {600, 350};
    cam.target = player.pos;
    cam.rotation = 0.0f;
    cam.zoom = 1.0f;

    while (!WindowShouldClose()) {
        float dt = GetFrameTime();

        player.Update(dt);
        cam.target = player.pos;

        BeginDrawing();
        ClearBackground(RAYWHITE);

        BeginMode2D(cam);

        // Draw background at world origin
        DrawTexture(bg, 0, 0, WHITE);

        // Draw player
        player.Draw();

        EndMode2D();

        EndDrawing();
    }

    CloseWindow();
    return 0;
}
