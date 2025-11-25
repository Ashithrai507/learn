#pragma once
#include "raylib.h"

struct Player {
    // position is FEET position (x,y) => y is at the feet
    Vector2 pos;
    Vector2 vel;

    // movement values
    float speed;          // max horizontal speed
    float groundAccel;    // horizontal accel on ground
    float airAccel;       // horizontal accel in air
    float groundFriction; // when no input on ground
    float jumpForce;      // initial jump velocity (negative)
    bool isGrounded;

    // sprite / animation
    Texture2D sprite;
    int frameWidth;
    int frameHeight;
    int frameCount;
    float frameTime;
    float frameTimer;
    int currentFrame;
    int idleFrame;
    float scale;

    // advanced physics
    float gravity;               // base gravity
    float fallMultiplier;        // multiplier when falling
    float lowJumpMultiplier;     // multiplier when releasing jump early
    float terminalVelocity;      // max fall speed

    // coyote time & jump buffer
    float coyoteTime;            // allowed time after leaving ground to still jump
    float coyoteTimer;

    float jumpBufferTime;        // allowed time before landing to buffer jump
    float jumpBufferTimer;

    // facing
    int facing; // 1 = right, -1 = left

    // Methods
    void Init(const char *spritePath, Vector2 startPos);
    void Update(float dt);        // process input & integrate velocity
    void Draw() const;

    // Called by main after collision detection
    void Land();      // called when player lands on ground
    void LeaveGround(); // called when player leaves ground (start falling)
};
