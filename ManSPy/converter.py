def Extraction2IL(version):
    return __import__('converter_assocv'+str(version), globals={"__name__":__name__}).Extraction2IL
