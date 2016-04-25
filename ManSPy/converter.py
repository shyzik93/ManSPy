def Extraction2IL(version):
    return __import__('converter_assocv'+str(version), globals={"__name__":__name__}, level=1).Extraction2IL
