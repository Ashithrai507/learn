#include "player.h"

void Player::Init(const char *spritePath, Vector2 startPos) {
    sprite = LoadTexture(spritePath);

    frameCount = 6; // change if your sheet has different number of frames
    frameWidth = sprite.width / frameCount;
    frameHeight = sprite.height;

    pos = startPos;
    vel = {0, 0};

    speed = 200.0f;
    jumpForce = -350.0f;
    isGrounded = false;

    frameTime = 0.1f;
    frameTimer = 0.0f;
    currentFrame = 0;
}

void Player::Update(float dt) {
    vel.x = 0;

    if (IsKeyDown(KEY_A)) vel.x = -speed;
    if (IsKeyDown(KEY_D)) vel.x = speed;

    if (isGrounded && IsKeyPressed(KEY_SPACE)) {
        vel.y = jumpForce;
        isGrounded = false;
    }

    vel.y += 900 * dt;

    pos.x += vel.x * dt;
    pos.y += vel.y * dt;

    if (pos.y >= 400) {
        pos.y = 400;
        vel.y = 0;
        isGrounded = true;
    }

    if (vel.x != 0) {
        frameTimer += dt;
        if (frameTimer >= frameTime) {
            frameTimer = 0;
            currentFrame++;
            if (currentFrame >= frameCount) currentFrame = 0;
        }
    }
}

void Player::Draw() {
    Rectangle src = {
        (float)currentFrame * frameWidth,
        0,
        (float)frameWidth,
        (float)frameHeight
    };

    if (vel.x < 0) src.width = -frameWidth;

    DrawTextureRec(sprite, src, pos, WHITE);
}
