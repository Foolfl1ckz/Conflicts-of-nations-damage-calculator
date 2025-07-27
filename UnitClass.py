type_list = ["soft", "hard", "fixed wing", "rotary wing", "drone", "missile", "ship", "submarine"]
class Debuff:
    def __init__(self, open=0, mountain=0, forest=0, city=0, suburbs=0,
                 jungle=0, tundra=0, desert=0, deep_sea=0, low_sea=0):
        self.open = open
        self.mountain = mountain
        self.forest = forest
        self.city = city
        self.suburbs = suburbs
        self.jungle = jungle
        self.tundra = tundra
        self.desert = desert
        self.deep_sea = deep_sea
        self.low_sea = low_sea

    def to_dict(self):
        return self.__dict__
    
    def __repr__(self):
        return (f"Debuff(open={self.open}, mountain={self.mountain}, forest={self.forest}, city={self.city}, "
                f"suburbs={self.suburbs}, jungle={self.jungle}, tundra={self.tundra}, desert={self.desert}, "
                f"deep_sea={self.deep_sea}, low_sea={self.low_sea})")

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    


class Unit:
    def __init__(self, name: str, weight: float, debuffs: Debuff, type: str = None, extra_debuffs: float = 0,):
        self.name = name
        self.weight = weight
        self.debuffs = debuffs
        self.extra_debuffs = extra_debuffs
        self.type = type

    def to_dict(self):
        return {
            "name": self.name,
            "weight": self.weight,
            "debuffs": self.debuffs.to_dict()
            
        }
    
    def __repr__(self):
            return self.name

    @classmethod
    def from_dict(cls, data, type, extra_debuffs = 0):
        "Loads unit from a dictionary"
        debuff = Debuff.from_dict(data["debuffs"])
        return cls(data["name"], data["weight"], debuff, type, extra_debuffs)


class UnitDamage:
    def __init__(self, unit_list: list):
        self.unit_list = unit_list

    def simple_attack(self, dmg_list):

        def zip_dmg_list(dmg_list):
            dmg_dict = {}
            for i in range(len(dmg_list)):
                dmg_dict[type_list[i]] = dmg_list[i]
            return dmg_dict

        dealt_dmg = []
        weight_list = []
        weighted_list = []
        dmg_dict = zip_dmg_list(dmg_list)
        sum = 0
        for unit in self.unit_list:
            weight_list.append(unit.weight)
            sum += unit.weight
        for i in weight_list:
            weighted_list.append(i/sum) #Gets damage percentile
        for i in range(len(self.unit_list)):
            unit = self.unit_list[i]
            amplifyer = (100-unit.extra_debuffs)/100 #Applies simple buffs/debuffs
            dealt_dmg.append((unit, (dmg_dict[unit.type]*weighted_list[i])*amplifyer)) #Gets estimated damage (Note there is rng on upto +/-50%)
        return dealt_dmg
