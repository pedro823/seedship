from .language import TXT
import random as r
from .util import Color, SeedshipExecutionError
from .planet import Planet


class SeedshipModule:

    def __init__(self, name: str, health: int = 100):
        self.name = self.resolve_module_name(name)
        self.health = health
        self.full_health = health

    def get_color(self) -> str:
        ''' Returns a color representing the status of the module '''
        ratio = self.health / self.full_health
        if ratio <= 0.1:
            return Color.RED + Color.BLINK
        if ratio <= 0.4:
            return Color.LIGHT_RED
        if ratio <= 0.7:
            return Color.YELLOW
        if ratio <= 0.95:
            return Color.LIGHT_GREEN
        return Color.GREEN

    @classmethod
    def resolve_module_name(cls, name: str) -> str:
        return TXT['seedship_module'].get(name, name)

    def damage(self, amount: int):
        if amount < 0:
            raise SeedshipExecutionError('invalid_amount')
        self.health = max(0, self.health - amount)

    def trace_damage(self, chance: float, max_amount: int):
        if r.random() < chance:
            self.health -= r.choice(range(max_amount))


class SeedshipConsumable:

    name = TXT['seedship_consumables']['consumable']

    def __init__(self, name: str, amount: int):
        self.name = self.resolve_module_name(name)
        self.amount = amount
        self.full_amount = amount

    def get_color(self) -> str:
        ''' Gets status level color '''
        ratio = self.get_ratio()
        if ratio <= 0.1:
            return Color.RED + Color.BLINK
        if ratio <= 0.4:
            return Color.LIGHT_RED
        if ratio <= 0.7:
            return Color.YELLOW
        if ratio <= 0.95:
            return Color.LIGHT_GREEN
        return Color.GREEN

    def get_ratio(self) -> float:
        ''' Gets ratio of amount / full_amount '''
        return self.amount / self.full_amount

    def waste(self, amount: int):
        if amount < 0:
            raise SeedshipExecutionError('invalid_amount')
        self.amount = max(self.amount - amount, 0)

    def repair(self, amount: int):
        if amount < 0:
            raise SeedshipExecutionError('invalid_amount')
        self.amount = min(self.amount + amount, self.full_amount)

    @classmethod
    def resolve_module_name(cls, name: str) -> str:
        return TXT['seedship_consumables'].get(name, name)


class Scanner(SeedshipModule):
    ''' Represents a scanner of the seedship. '''
    name = SeedshipModule.resolve_module_name('scanner')

    def __init__(self, name: str):
        super().__init__(name)
        self.upgrade_level = 0

    def upgrade(self):
        if self.upgrade_level >= 2:
            raise SeedshipExecutionError('upgrade_max_level')
        self.upgrade_level += 1

    def scan_hits(self) -> bool:
        ''' Scan hits the target? '''
        return r.randint(1, 100) <= self.health

    def repair(self, amount: int):
        if amount < 0:
            raise SeedshipExecutionError('invalid_amount')
        self.health = min(self.health + amount, self.full_health)


class System(SeedshipModule):
    ''' Represent a landing/construction system inside the seedship. '''
    name = SeedshipModule.resolve_module_name('system')


class Database(SeedshipModule):
    ''' Represents a seedship's database '''
    name = SeedshipModule.resolve_module_name('database')

    def repair(self, amount):
        if amount < 0:
            raise SeedshipExecutionError('invalid_amount')
        self.health += amount  # can go over full health, intentional.


class Colonists:
    name = SeedshipModule.resolve_module_name('colonists')

    def __init__(self):
        self.amount = 1000

    def damage(self, amount: int):
        if amount < 0:
            raise SeedshipExecutionError('invalid_amount')
        self.amount = max(0, self.amount - amount)

    def __lt__(self, number: int):
        return self.amount < number

    def __str__(self):
        return str(self.amount)


class ScanResult:
    ''' Represents a scan result of a probe or from seedship '''

    class ScanFailure:
        text = TXT['scanner']['scan_failed']
        color = Color.RED

    @classmethod
    def from_probe(cls, planet: Planet):
        return ScanResult(atmosphere=planet.atmosphere,
                          gravity=planet.gravity,
                          temperature=planet.temperature,
                          water=planet.water,
                          resources=planet.resources,
                          landscape=planet.landscape,
                          was_from_probe=True)

    def __init__(self,
                 atmosphere,
                 gravity,
                 temperature,
                 water,
                 resources,
                 landscape=None,
                 was_from_probe=False):
        self.features = {
            'atmosphere': atmosphere,
            'gravity': gravity,
            'temperature': temperature,
            'water': water,
            'resources': resources
        }
        self.landscape = landscape
        self.was_from_probe = was_from_probe


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
        self.modules = [self.scanners, self.databases, self.systems]
        self.planet = None
        self.scan_result = None
        self.probes_left = 10
        self.colonists = Colonists()
        self.fuel = SeedshipConsumable('fuel', 200)
        self.energy = SeedshipConsumable('energy', 40)
        self.consumables = [self.fuel, self.energy]
        self.evaded_colision = False

    def scan_planet(self) -> ScanResult:
        ''' Scans a planet with seedship's own scanners '''
        if self.scan_result is not None:
            return self.scan_result
        if self.planet is None:
            raise Exception('Cannot scan None')
        scan_results = {}
        for name, scanner in self.scanners.items():
            scan_results[name] = getattr(self.planet, name) \
                                    if scanner.scan_hits() \
                                    else ScanResult.ScanFailure
        self.scan_result = ScanResult(**scan_results)
        return self.scan_result

    def probe_planet(self) -> ScanResult:
        ''' Sends a probe to the planet for full scan results '''
        if self.scan_result is not None and self.scan_result.was_from_probe:
            return self.scan_result
        if self.probes_left <= 0:
            raise Exception('No probes left')
        if self.planet is None:
            raise Exception('Cannot scan None')
        self.probes_left -= 1
        self.scan_result = ScanResult.from_probe(self.planet)
        return self.scan_result

    def find_new_planet(self):
        if self.evaded_colision:
            self.planet = Planet.from_evasion(self.scanners)
            self.evaded_colision = False
        else:
            self.planet = Planet.from_scanners(self.scanners)
        self.scan_result = None

    def evade_colision(self):
        self.evaded_colision = True

    def deal_trace_damage(self):
        ''' Deals trace damage by wear & tear '''
        for scanner in self.scanners.values():
            scanner.trace_damage(0.3, 3)
        for database in self.databases.values():
            database.trace_damage(0.3, 2)
        for system in self.systems.values():
            system.trace_damage(0.3, 2)

    def recharge_trace_energy(self):
        ''' Recharges trace amount of energy due to solar panels '''
        if r.random() < 0.4:
            self.energy = min(self.energy + r.choice(range(3)), 40)

    def to_dict(self) -> dict:
        ''' returns a representation of the seedship into a dictionary '''
        return {
            'scanners': {
                    name: {'health': scanner.health, 'upgrade_level': scanner.upgrade_level}
                    for name, scanner in self.scanners.items()
            },
            'databases': {
                name: database.health
                for name, database in self.databases.items()
            },
            'systems': {
                name: system.health
                for name, system in self.systems.items()
            },
            'colonists': self.colonists.amount,
            'probes': self.probes_left
        }


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
