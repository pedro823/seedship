from language import LANG_DICT
import random as r
import settings
from planet import Planet


class SeedshipModule:

    def __init__(self, name: str, health: int = 100):
        self.name = self.resolve_module_name(name)
        self.health = health

    @classmethod
    def resolve_module_name(cls, name: str) -> str:
        return LANG_DICT['seedship_module'].get(name, name)

    def damage(self, amount: int):
        self.health = max(0, self.health - amount)


class Scanner(SeedshipModule):
    ''' Represents a scanner of the seedship. '''

    def __init__(self, name: str):
        super().__init__(name)
        self.upgrade_level = 0

    def upgrade(self):
        if self.upgrade_level >= 2:
            raise Exception('Upgrade at max level')
        self.upgrade_level += 1

    def scan_hits(self) -> bool:
        ''' Scan hits the target? '''
        return r.randint(1, 100) < self.health


class System(SeedshipModule):
    ''' Represent a landing/construction system inside the seedship. '''
    pass


class Database(SeedshipModule):
    ''' Represents a seedship's database '''
    pass


class ScanResult:
    ''' Represents a scan result of a probe or from seedship '''

    SCAN_FAILURE = settings.SCAN_FAILURE

    @classmethod
    def from_probe(cls, planet):
        return ScanResult(atmosphere=planet.atmosphere,
                          gravity=planet.gravity,
                          temperature=planet.temperature,
                          water=planet.water,
                          resources=planet.resources,
                          landscape=planet.landscape,
                          from_probe=True)

    def __init__(self,
                 atmosphere,
                 gravity,
                 temperature,
                 water,
                 resources,
                 landscape=None,
                 from_probe=False):
        self.atmosphere = atmosphere
        self.gravity = gravity
        self.temperature = temperature
        self.water = water
        self.resources = resources
        self.landscape = landscape
        self.from_probe = from_probe


class Seedship:

    def __init__(self):
        atmosphere_scanner = Scanner('atmosphere_scanner')
        gravity_scanner = Scanner('gravity_scanner')
        temperature_scanner = Scanner('temperature_scanner')
        water_scanner = Scanner('water_scanner')
        resources_scanner = Scanner('resources_scanner')
        self.scanners = {
            'atmosphere': atmosphere_scanner,
            'gravity': gravity_scanner,
            'temperature': temperature_scanner,
            'water': water_scanner,
            'resources': resources_scanner
        }
        cultural_database = Database('cultural_database')
        scientific_database = Database('scientific_database')
        self.databases = {
            'cultural': cultural_database,
            'scientific': scientific_database
        }
        landing_system = System('landing_system')
        construction_system = System('construction_system')
        self.systems = {
            'landing': landing_system,
            'construction': construction_system
        }
        self.planet = None
        self.scan_result = None
        self.probes_left = 10

    def scan_planet(self) -> ScanResult:
        if self.scan_result is not None:
            return self.scan_result
        if self.planet is None:
            raise Exception('Cannot scan None')
        scan_results = {}
        for name, scanner in self.scanners.items():
            scan_results[name] = getattr(self.planet, name) \
                                    if scanner.scan_hits() \
                                    else ScanResult.SCAN_FAILURE
        self.scan_result = ScanResult(**scan_results)
        return self.scan_result

    def probe_planet(self) -> ScanResult:
        if self.scan_result is not None and self.scan_result.from_probe:
            return self.scan_result
        if self.probes_left <= 0:
            raise Exception('No probes left')
        if self.planet is None:
            raise Exception('Cannot scan None')
        self.probes_left -= 1
        self.scan_result = ScanResult.from_probe(self.planet)
        return self.scan_result

    def move_on(self):
        self.planet = None
        self.scan_result = None

    def find_new_planet(self):
        self.planet = Planet.from_scanners(self.scanners)
        self.scan_result = None


if __name__ == '__main__':
    sdshp = Seedship()
    for scanner in sdshp.scanners.values():
        for _ in range(2):
            scanner.upgrade()
    sdshp.find_new_planet()
    print(sdshp.planet.atmosphere)
    print(sdshp.planet.temperature)
    print(sdshp.planet.gravity)
    print(sdshp.planet.water)
    print(sdshp.planet.resources)
