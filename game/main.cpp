#include "raylib.h"
#include "player.h"

int main() {
    InitWindow(1200, 700, "Advanced Physics - B style");
    SetTargetFPS(60);

    Player player;
    player.Init("assets/player.png", {300.0f, 400.0f});
    Texture2D bg = LoadTexture("assets/bg.png");
    while (!WindowShouldClose()) {
        float dt = GetFrameTime();
        player.Update(dt);
        float spriteW = player.frameWidth * player.scale;
        float spriteH = player.frameHeight * player.scale;

        Rectangle playerBox = {
            player.pos.x,
            player.pos.y - spriteH,
            spriteW,
            spriteH
        };

        bool landedThisFrame = false;

        // LEFT
        if (playerBox.x < 0.0f) {
            player.pos.x = 0.0f;
            player.vel.x = 0.0f;
        }

        // RIGHT
        if (playerBox.x + playerBox.width > GetScreenWidth()) {
            player.pos.x = GetScreenWidth() - playerBox.width;
            player.vel.x = 0.0f;
        }

        // CEILING
        if (playerBox.y < 0.0f) {
            player.pos.y = spriteH;
            player.vel.y = 0.0f;
        }

        if (playerBox.y + playerBox.height > GetScreenHeight()) {
            player.pos.y = GetScreenHeight();
            landedThisFrame = true;

        }

        if (landedThisFrame) {
            player.Land();
        } else {
            if (player.isGrounded) {
                player.LeaveGround();
            }
        }
        BeginDrawing();
        ClearBackground(RAYWHITE);
        DrawTexture(bg, 0, 0, WHITE);
        player.Draw();
        EndDrawing();
    }

    CloseWindow();
    return 0;
}
