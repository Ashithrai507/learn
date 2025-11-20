#include "raylib.h"
#include "raymath.h"
#include <cmath>
#include <cstdlib>
#include <ctime>

// Movement constants
#define GRAVITY         32.0f
#define MAX_SPEED       20.0f
#define CROUCH_SPEED     5.0f
#define JUMP_FORCE      12.0f
#define MAX_ACCEL      150.0f
#define FRICTION         0.86f
#define AIR_DRAG         0.98f
#define CONTROL         15.0f
#define CROUCH_HEIGHT    0.0f
#define STAND_HEIGHT     1.0f
#define BOTTOM_HEIGHT    0.5f

typedef struct {
    Vector3 position;
    Vector3 velocity;
    Vector3 dir;
    bool isGrounded;
} Body;

static Vector2 sensitivity = { 0.001f, 0.001f };
// Unit cube model used for textured buildings (created at startup if needed)
static Model cubeModel = { 0 };
static bool cubeModelCreated = false;

static Body player = { 0 };
static Vector2 lookRotation = { 0 };
static float headTimer = 0.0f;
static float walkLerp = 0.0f;
static float headLerp = STAND_HEIGHT;
static Vector2 lean = { 0 };

static void DrawLevel(Texture2D floorTex, Texture2D buildingTex);
static void UpdateCameraFPS(Camera *camera);
static void UpdateBody(Body *body, float rot, char side, char forward, bool jumpPressed, bool crouchHold);

int main(void)
{
    const int screenWidth = 1280;
    const int screenHeight = 720;

    InitWindow(screenWidth, screenHeight, "Raylib FPS Movement with Textured Buildings");

    // Load textures
    Texture2D floorTex = LoadTexture("assets/floor.png");
    Texture2D buildingTex = LoadTexture("assets/building.png");

    // Create a unit cube model used to draw textured cubes (we'll set material textures per-draw)
    Mesh cubeMesh = GenMeshCube(1.0f, 1.0f, 1.0f);
    cubeModel = LoadModelFromMesh(cubeMesh);
    cubeModelCreated = true;
    // If building texture is available, assign it as default material texture
    if (buildingTex.id != 0) SetMaterialTexture(&cubeModel.materials[0], MATERIAL_MAP_DIFFUSE, buildingTex);

    // Initialize player
    player.position = {0.0f, 0.0f, 0.0f};
    player.velocity = {0};
    player.dir = {0,0,1};
    player.isGrounded = true;

    Camera camera = {0};
    camera.position = { 0.0f, BOTTOM_HEIGHT + headLerp, 0.0f };
    camera.fovy = 60.0f;
    camera.projection = CAMERA_PERSPECTIVE;

    DisableCursor();
    SetTargetFPS(60);

    while (!WindowShouldClose())
    {
        Vector2 mouseDelta = GetMouseDelta();
        lookRotation.x -= mouseDelta.x * sensitivity.x;
        lookRotation.y += mouseDelta.y * sensitivity.y;

        char side = (IsKeyDown(KEY_D) - IsKeyDown(KEY_A));
        char forward = (IsKeyDown(KEY_W) - IsKeyDown(KEY_S));
        bool crouching = IsKeyDown(KEY_LEFT_CONTROL);
        UpdateBody(&player, lookRotation.x, side, forward, IsKeyPressed(KEY_SPACE), crouching);

        float delta = GetFrameTime();
        headLerp = Lerp(headLerp, crouching ? CROUCH_HEIGHT : STAND_HEIGHT, 20.0f * delta);

        camera.position = {
            player.position.x,
            player.position.y + (BOTTOM_HEIGHT + headLerp),
            player.position.z
        };

        UpdateCameraFPS(&camera);

        BeginDrawing();
        ClearBackground(RAYWHITE);

        BeginMode3D(camera);
        DrawLevel(floorTex, buildingTex);
        EndMode3D();

        DrawText("WASD to move | Mouse to look | SPACE to jump", 20, 20, 20, DARKGRAY);

        EndDrawing();
    }

    // Unload resources
    UnloadTexture(floorTex);
    UnloadTexture(buildingTex);
    if (cubeModelCreated) UnloadModel(cubeModel);

    CloseWindow();
    return 0;
}


//--------------------------------------------------------------------------
// DRAW LEVEL WITH TEXTURED BUILDINGS + FLOOR
//--------------------------------------------------------------------------
static void DrawLevel(Texture2D floorTex, Texture2D buildingTex)
{
    // Draw floor (Plane)
    DrawPlane((Vector3){0, 0, 0}, (Vector2){50, 50}, WHITE);
    if (cubeModelCreated && floorTex.id != 0)
    {
        // use the cube model scaled to a very flat box as the textured floor
        SetMaterialTexture(&cubeModel.materials[0], MATERIAL_MAP_DIFFUSE, floorTex);
        DrawModelEx(cubeModel, (Vector3){0, -0.01f, 0}, (Vector3){0, 1, 0}, 0.0f, (Vector3){100.0f, 0.02f, 100.0f}, WHITE);
        // restore building texture if available
        if (buildingTex.id != 0) SetMaterialTexture(&cubeModel.materials[0], MATERIAL_MAP_DIFFUSE, buildingTex);
    }
    else
    {
        DrawCube((Vector3){0, -0.01f, 0}, 100, 0.02f, 100, WHITE);
    }

    // Buildings (Textured Cubes)
    Vector3 size = {4, 8, 4};

    if (cubeModelCreated && buildingTex.id != 0)
    {
        DrawModelEx(cubeModel, (Vector3){10,4,10}, (Vector3){0,1,0}, 0.0f, size, WHITE);
        DrawModelEx(cubeModel, (Vector3){-10,4,10}, (Vector3){0,1,0}, 0.0f, size, WHITE);
        DrawModelEx(cubeModel, (Vector3){10,4,-10}, (Vector3){0,1,0}, 0.0f, size, WHITE);
        DrawModelEx(cubeModel, (Vector3){-10,4,-10}, (Vector3){0,1,0}, 0.0f, size, WHITE);
    }
    else
    {
        DrawCubeV((Vector3){10,4,10}, size, WHITE);
        DrawCubeV((Vector3){-10,4,10}, size, WHITE);
        DrawCubeV((Vector3){10,4,-10}, size, WHITE);
        DrawCubeV((Vector3){-10,4,-10}, size, WHITE);
    }

    // Big tower
    if (cubeModelCreated && buildingTex.id != 0)
    {
        DrawModelEx(cubeModel, (Vector3){0,8,20}, (Vector3){0,1,0}, 0.0f, (Vector3){6,16,6}, WHITE);
    }
    else
    {
        DrawCube((Vector3){0,8,20}, 6, 16, 6, WHITE);
    }
}


//--------------------------------------------------------------------------
// FPS CAMERA UPDATE (YOUR ORIGINAL FUNCTION)
//--------------------------------------------------------------------------
static void UpdateCameraFPS(Camera *camera)
{
    const Vector3 up = {0.0f, 1.0f, 0.0f};
    const Vector3 forward = {0,0,-1};

    Vector3 yaw = Vector3RotateByAxisAngle(forward, up, lookRotation.x);
    Vector3 right = Vector3Normalize(Vector3CrossProduct(yaw, up));
    Vector3 pitch = Vector3RotateByAxisAngle(yaw, right, -lookRotation.y);

    camera->target = Vector3Add(camera->position, pitch);
    camera->up = up;
}


//--------------------------------------------------------------------------
// PLAYER PHYSICS UPDATE
//--------------------------------------------------------------------------
static void UpdateBody(Body *body, float rot, char side, char forward, bool jump, bool crouch)
{
    Vector2 input = {(float)side, (float)-forward};
    float dt = GetFrameTime();

    if (!body->isGrounded)
        body->velocity.y -= GRAVITY * dt;

    if (body->isGrounded && jump) {
        body->velocity.y = JUMP_FORCE;
        body->isGrounded = false;
    }

    Vector3 front = {sinf(rot), 0, cosf(rot)};
    Vector3 right = {cosf(-rot), 0, sinf(-rot)};
    Vector3 desired = {
        input.x * right.x + input.y * front.x,
        0.0f,
        input.x * right.z + input.y * front.z
    };

    float accel = MAX_ACCEL * dt;
    body->velocity.x += desired.x * accel;
    body->velocity.z += desired.z * accel;

    body->velocity.x *= body->isGrounded ? FRICTION : AIR_DRAG;
    body->velocity.z *= body->isGrounded ? FRICTION : AIR_DRAG;

    body->position.x += body->velocity.x * dt;
    body->position.y += body->velocity.y * dt;
    body->position.z += body->velocity.z * dt;

    if (body->position.y <= 0) {
        body->position.y = 0;
        body->velocity.y = 0;
        body->isGrounded = true;
    }
}
