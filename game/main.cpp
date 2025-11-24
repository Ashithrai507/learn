#include "raylib.h"
#include "player.h"

int main() {
    InitWindow(1200, 700, "Platformer Base");
    SetTargetFPS(60);

    // Player
    Player player;

    // Background
    Texture2D bg = LoadTexture("assets/bg.png");

    // Platform size (will be aligned to bottom of screen)
    const int platformHeight = 50;
    // Initialize player so its feet start on top of the platform
    player.Init("assets/player.png", {100, (float)GetScreenHeight() - platformHeight - 1});

    // PLATFORM (screen-space rectangle that fits the full width)
    Rectangle platform = { 0.0f, (float)GetScreenHeight() - platformHeight, (float)GetScreenWidth(), (float)platformHeight };

    // Camera (not following for now)
    Camera2D cam = {0};
    cam.offset = {600, 350};
    cam.target = player.pos;
    cam.rotation = 0.0f;
    cam.zoom = 1.0f;

    while (!WindowShouldClose()) {
        float dt = GetFrameTime();

        // Update Player FIRST
        player.Update(dt);

        // -----------------------------------------
        // PLATFORM COLLISION DETECTION (platform is screen-space)
        // Convert player's world position to screen space for collision
        // (camera is applied by GetWorldToScreen2D)
        Vector2 playerScreenPos = GetWorldToScreen2D(player.pos, cam);

        Rectangle playerFeet = {
            playerScreenPos.x,
            playerScreenPos.y - 5,
            player.frameWidth * player.scale,
            5
        };

        if (CheckCollisionRecs(playerFeet, platform)) {
            // Snap player's world position so the feet sit on top of the platform.
            Vector2 targetScreen = { playerScreenPos.x, platform.y };
            Vector2 worldTarget = GetScreenToWorld2D(targetScreen, cam);
            player.pos.y = worldTarget.y;
            player.vel.y = 0;
            player.isGrounded = true;
        }

        BeginDrawing();
        ClearBackground(RAYWHITE);

    DrawTexture(bg, 0, 0, WHITE);

    // Draw platform in screen-space (stays aligned to bottom)
    DrawRectangleRec(platform, DARKGRAY);

    BeginMode2D(cam);

    // Draw player (world-space, transformed by camera)
    player.Draw();

    EndMode2D();

        EndDrawing();
    }

    CloseWindow();
    return 0;
}
