#include <assert.h>
#include "../libraries/PlantController/src/PlantController.h"
using plant::Inputs;
using plant::PlantController;
int main() {
  PlantController c;
  assert(!c.begin(0, {}).pumpRequested);
  assert(!c.update(0, {true,false,false,4095}).pumpRequested);
  assert(!c.update(34, {true,false,false,4095}).pumpRequested);
  assert(c.update(35, {true,false,false,4095}).pumpRequested);
  auto o=c.update(36, {false,false,false,0});
  assert(o.pumpRequested && o.doseMs==5000); // release and pot change do not alter dose
  assert(c.update(5034, {}).pumpRequested);
  assert(!c.update(5035, {true}).pumpRequested);
  assert(!c.update(6000, {true}).pumpRequested); // held cannot repeat
  c.update(6001, {});
  assert(c.update(6035, {}).lockedOut);
  assert(!c.update(6036, {}).lockedOut);
  c.update(6040,{true,false,false,2048});
  o=c.update(6075,{true,false,false,2048});
  assert(o.pumpRequested && o.doseMs==2500);
  o=c.update(6076,{true,true,true,4095});
  assert(!o.pumpRequested && o.redLed && o.blueLed && o.greenLed);
  assert(!c.update(7000,{true}).pumpRequested);
  c.begin(0,{false,false,true});
  assert(c.update(50,{}).lockedOut);
  assert(!c.update(85,{}).lockedOut);
  c.update(90,{true,false,false,4095});
  assert(c.update(125,{true,false,false,4095}).pumpRequested);
  assert(!c.update(126,{false,false,true}).pumpRequested);
  assert(!c.begin(0,{}).pumpRequested); // reinitialisation
  c.update(0,{true});
  assert(!c.update(35,{true}).pumpRequested); // zero setting
  c.begin(0xfffffff0u,{});
  c.update(0xfffffff0u,{true,false,false,65535});
  o=c.update(0x13u,{true,false,false,65535});
  assert(o.pumpRequested && o.doseMs==5000);
  assert(!c.update(0x13u+5000,{}).pumpRequested);
  return 0;
}
