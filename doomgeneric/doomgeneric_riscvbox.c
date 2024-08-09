#include "doomkeys.h"
#include "m_argv.h"
#include "doomgeneric.h"

#include <stdio.h>
#include <unistd.h>

#include <stdbool.h>

void DG_Init()
{

}

void DG_DrawFrame()
{
  printf("doom_draw\n");
}

void DG_SleepMs(uint32_t ms)
{
  
}

uint32_t DG_GetTicksMs()
{
  static uint32_t cnt = 0;
  return ++cnt;
}

int DG_GetKey(int* pressed, unsigned char* doomKey)
{
  return 0;
}

void DG_SetWindowTitle(const char * title)
{

}

int main(int argc, char **argv)
{
    doomgeneric_Create(argc, argv);

    for (;;)
    {
        doomgeneric_Tick();
    }

    return 0;
}
