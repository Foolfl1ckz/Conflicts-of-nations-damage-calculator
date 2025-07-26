import UnitClass as uc
type_list = ["soft", "hard", "fixed wing", "rotary wing", "drone", "missile", "ship", "submarine", "multible"]

unit_list = [
    uc.Unit("Motorized Infantry", 3, uc.Debuff(), type_list[0]),
    uc.Unit("Mechanized Infantry", 7, uc.Debuff(),type_list[0]),
    uc.Unit("Airborne Infantry", 5, uc.Debuff(),type_list[0]),
    uc.Unit("National Guard", 4, uc.Debuff(),type_list[0]),
    uc.Unit("Mountain Infantry", 3, uc.Debuff(),type_list[0]),
    uc.Unit("Marine Infantry", 6, uc.Debuff(),type_list[0]),
    uc.Unit("Special Forces", 1, uc.Debuff(),type_list[0]),
    uc.Unit("Mercenaries", 10, uc.Debuff(),type_list[0]),
    uc.Unit("Combat Recon Vehicle", 2, uc.Debuff(),type_list[1]),
    uc.Unit("Amphibious Combat Vehicle", 6, uc.Debuff(),type_list[1]),
    uc.Unit("Tank Destroyer", 8, uc.Debuff(),type_list[1]),
    uc.Unit("Armored Fighting Vehicle", 7, uc.Debuff(),type_list[1]),
    uc.Unit("Main Battle Tank", 9, uc.Debuff(),type_list[1]),
    uc.Unit("Towed Artillery", 2, uc.Debuff(),type_list[0]),
    uc.Unit("Multiple Rocket Launcher", 6, uc.Debuff(),type_list[1]),
    uc.Unit("SAM", 3, uc.Debuff(),type_list[1]),
    uc.Unit("Mobile Radar", 1, uc.Debuff(),type_list[1]),
    uc.Unit("Mobile Artillery", 6, uc.Debuff(),type_list[1]),
    uc.Unit("Mobile Anti-Aircraft", 4, uc.Debuff(),type_list[1]),
    uc.Unit("TDS", 1, uc.Debuff(),type_list[1]),
    uc.Unit("Infantry Officer", 2, uc.Debuff(),type_list[0]),
    uc.Unit("Tank Officer", 5, uc.Debuff(),type_list[1]),
    uc.Unit("Airborne Officer", 1, uc.Debuff(),type_list[0]),
    uc.Unit("Elite Main Battle Tank", 7, uc.Debuff(),type_list[1]),
    uc.Unit("Elite UGV", 1.5, uc.Debuff(),type_list[1]),
    uc.Unit("Elite Drone Operator", 2, uc.Debuff(),type_list[4]),
    uc.Unit("Elite Railgun", 7, uc.Debuff(),type_list[1]),
    uc.Unit("Elite Special Forces", 1, uc.Debuff(),type_list[0]),
    uc.Unit("Elite Armored Fighting Vehicle", 1, uc.Debuff(),type_list[1]),
    uc.Unit("ICBM Launcher", 1, uc.Debuff(),type_list[5]),
    uc.Unit("CM Launcher", 1, uc.Debuff(),type_list[5]),
    uc.Unit("BM Launcher", 1, uc.Debuff(),type_list[5]),

]

terrain_list = ["open", "mountain", "forest", "city", "suburbs", "jungle", "tundra", "desert", "deep_sea", "low_sea"]
