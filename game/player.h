#pragma once
#include "raylib.h"

struct Player {
    Vector2 pos;
    Vector2 vel;

    float speed;
    float jumpForce;
    bool isGrounded;

    Texture2D sprite;
    int frameWidth;
    int frameHeight;
    int frameCount;
    float frameTime;
    float frameTimer;
    int currentFrame;
    float scale;

    void Init(const char *spritePath, Vector2 startPos);
    void Update(float dt);
    void Draw();
};
