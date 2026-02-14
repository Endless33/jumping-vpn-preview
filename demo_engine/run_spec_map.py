from spec_map import SpecMap

if __name__ == "__main__":
    mapper = SpecMap()
    mapper.load_spec()
    mapper.index_code()
    mapper.match()
    path = mapper.export()
    print(f"SPEC_MAP generated: {path}")