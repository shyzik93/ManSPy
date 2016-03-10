def Extract(version):
    return __import__('extractor_assocv'+str(version), globals={"__name__":__name__}).Extract
