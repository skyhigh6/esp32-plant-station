#include <assert.h>
#include "../arduino/PlantUno/PlantView.h"
#include "../arduino/PlantUno/PlantController.h"
int main() {
  assert(moisturePercent(447) == 0);
  assert(moisturePercent(221) == 100);
  assert(moisturePercent(189) == 100);
  assert(moisturePercent(334) == 50);
  assert(moisturePercent(1023) == 0);
  SoilIndicator soil;
  soil.begin(0, 0);
  assert(soil.state() == SoilState::Fault);
  assert(redSoilBlink(SoilState::Fault, 50));
  assert(!redSoilBlink(SoilState::Fault, 150));
  assert(soil.update(100, 390) == SoilState::Fault); // 25% is wet/green.
  assert(soil.update(600, 390) == SoilState::Wet);
  assert(soil.percent() == 25);
  assert(soil.update(700, 391) == SoilState::Wet); // 24% candidate.
  assert(soil.percent() == 25); // Status display follows the accepted lamp state.
  assert(soil.update(1199, 391) == SoilState::Wet);
  assert(soil.update(1200, 391) == SoilState::Dry);
  assert(soil.percent() == 24);
  assert(redSoilBlink(SoilState::Dry, 200));
  assert(!redSoilBlink(SoilState::Dry, 700));
  assert(soil.update(1300, 0) == SoilState::Fault); // No false wet on rail-low A0.
  DebouncedPress t;
  t.begin(0, false);
  auto press = [&](uint32_t n) { assert(!t.update(n,true)); return t.update(n+35,true); };
  auto release = [&](uint32_t n) { assert(!t.update(n,false)); assert(!t.update(n+35,false)); };
  assert(press(100)); release(200);
  assert(press(300)); release(400);
  assert(!t.update(900,true)); // New press must debounce.
  assert(t.update(935,true));
  assert(!t.update(950,true)); // Holding is not another press.
  release(1000);
  t.begin(0,true);
  assert(!t.update(100,true)); // Boot-held input does not count.
  release(200);
  assert(!t.update(300,true)); assert(!t.update(310,false));
  assert(!t.update(350,false)); // Short bounce does not count.
  assert(press(800));
  t.begin(0xffffff00u,false);
  assert(press(0xfffffff0u)); release(0x30u);
  assert(press(0x80u)); // Debounce works across millis rollover.
  plant::PlantController ranged(plant::ControllerConfig{35, 4000, 1000});
  assert(ranged.plannedDoseMs(0) == 1000);
  assert(ranged.plannedDoseMs(4095) == 4000);
  assert(ranged.plannedDoseMs(65535) == 4000);
  assert(ranged.plannedDoseMs(2048) >= 2499 && ranged.plannedDoseMs(2048) <= 2501);
  ranged.begin(0, {});
  ranged.update(10, {true,false,false,0});
  auto dose = ranged.update(45, {true,false,false,0});
  assert(dose.pumpRequested && dose.doseMs == 1000);
  assert(ranged.update(1044, {}).pumpRequested);
  assert(!ranged.update(1045, {}).pumpRequested);
  plant::PlantController c;
  c.begin(0,{});
  assert(!c.update(100,{true,false,true,4095}).pumpRequested);
  assert(!c.update(200,{true,false,false,4095}).pumpRequested);
  assert(c.update(300,{}).lockedOut);
  assert(!c.update(335,{}).lockedOut);
  c.update(400,{true,false,false,4095});
  assert(c.update(435,{true,false,false,4095}).pumpRequested);
}
