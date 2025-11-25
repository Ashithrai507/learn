#include "player.h"
#include <algorithm>

// small helper: move value toward target by maxDelta
static float Approach(float value, float target, float maxDelta) {
    if (value < target) {
        value += maxDelta;
        if (value > target) value = target;
    } else if (value > target) {
        value -= maxDelta;
        if (value < target) value = target;
    }
    return value;
}

void Player::Init(const char *spritePath, Vector2 startPos) {
    sprite = LoadTexture(spritePath);

    frameCount = 6;
    frameWidth = sprite.width / frameCount;
    frameHeight = sprite.height;

    pos = startPos;   // FEET position
    vel = {0, 0};

    // Movement tuning (feel free to tweak)
    speed = 260.0f;
    groundAccel = 2600.0f;
    airAccel = 1000.0f;
    groundFriction = 2000.0f;

    jumpForce = -520.0f; // strong jump

    // Animation
    frameTime = 0.08f;
    frameTimer = 0.0f;
    currentFrame = 0;
    scale = 0.35f;

    // Advanced gravity
    gravity = 1800.0f;
    fallMultiplier = 2.2f;      // faster fall
    lowJumpMultiplier = 3.0f;   // cut short when jump released
    terminalVelocity = 1200.0f;

    // Coyote & buffer
    coyoteTime = 0.12f;
    coyoteTimer = 0.0f;

    jumpBufferTime = 0.12f;
    jumpBufferTimer = 0.0f;

    isGrounded = false;
    facing = 1;
}

void Player::Update(float dt) {
    // timers
    if (coyoteTimer > 0.0f) coyoteTimer -= dt;
    if (jumpBufferTimer > 0.0f) jumpBufferTimer -= dt;

    // INPUT
    float inputX = 0.0f;
    if (IsKeyDown(KEY_A)) inputX -= 1.0f;
    if (IsKeyDown(KEY_D)) inputX += 1.0f;

    if (inputX > 0) facing = 1;
    else if (inputX < 0) facing = -1;

    // Horizontal movement: smooth acceleration
    float targetVx = inputX * speed;
    float accel = isGrounded ? groundAccel : airAccel;
    vel.x = Approach(vel.x, targetVx, accel * dt);

    // friction when no input and grounded
    if (isGrounded && inputX == 0.0f) {
        vel.x = Approach(vel.x, 0.0f, groundFriction * dt);
        // tiny clamp to avoid micro velocity
        if (fabs(vel.x) < 1.0f) vel.x = 0.0f;
    }

    // JUMP BUFFERING
    if (IsKeyPressed(KEY_SPACE)) {
        jumpBufferTimer = jumpBufferTime;
    }

    // CAN JUMP? (coyote allowed)
    bool canJump = (isGrounded || coyoteTimer > 0.0f);
    if (jumpBufferTimer > 0.0f && canJump) {
        // perform jump
        vel.y = jumpForce;    // negative
        isGrounded = false;
        coyoteTimer = 0.0f;
        jumpBufferTimer = 0.0f;
    }

    // GRAVITY (variable)
    // if going up and player released jump -> stronger gravity to shorten jump
    bool holdingJump = IsKeyDown(KEY_SPACE);

    if (vel.y < 0.0f) {
        // ascending
        if (!holdingJump) {
            vel.y += gravity * lowJumpMultiplier * dt;
        } else {
            vel.y += gravity * dt;
        }
    } else {
        // descending
        vel.y += gravity * fallMultiplier * dt;
    }

    // clamp terminal velocity
    if (vel.y > terminalVelocity) vel.y = terminalVelocity;

    // integrate position (pos = feet position)
    pos.x += vel.x * dt;
    pos.y += vel.y * dt;

    // ANIMATION (simple)
    if (fabs(vel.x) > 1.0f) {
        frameTimer += dt;
        if (frameTimer >= frameTime) {
            frameTimer = 0.0f;
            currentFrame = (currentFrame + 1) % frameCount;
        }
    } else {
        currentFrame = 0; // idle frame
    }
}

void Player::Land() {
    // Called from main when collision determined we landed this frame.
    isGrounded = true;
    coyoteTimer = coyoteTime;
    jumpBufferTimer = 0.0f; // clear buffered jumps
    vel.y = 0.0f; // ensure vertical stop
}

void Player::LeaveGround() {
    // Called from main when collision determined we left ground
    if (isGrounded) {
        isGrounded = false;
        // start coyote timer
        coyoteTimer = coyoteTime;
    }
}

void Player::Draw() const {
    Rectangle src = {
        (float)currentFrame * frameWidth,
        0,
        (float)frameWidth,
        (float)frameHeight
    };

    // Determine flipping with DrawTexturePro: if facing left, flip by negative width and adjust src.x
    Rectangle dest = {
        pos.x,
        pos.y - (frameHeight * scale),
        frameWidth * scale,
        frameHeight * scale
    };

    Vector2 origin = {0, 0};
    float rotation = 0.0f;

    if (facing >= 0) {
        // normal
        DrawTexturePro(sprite, src, dest, origin, rotation, WHITE);
    } else {
        // flip horizontally: we draw with negative width in src and shift dest.x to keep feet aligned
        Rectangle srcFlip = { src.x + src.width, src.y, -src.width, src.height };
        DrawTexturePro(sprite, srcFlip, dest, origin, rotation, WHITE);
    }
}
